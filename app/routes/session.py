from datetime import datetime, timezone

from flask import Blueprint, g, jsonify, redirect, request
from flask import session as cookie_session
from flask import url_for
from flask_login import login_required, logout_user
from marshmallow import ValidationError
from sdc.crypto.exceptions import InvalidTokenException
from structlog import get_logger
from werkzeug.exceptions import Unauthorized

from app.authentication.auth_payload_version import AuthPayloadVersion
from app.authentication.authenticator import decrypt_token, store_session
from app.authentication.jti_claim_storage import JtiTokenUsed, use_jti_claim
from app.data_models.metadata_proxy import MetadataProxy
from app.globals import get_session_store, get_session_timeout_in_seconds
from app.helpers.template_helpers import get_survey_config, render_template
from app.utilities.metadata_parser import validate_runner_claims
from app.utilities.metadata_parser_v2 import (
    validate_questionnaire_claims,
    validate_runner_claims_v2,
)
from app.utilities.schema import load_schema_from_metadata

logger = get_logger()

session_blueprint = Blueprint("session", __name__)


@session_blueprint.after_request
def add_cache_control(response):
    response.cache_control.no_cache = True
    return response


@session_blueprint.route("/session", methods=["HEAD"])
def login_head():
    return "", 204


@session_blueprint.route("/session", methods=["GET", "POST"])
def login():
    """
    Initial url processing - expects a token parameter and then will authenticate this token. Once authenticated
    it will be placed in the users session
    :return: a 302 redirect to the next location for the user
    """
    # logging in again clears any session state
    if cookie_session:
        cookie_session.clear()

    decrypted_token = decrypt_token(request.args.get("token"))

    validate_jti(decrypted_token)

    runner_claims = get_runner_claims(decrypted_token)

    metadata = MetadataProxy.from_dict(runner_claims)

    # pylint: disable=assigning-non-slot
    g.schema = load_schema_from_metadata(metadata=metadata)
    schema_metadata = g.schema.json["metadata"]

    questionnaire_claims = get_questionnaire_claims(
        decrypted_token=decrypted_token, schema_metadata=schema_metadata
    )

    theme = g.schema.json["theme"]
    questionnaire_id = None

    if decrypted_token.get("version") == AuthPayloadVersion.V2.value:
        runner_claims["survey_metadata"]["data"] = questionnaire_claims

        data = runner_claims.get("survey_metadata").get("data", {})
        ru_ref = data.get("ru_ref")
        questionnaire_id = data.get("questionnaire_id")

        claims = runner_claims
    else:
        claims = {**runner_claims, **questionnaire_claims}
        ru_ref = claims["ru_ref"]

    tx_id = claims["tx_id"]
    case_id = claims["case_id"]

    logger.bind(
        tx_id=tx_id,
        case_id=case_id,
    )

    if schema_name := metadata["schema_name"]:
        logger.bind(schema_name=schema_name)

    if schema_url := metadata["schema_url"]:
        logger.bind(schema_url=schema_url)

    if ru_ref:
        logger.bind(ru_ref=ru_ref)

    if questionnaire_id:
        logger.bind(questionnaire_id=questionnaire_id)

    logger.info("decrypted token and parsed metadata")

    store_session(claims)

    cookie_session["theme"] = theme
    cookie_session["survey_title"] = g.schema.json["title"]
    cookie_session["expires_in"] = get_session_timeout_in_seconds(g.schema)

    if account_service_url := claims.get("account_service_url"):
        cookie_session["account_service_base_url"] = account_service_url

    if claims.get("account_service_log_out_url"):
        cookie_session["account_service_log_out_url"] = claims.get(  # pragma: no cover
            "account_service_log_out_url"
        )

    return redirect(url_for("questionnaire.get_questionnaire"))


def validate_jti(decrypted_token):
    expires_at = datetime.fromtimestamp(decrypted_token["exp"], tz=timezone.utc)
    jwt_expired = expires_at < datetime.now(tz=timezone.utc)
    if jwt_expired:
        raise Unauthorized

    jti_claim = decrypted_token.get("jti")
    try:
        use_jti_claim(jti_claim, expires_at)
    except JtiTokenUsed as e:
        raise Unauthorized from e
    except (TypeError, ValueError) as e:
        raise InvalidTokenException from e


@session_blueprint.route("/session-expired", methods=["GET"])
def get_session_expired():
    # Check for GET as we don't want to log out for HEAD requests
    if request.method == "GET":
        logout_user()

    return render_template("errors/401")


@session_blueprint.route("/session-expiry", methods=["GET", "PATCH"])
@login_required
def session_expiry():
    return jsonify(expires_at=get_session_store().expiration_time.isoformat())


@session_blueprint.route("/sign-out", methods=["GET"])
def get_sign_out():
    """
    Signs the user out of eQ and redirects to the log out url.
    """
    survey_config = get_survey_config()
    log_out_url = (
        survey_config.account_service_todo_url if "todo" in request.args else None
    )

    if not log_out_url:
        log_out_url = survey_config.account_service_log_out_url

    # Check for GET as we don't want to log out for HEAD requests
    if request.method == "GET":
        logout_user()

    return redirect(log_out_url)


@session_blueprint.route("/signed-out", methods=["GET"])
def get_signed_out():
    return render_template(template="signed-out")


def get_runner_claims(decrypted_token):
    if decrypted_token.get("version"):
        if decrypted_token.get("version") == AuthPayloadVersion.V2.value:
            try:
                return validate_runner_claims_v2(decrypted_token)
            except ValidationError as e:
                raise InvalidTokenException("Invalid runner claims") from e

    try:
        return validate_runner_claims(decrypted_token)
    except ValidationError as e:
        raise InvalidTokenException("Invalid runner claims") from e


def get_questionnaire_claims(decrypted_token, schema_metadata):
    try:
        if decrypted_token.get("version") == AuthPayloadVersion.V2.value:
            claims = decrypted_token.get("survey_metadata", {}).get("data", {})
        else:
            claims = decrypted_token

        return validate_questionnaire_claims(claims, schema_metadata)

    except ValidationError as e:
        raise InvalidTokenException("Invalid questionnaire claims") from e
