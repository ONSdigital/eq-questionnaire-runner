from datetime import datetime, timezone

from flask import Blueprint, g, jsonify, redirect, request
from flask import session as cookie_session
from flask import url_for
from flask_login import login_required, logout_user
from marshmallow import ValidationError
from sdc.crypto.exceptions import InvalidTokenException
from structlog import get_logger
from werkzeug.exceptions import Unauthorized

from app.authentication.authenticator import decrypt_token, store_session
from app.authentication.jti_claim_storage import JtiTokenUsed, use_jti_claim
from app.globals import get_session_store, get_session_timeout_in_seconds
from app.helpers.template_helpers import get_survey_config, render_template
from app.routes.errors import _render_error_page
from app.utilities.metadata_parser import (
    validate_questionnaire_claims,
    validate_runner_claims,
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

    try:
        runner_claims = validate_runner_claims(decrypted_token)
    except ValidationError as e:
        raise InvalidTokenException("Invalid runner claims") from e
    # pylint: disable=assigning-non-slot
    g.schema = load_schema_from_metadata(metadata=runner_claims)
    schema_metadata = g.schema.json["metadata"]

    try:
        questionnaire_claims = validate_questionnaire_claims(
            decrypted_token, schema_metadata
        )
    except ValidationError as e:
        raise InvalidTokenException("Invalid questionnaire claims") from e

    claims = {**runner_claims, **questionnaire_claims}

    schema_name = claims["schema_name"]
    tx_id = claims["tx_id"]
    ru_ref = claims["ru_ref"]
    case_id = claims["case_id"]

    logger.bind(
        schema_name=schema_name,
        tx_id=tx_id,
        ru_ref=ru_ref,
        case_id=case_id,
    )
    logger.info("decrypted token and parsed metadata")

    store_session(claims)

    cookie_session["theme"] = g.schema.json["theme"]
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

    return _render_error_page(200, template="401")


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
