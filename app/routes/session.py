import json
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

import requests
from flask import Blueprint, g, jsonify, redirect, request
from flask import session as cookie_session
from flask import url_for
from flask_login import login_required, logout_user
from marshmallow import INCLUDE, ValidationError
from requests import RequestException
from requests.adapters import HTTPAdapter, Retry
from sdc.crypto.exceptions import InvalidTokenException
from structlog import contextvars, get_logger
from werkzeug.exceptions import Unauthorized
from werkzeug.wrappers.response import Response

from app.authentication.auth_payload_versions import AuthPayloadVersion
from app.authentication.authenticator import decrypt_token, store_session
from app.authentication.jti_claim_storage import JtiTokenUsed, use_jti_claim
from app.data_models.metadata_proxy import MetadataProxy
from app.globals import get_session_store, get_session_timeout_in_seconds
from app.helpers.template_helpers import (
    DATA_LAYER_KEYS,
    get_survey_config,
    render_template,
)
from app.questionnaire import QuestionnaireSchema
from app.routes.errors import _render_error_page
from app.utilities.metadata_parser import validate_runner_claims
from app.utilities.metadata_parser_v2 import (
    validate_questionnaire_claims,
    validate_runner_claims_v2,
)
from app.utilities.prepop_parser import validate_prepop_data_v1
from app.utilities.schema import load_schema_from_metadata

logger = get_logger()

session_blueprint = Blueprint("session", __name__)

PREPOP_URL = ""
PREPOP_REQUEST_MAX_BACKOFF = 0.2
PREPOP_REQUEST_MAX_RETRIES = 2  # Totals no. of request should be 3. The initial request + PREPOP_REQUEST_MAX_RETRIES
PREPOP_REQUEST_TIMEOUT = 3
PREPOP_REQUEST_RETRY_STATUS_CODES = [
    408,
    429,
    500,
    502,
    503,
    504,
]


class PrepopRequestFailed(Exception):
    def __str__(self) -> str:
        return "Prepop request failed"


@session_blueprint.after_request
def add_cache_control(response: Response) -> Response:
    response.cache_control.no_cache = True
    return response


@session_blueprint.route("/session", methods=["HEAD"])
def login_head() -> tuple[str, int]:
    return "", 204


def set_schema_context_in_cookie(schema: QuestionnaireSchema) -> None:
    for key in [*DATA_LAYER_KEYS, "theme"]:
        if value := schema.json.get(key):
            cookie_session[key] = value


@session_blueprint.route("/session", methods=["GET", "POST"])
def login() -> Response:
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
    g.schema = load_schema_from_metadata(
        metadata=metadata, language_code=metadata.language_code
    )
    schema_metadata = g.schema.json["metadata"]

    questionnaire_claims = get_questionnaire_claims(
        decrypted_token=decrypted_token, schema_metadata=schema_metadata
    )

    if metadata.version is AuthPayloadVersion.V2:
        if questionnaire_claims:
            runner_claims["survey_metadata"]["data"] = questionnaire_claims

        ru_ref = questionnaire_claims.get("ru_ref")
        qid = questionnaire_claims.get("qid")
        claims = runner_claims
    else:
        ru_ref = runner_claims["ru_ref"]
        qid = None
        claims = {**runner_claims, **questionnaire_claims}

    tx_id = claims["tx_id"]
    case_id = claims["case_id"]

    logger_args = {
        key: value
        for key, value in {
            "tx_id": tx_id,
            "case_id": case_id,
            "schema_name": metadata.schema_name,
            "schema_url": metadata.schema_url,
            "ru_ref": ru_ref,
            "qid": qid,
        }.items()
        if value
    }
    contextvars.bind_contextvars(**logger_args)

    logger.info("decrypted token and parsed metadata")

    store_session(claims)

    cookie_session["expires_in"] = get_session_timeout_in_seconds(g.schema)

    set_schema_context_in_cookie(g.schema)

    if account_service_url := claims.get("account_service_url"):
        cookie_session["account_service_base_url"] = account_service_url

    if claims.get("account_service_log_out_url"):
        cookie_session["account_service_log_out_url"] = claims.get(  # pragma: no cover
            "account_service_log_out_url"
        )

    cookie_session["language_code"] = metadata.language_code

    if (dataset_id := metadata["sds_dataset_id"]) and ru_ref:
        get_prepop_data(prepop_url=PREPOP_URL, dataset_id=dataset_id, ru_ref=ru_ref)

    return redirect(url_for("questionnaire.get_questionnaire"))


def get_prepop_data(prepop_url: str, dataset_id: str, ru_ref: str) -> dict:
    constructed_prepop_url = f"{prepop_url}?dataset_id={dataset_id}&unit_id={ru_ref}"

    session = requests.Session()

    retries = Retry(
        total=PREPOP_REQUEST_MAX_RETRIES,
        status_forcelist=PREPOP_REQUEST_RETRY_STATUS_CODES,
    )  # Codes to retry according to Google Docs https://cloud.google.com/storage/docs/retry-strategy#client-libraries

    # Type ignore: MyPy does not recognise BACKOFF_MAX however it is a property, albeit deprecated
    retries.BACKOFF_MAX = PREPOP_REQUEST_MAX_BACKOFF  # type: ignore

    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("https://", HTTPAdapter(max_retries=retries))

    try:
        response = session.get(constructed_prepop_url, timeout=PREPOP_REQUEST_TIMEOUT)
    except RequestException as exc:
        logger.exception(
            "Error requesting prepopulated data",
            prepop_url=constructed_prepop_url,
        )
        raise PrepopRequestFailed from exc

    if response.status_code == 200:
        prepop_response_content = response.content.decode()
        prepop_data = json.loads(prepop_response_content)

        return validate_prepop_data(
            prepop_data=prepop_data, dataset_id=dataset_id, ru_ref=ru_ref
        )

    logger.error(
        "got a non-200 response for prepop data request",
        status_code=response.status_code,
        schema_url=constructed_prepop_url,
    )

    raise PrepopRequestFailed


def validate_prepop_data(prepop_data: Mapping, dataset_id: str, ru_ref: str) -> dict:
    try:
        return validate_prepop_data_v1(
            prepop_data=prepop_data, dataset_id=dataset_id, ru_ref=ru_ref
        )
    except ValidationError as e:
        raise ValidationError("Invalid prepopulation data") from e


def validate_jti(decrypted_token: dict[str, str | list | int]) -> None:
    # Type ignore: decrypted_token["exp"] will return a valid timestamp with compatible typing
    expires_at = datetime.fromtimestamp(decrypted_token["exp"], tz=timezone.utc)  # type: ignore
    jwt_expired = expires_at < datetime.now(tz=timezone.utc)
    if jwt_expired:
        raise Unauthorized

    jti_claim = decrypted_token.get("jti")
    try:
        # Type ignore: decrypted_token.get("jti") will return a valid JTI with compatible typing
        use_jti_claim(jti_claim, expires_at)  # type: ignore
    except JtiTokenUsed as e:
        raise Unauthorized from e
    except (TypeError, ValueError) as e:
        raise InvalidTokenException from e


@session_blueprint.route("/session-expired", methods=["GET"])
def get_session_expired() -> tuple[str, int]:
    # Check for GET as we don't want to log out for HEAD requests
    if request.method == "GET":
        logout_user()

    return _render_error_page(200, template="401")


@session_blueprint.route("/session-expiry", methods=["GET", "PATCH"])
@login_required
def session_expiry() -> Response:
    # Type ignore: @login_required endpoint will ensure a session store exists
    return jsonify(expires_at=get_session_store().expiration_time.isoformat())  # type: ignore


@session_blueprint.route("/sign-out", methods=["GET"])
def get_sign_out() -> Response:
    """
    Signs the user out of eQ and redirects to the log out url.
    """
    survey_config = get_survey_config()
    log_out_url = None
    if "internal_redirect" in request.args:
        log_out_url = url_for("session.get_signed_out")
    elif "todo" in request.args:
        log_out_url = survey_config.account_service_todo_url

    if not log_out_url:
        log_out_url = survey_config.account_service_log_out_url

    # Check for GET as we don't want to log out for HEAD requests
    if request.method == "GET":
        logout_user()

    # Type ignore: Logic above to set log_out_url ensures it is not None
    return redirect(log_out_url)  # type: ignore


@session_blueprint.route("/signed-out", methods=["GET"])
def get_signed_out() -> Response | str:
    if not cookie_session:
        return redirect(url_for("session.get_session_expired"))

    survey_config = get_survey_config()
    redirect_url = (
        survey_config.account_service_todo_url
        or survey_config.account_service_log_out_url
    )
    return render_template(
        template="signed-out",
        redirect_url=redirect_url,
    )


def get_runner_claims(decrypted_token: Mapping[str, Any]) -> dict:
    try:
        if version := decrypted_token.get("version"):
            if version == AuthPayloadVersion.V2.value:
                return validate_runner_claims_v2(decrypted_token)

            raise InvalidTokenException(f"Invalid runner claims version: {version}")

        return validate_runner_claims(decrypted_token)
    except ValidationError as e:
        raise InvalidTokenException("Invalid runner claims") from e


def get_questionnaire_claims(
    decrypted_token: Mapping, schema_metadata: Iterable[Mapping[str, str]]
) -> dict:
    try:
        if decrypted_token.get("version") == AuthPayloadVersion.V2.value:
            claims = decrypted_token.get("survey_metadata", {}).get("data", {})
            return validate_questionnaire_claims(
                claims, schema_metadata, unknown=INCLUDE
            )

        return validate_questionnaire_claims(decrypted_token, schema_metadata)

    except ValidationError as e:
        raise InvalidTokenException("Invalid questionnaire claims") from e
