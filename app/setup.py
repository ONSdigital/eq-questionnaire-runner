from copy import deepcopy
from typing import Dict
from uuid import uuid4

import boto3
import redis
import yaml
from botocore.config import Config
from flask import Flask
from flask import request as flask_request
from flask import session as cookie_session
from flask_babel import Babel
from flask_compress import Compress
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from google.cloud import datastore
from htmlmin.main import minify
from jinja2 import ChainableUndefined
from sdc.crypto.key_store import KeyStore, validate_required_keys
from structlog import contextvars, get_logger

from app import settings
from app.authentication.authenticator import login_manager
from app.authentication.cookie_session import SHA256SecureCookieSessionInterface
from app.authentication.user_id_generator import UserIDGenerator
from app.cloud_tasks import CloudTaskPublisher, LogCloudTaskPublisher
from app.helpers import get_span_and_trace
from app.jinja_filters import blueprint as filter_blueprint
from app.keys import KEY_PURPOSE_AUTHENTICATION, KEY_PURPOSE_SUBMISSION
from app.oidc.gcp_oidc import OIDCCredentialsServiceGCP
from app.oidc.local_oidc import OIDCCredentialsServiceLocal
from app.publisher import LogPublisher, PubSubPublisher
from app.routes.dump import dump_blueprint
from app.routes.errors import errors_blueprint
from app.routes.flush import flush_blueprint
from app.routes.individual_response import individual_response_blueprint
from app.routes.questionnaire import post_submission_blueprint, questionnaire_blueprint
from app.routes.schema import schema_blueprint
from app.routes.session import session_blueprint
from app.secrets import SecretStore, validate_required_secrets
from app.settings import DEFAULT_LOCALE
from app.storage import Datastore, Dynamodb, Redis
from app.submitter import (
    GCSFeedbackSubmitter,
    GCSSubmitter,
    LogFeedbackSubmitter,
    LogSubmitter,
    RabbitMQSubmitter,
)
from app.utilities.json import json_dumps
from app.utilities.schema import cache_questionnaire_schemas

CACHE_HEADERS = {
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
}

CSP_POLICY = {
    "default-src": ["'self'"],
    "font-src": ["'self'", "data:", "https://fonts.gstatic.com"],
    "script-src": [
        "'self'",
        "https://*.googletagmanager.com",
    ],
    "style-src": [
        "'self'",
        "https://fonts.googleapis.com",
        "'unsafe-inline'",
    ],
    "connect-src": [
        "'self'",
        "https://*.google-analytics.com",
        "https://*.analytics.google.com",
        "https://*.googletagmanager.com",
    ],
    "img-src": [
        "'self'",
        "data:",
        "https://ssl.gstatic.com",
        "https://www.gstatic.com",
        "https://*.google-analytics.com",
        "https://*.googletagmanager.com",
    ],
    "object-src": ["'none'"],
    "base-uri": ["'none'"],
}

compress = Compress()

logger = get_logger()


class MissingEnvironmentVariable(Exception):
    pass


class AWSReverseProxied:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get("HTTP_X_FORWARDED_PROTO", "http")
        if scheme:
            environ["wsgi.url_scheme"] = scheme
        return self.app(environ, start_response)


def create_app(  # noqa: C901  pylint: disable=too-complex, too-many-statements
    setting_overrides=None,
):
    application = Flask(__name__, template_folder="../templates")
    application.config.from_object(settings)
    if setting_overrides:
        application.config.update(setting_overrides)
    application.eq = {}

    with open(application.config["EQ_SECRETS_FILE"], encoding="UTF-8") as secrets_file:
        secrets = yaml.safe_load(secrets_file)
    conditional_required_secrets = []
    if application.config["ADDRESS_LOOKUP_API_AUTH_ENABLED"]:
        conditional_required_secrets.append("ADDRESS_LOOKUP_API_AUTH_TOKEN_SECRET")
    validate_required_secrets(secrets, conditional_required_secrets)
    application.eq["secret_store"] = SecretStore(secrets)

    with open(application.config["EQ_KEYS_FILE"], encoding="UTF-8") as keys_file:
        keys = yaml.safe_load(keys_file)
    validate_required_keys(keys, KEY_PURPOSE_SUBMISSION)
    validate_required_keys(keys, KEY_PURPOSE_AUTHENTICATION)
    application.eq["key_store"] = KeyStore(keys)

    if application.config["EQ_APPLICATION_VERSION"]:
        logger.info(
            "starting eq survey runner",
            version=application.config["EQ_APPLICATION_VERSION"],
        )

    # IMPORTANT: This must be initialised *before* any other Flask plugins that add
    # before_request hooks. Otherwise any logging by the plugin in their before
    # request will use the logger context of the previous request.
    @application.before_request
    def before_request():
        contextvars.clear_contextvars()

        request_id = str(uuid4())

        contextvars.bind_contextvars(request_id=request_id)

        span, trace = get_span_and_trace(flask_request.headers)
        if span and trace:
            contextvars.bind_contextvars(span=span, trace=trace)

        logger.info(
            "request",
            method=flask_request.method,
            url_path=flask_request.full_path,
            session_cookie_present="session" in flask_request.cookies,
            csrf_token_present="csrf_token" in cookie_session,
            user_agent=flask_request.user_agent.string,
        )

    setup_storage(application)

    setup_submitter(application)

    setup_feedback(application)

    setup_publisher(application)

    setup_task_client(application)

    setup_oidc(application)

    application.eq["id_generator"] = UserIDGenerator(
        application.config["EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS"],
        application.eq["secret_store"].get_secret_by_name(
            "EQ_SERVER_SIDE_STORAGE_USER_ID_SALT"
        ),
        application.eq["secret_store"].get_secret_by_name(
            "EQ_SERVER_SIDE_STORAGE_USER_IK_SALT"
        ),
    )

    cache_questionnaire_schemas()

    setup_secure_cookies(application)

    setup_secure_headers(application)

    setup_babel(application)

    application.wsgi_app = AWSReverseProxied(application.wsgi_app)

    application.url_map.strict_slashes = False

    add_blueprints(application)

    login_manager.init_app(application)

    add_safe_health_check(application)

    setup_compression(application)

    setup_jinja_env(application)

    @application.after_request
    def apply_caching(response):
        if "text/html" in response.content_type:
            for k, v in CACHE_HEADERS.items():
                response.headers[k] = v
        else:
            response.headers["Cache-Control"] = "max-age=2628000, public"

        return response

    @application.after_request
    def response_minify(response):
        """
        minify html response to decrease site traffic
        """
        if (
            application.config["EQ_ENABLE_HTML_MINIFY"]
            and response.content_type == "text/html; charset=utf-8"
        ):
            response.set_data(
                minify(
                    response.get_data(as_text=True),
                    remove_comments=True,
                    remove_empty_space=True,
                    remove_optional_attribute_quotes=False,
                )
            )

            return response
        return response

    @application.after_request
    def after_request(response):
        # We're using the stringified version of the Flask session to get a rough
        # length for the cookie. The real length won't be known yet as Flask
        # serializes and adds the cookie header after this method is called.
        logger.info(
            "response",
            status_code=response.status_code,
            session_modified=cookie_session.modified,
        )
        return response

    return application


def setup_jinja_env(application):
    # Enable whitespace removal
    application.jinja_env.trim_blocks = True
    application.jinja_env.lstrip_blocks = True
    application.jinja_env.undefined = ChainableUndefined

    # Switch off flask default autoescaping as schema content can contain html
    application.jinja_env.autoescape = False

    application.jinja_env.add_extension("jinja2.ext.do")


def _add_cdn_url_to_csp_policy(cdn_url) -> Dict:
    csp_policy = deepcopy(CSP_POLICY)
    for directive in csp_policy:
        if directive not in ["frame-src", "object-src", "base-uri"]:
            csp_policy[directive].append(cdn_url)
    return csp_policy


def setup_secure_headers(application):
    csp_policy = _add_cdn_url_to_csp_policy(application.config["CDN_URL"])

    if api_url := application.config["ADDRESS_LOOKUP_API_URL"]:
        csp_policy["connect-src"] += [api_url]

    if application.config["EQ_ENABLE_LIVE_RELOAD"]:
        # browsersync is configured to bind on port 5075
        csp_policy["connect-src"] += ["ws://localhost:35729"]

    application.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    Talisman(
        application,
        content_security_policy=csp_policy,
        content_security_policy_nonce_in=["script-src"],
        session_cookie_secure=application.config["EQ_ENABLE_SECURE_SESSION_COOKIE"],
        force_https=False,  # this is handled at the firewall
        strict_transport_security=True,
        strict_transport_security_max_age=31536000,
        frame_options="DENY",
        x_xss_protection=True,
    )


def setup_storage(application):
    if application.config["EQ_STORAGE_BACKEND"] == "datastore":
        setup_datastore(application)
    elif application.config["EQ_STORAGE_BACKEND"] == "dynamodb":
        setup_dynamodb(application)
    else:
        raise NotImplementedError("Unknown EQ_STORAGE_BACKEND")

    setup_redis(application)


def setup_dynamodb(application):
    # Number of additional connection attempts
    config = Config(
        retries={"max_attempts": application.config["EQ_DYNAMODB_MAX_RETRIES"]},
        max_pool_connections=application.config["EQ_DYNAMODB_MAX_POOL_CONNECTIONS"],
    )

    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=application.config["EQ_DYNAMODB_ENDPOINT"],
        config=config,
    )
    application.eq["storage"] = Dynamodb(dynamodb)


def setup_datastore(application):
    client = datastore.Client(_use_grpc=application.config["DATASTORE_USE_GRPC"])
    application.eq["storage"] = Datastore(client)


def setup_redis(application):
    redis_client = redis.Redis(
        host=application.config["EQ_REDIS_HOST"],
        port=application.config["EQ_REDIS_PORT"],
        retry_on_timeout=True,
    )

    application.eq["ephemeral_storage"] = Redis(redis_client)


def setup_submitter(application):
    if application.config["EQ_SUBMISSION_BACKEND"] == "gcs":
        if not (bucket_name := application.config.get("EQ_GCS_SUBMISSION_BUCKET_ID")):
            raise MissingEnvironmentVariable(
                "Setting EQ_GCS_SUBMISSION_BUCKET_ID Missing"
            )

        application.eq["submitter"] = GCSSubmitter(bucket_name=bucket_name)

    elif application.config["EQ_SUBMISSION_BACKEND"] == "rabbitmq":
        host = application.config.get("EQ_RABBITMQ_HOST")
        secondary_host = application.config.get("EQ_RABBITMQ_HOST_SECONDARY")

        if not host:
            raise MissingEnvironmentVariable("Setting EQ_RABBITMQ_HOST Missing")
        if not secondary_host:
            raise MissingEnvironmentVariable(
                "Setting EQ_RABBITMQ_HOST_SECONDARY Missing"
            )

        application.eq["submitter"] = RabbitMQSubmitter(
            host=host,
            secondary_host=secondary_host,
            port=application.config["EQ_RABBITMQ_PORT"],
            queue=application.config["EQ_RABBITMQ_QUEUE_NAME"],
            username=application.eq["secret_store"].get_secret_by_name(
                "EQ_RABBITMQ_USERNAME"
            ),
            password=application.eq["secret_store"].get_secret_by_name(
                "EQ_RABBITMQ_PASSWORD"
            ),
        )

    elif application.config["EQ_SUBMISSION_BACKEND"] == "log":
        application.eq["submitter"] = LogSubmitter()

    else:
        raise NotImplementedError("Unknown EQ_SUBMISSION_BACKEND")


def setup_task_client(application):
    if application.config["EQ_SUBMISSION_CONFIRMATION_BACKEND"] == "cloud-tasks":
        application.eq["cloud_tasks"] = CloudTaskPublisher()
    elif application.config["EQ_SUBMISSION_CONFIRMATION_BACKEND"] == "log":
        application.eq["cloud_tasks"] = LogCloudTaskPublisher()
    else:
        raise NotImplementedError("Unknown EQ_SUBMISSION_CONFIRMATION_BACKEND")


def setup_oidc(application):
    def client_ids_exist():
        if not application.config.get("SDS_OAUTH2_CLIENT_ID"):
            raise MissingEnvironmentVariable("Setting SDS_OAUTH2_CLIENT_ID Missing")

        if not application.config.get("CIR_OAUTH2_CLIENT_ID"):
            raise MissingEnvironmentVariable("Setting CIR_OAUTH2_CLIENT_ID Missing")

    if not (oidc_token_backend := application.config.get("OIDC_TOKEN_BACKEND")):
        raise MissingEnvironmentVariable("Setting OIDC_TOKEN_BACKEND Missing")

    if oidc_token_backend == "gcp":
        client_ids_exist()
        application.eq["oidc_credentials_service"] = OIDCCredentialsServiceGCP()

    elif oidc_token_backend == "local":
        application.eq["oidc_credentials_service"] = OIDCCredentialsServiceLocal()

    else:
        raise NotImplementedError("Unknown OIDC_TOKEN_BACKEND")


def setup_publisher(application):
    if application.config["EQ_PUBLISHER_BACKEND"] == "pubsub":
        application.eq["publisher"] = PubSubPublisher()

    elif application.config["EQ_PUBLISHER_BACKEND"] == "log":
        application.eq["publisher"] = LogPublisher()

    else:
        raise NotImplementedError("Unknown EQ_PUBLISHER_BACKEND")


def setup_feedback(application):
    if application.config["EQ_FEEDBACK_BACKEND"] == "gcs":
        if not (bucket_name := application.config.get("EQ_GCS_FEEDBACK_BUCKET_ID")):
            raise MissingEnvironmentVariable(
                "Setting EQ_GCS_FEEDBACK_BUCKET_ID Missing"
            )

        application.eq["feedback_submitter"] = GCSFeedbackSubmitter(
            bucket_name=bucket_name
        )

    elif application.config["EQ_FEEDBACK_BACKEND"] == "log":
        application.eq["feedback_submitter"] = LogFeedbackSubmitter()
    else:
        raise NotImplementedError("Unknown EQ_FEEDBACK_BACKEND")


def add_blueprints(application):
    csrf = CSRFProtect(application)

    application.register_blueprint(questionnaire_blueprint)
    questionnaire_blueprint.config = application.config.copy()

    application.register_blueprint(post_submission_blueprint)
    post_submission_blueprint.config = application.config.copy()

    csrf.exempt(session_blueprint)
    application.register_blueprint(session_blueprint)
    session_blueprint.config = application.config.copy()

    csrf.exempt(flush_blueprint)
    application.register_blueprint(flush_blueprint)
    flush_blueprint.config = application.config.copy()

    application.register_blueprint(dump_blueprint)
    dump_blueprint.config = application.config.copy()

    application.register_blueprint(errors_blueprint)
    errors_blueprint.config = application.config.copy()

    application.register_blueprint(filter_blueprint)

    application.register_blueprint(schema_blueprint)
    schema_blueprint.config = application.config.copy()

    application.register_blueprint(individual_response_blueprint)
    individual_response_blueprint.config = application.config.copy()


def setup_secure_cookies(application):
    secret_key = application.eq["secret_store"].get_secret_by_name("EQ_SECRET_KEY")
    if not secret_key:
        raise ValueError("Application secret key does not exist")
    application.secret_key = secret_key
    application.session_interface = SHA256SecureCookieSessionInterface()


def setup_babel(application):
    application.babel = Babel(application)
    application.jinja_env.add_extension("jinja2.ext.i18n")

    application.babel.init_app(
        application, locale_selector=get_locale, timezone_selector=get_timezone
    )


def setup_compression(application):
    application.config["COMPRESS_ALGORITHM"] = ["gzip", "br", "deflate"]
    compress.init_app(application)


def add_safe_health_check(application):
    @application.route("/status")
    def safe_health_check():
        data = {"status": "OK", "version": application.config["EQ_APPLICATION_VERSION"]}
        return json_dumps(data)


def get_minimized_asset(filename):
    """
    If we're in production and it's a js or css file, return the minified version.
    :param filename: the original filename
    :return: the new file name will be .min.css or .min.js
    """
    if settings.EQ_MINIMIZE_ASSETS:
        if "css" in filename:
            filename = filename.replace(".css", ".min.css")
        elif "js" in filename:
            filename = filename.replace(".js", ".min.js")
    return filename


def get_locale():
    return (
        DEFAULT_LOCALE
        if cookie_session.get("language_code") == "en"
        else cookie_session.get("language_code")
    )


def get_timezone():
    # For now regardless of locale we will show times in GMT/BST
    return "Europe/London"
