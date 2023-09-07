from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

from flask import Blueprint, g, jsonify, redirect, request
from flask import session as cookie_session
from flask import url_for
from flask_login import login_required, logout_user
from marshmallow import INCLUDE, ValidationError
from sdc.crypto.exceptions import InvalidTokenException
from structlog import contextvars, get_logger
from werkzeug.exceptions import Unauthorized
from werkzeug.wrappers.response import Response

from app.authentication.auth_payload_versions import AuthPayloadVersion
from app.authentication.authenticator import (
    create_session_questionnaire_store,
    decrypt_token,
)
from app.authentication.jti_claim_storage import JtiTokenUsed, use_jti_claim
from app.data_models import QuestionnaireStore
from app.data_models.metadata_proxy import MetadataProxy
from app.globals import get_session_store, get_session_timeout_in_seconds
from app.helpers.template_helpers import (
    DATA_LAYER_KEYS,
    get_survey_config,
    render_template,
)
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.routes.errors import _render_error_page
from app.services.supplementary_data import get_supplementary_data_v1
from app.utilities.metadata_parser import validate_runner_claims
from app.utilities.metadata_parser_v2 import (
    validate_questionnaire_claims,
    validate_runner_claims_v2,
)
from app.utilities.schema import load_schema_from_metadata

logger = get_logger()

session_blueprint = Blueprint("session", __name__)


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

    _data = (
        survey_metadata.get("data", {})
        if (survey_metadata := decrypted_token.get("survey_metadata"))
        else decrypted_token
    )
    ru_ref, qid = _data.get("ru_ref"), _data.get("qid")

    logger_args = {
        key: value
        for key, value in {
            "tx_id": decrypted_token.get("tx_id"),
            "case_id": decrypted_token.get("case_id"),
            "schema_name": decrypted_token.get("schema_name"),
            "schema_url": decrypted_token.get("schema_url"),
            "ru_ref": ru_ref,
            "qid": qid,
        }.items()
        if value
    }
    contextvars.bind_contextvars(**logger_args)

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

        claims = runner_claims
    else:
        claims = {**runner_claims, **questionnaire_claims}

    logger.info("decrypted token and parsed metadata")

    with create_session_questionnaire_store(claims) as questionnaire_store:
        _set_questionnaire_supplementary_data(
            questionnaire_store=questionnaire_store, metadata=metadata, schema=g.schema
        )

    cookie_session["expires_in"] = get_session_timeout_in_seconds(g.schema)

    set_schema_context_in_cookie(g.schema)

    if account_service_url := claims.get("account_service_url"):
        cookie_session["account_service_base_url"] = account_service_url

    if claims.get("account_service_log_out_url"):
        cookie_session["account_service_log_out_url"] = claims.get(  # pragma: no cover
            "account_service_log_out_url"
        )

    cookie_session["language_code"] = metadata.language_code or DEFAULT_LANGUAGE_CODE

    return redirect(url_for("questionnaire.get_questionnaire"))


def _set_questionnaire_supplementary_data(
    *,
    questionnaire_store: QuestionnaireStore,
    metadata: MetadataProxy,
    schema: QuestionnaireSchema,
) -> None:
    """
    If the survey metadata has an sds dataset id, and it either doesn't match what it stored, or there is no stored supplementary data
    then fetch it and add it to the store
    This includes verification that the supplementary data lists cover any schema dependent lists which aren't populated by a list collector
    """
    if not (new_sds_dataset_id := metadata["sds_dataset_id"]):
        return

    existing_sds_dataset_id = (
        questionnaire_store.metadata.survey_metadata["sds_dataset_id"]
        if questionnaire_store.metadata and questionnaire_store.metadata.survey_metadata
        else None
    )

    if existing_sds_dataset_id == new_sds_dataset_id:
        # no need to fetch again
        return

    supplementary_data = get_supplementary_data_v1(
        # Type ignore: survey_id and either ru_ref or qid are required for schemas that use supplementary data
        dataset_id=new_sds_dataset_id,
        identifier=metadata["ru_ref"] or metadata["qid"],  # type: ignore
        survey_id=metadata["survey_id"],  # type: ignore
    )
    logger.info(
        "fetched supplementary data",
        survey_id=metadata["survey_id"],
        sds_dataset_id=new_sds_dataset_id,
    )
    # ensure any required lists for the schema are included in the supplementary data
    _validate_supplementary_data_lists(
        supplementary_data=supplementary_data, schema=schema
    )
    questionnaire_store.set_supplementary_data(supplementary_data["data"])


def _validate_supplementary_data_lists(
    *, supplementary_data: dict, schema: QuestionnaireSchema
) -> None:
    """
    Validates that any lists the schema requires (which are those in the supplementary_data.lists property)
    are included in the supplementary data
    """
    supplementary_lists = set(supplementary_data["data"].get("items", {}).keys())
    if missing := schema.supplementary_lists - supplementary_lists:
        raise ValidationError(
            f"Supplementary data does not include the following lists required for the schema: {', '.join(missing)}"
        )


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
