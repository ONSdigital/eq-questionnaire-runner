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

from app.authentication.authenticator import (
    create_session_questionnaire_store,
    decrypt_token,
)
from app.authentication.jti_claim_storage import JtiTokenUsed, use_jti_claim
from app.data_models import QuestionnaireStore
from app.data_models.metadata_proxy import MetadataProxy
from app.globals import get_session_store, get_session_timeout_in_seconds
from app.helpers.metadata_helpers import get_ru_ref_without_check_letter
from app.helpers.template_helpers import (
    DATA_LAYER_KEYS,
    get_survey_config,
    render_template,
)
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.questionnaire.questionnaire_store_updater import QuestionnaireStoreUpdaterBase
from app.questionnaire.router import Router
from app.routes.errors import _render_error_page
from app.services.supplementary_data import get_supplementary_data_v1
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
            "cir_instrument_id": decrypted_token.get("cir_instrument_id"),
            "ru_ref": ru_ref,
            "qid": qid,
        }.items()
        if value
    }
    contextvars.bind_contextvars(**logger_args)

    runner_claims = get_runner_claims(decrypted_token)

    metadata = MetadataProxy.from_dict(runner_claims)

    g.schema = load_schema_from_metadata(
        metadata=metadata, language_code=metadata.language_code
    )
    schema_metadata = g.schema.json["metadata"]

    questionnaire_claims = get_questionnaire_claims(
        decrypted_token=decrypted_token, schema_metadata=schema_metadata
    )

    runner_claims["survey_metadata"]["data"] = questionnaire_claims

    logger.info("decrypted token and parsed metadata")

    with create_session_questionnaire_store(runner_claims) as questionnaire_store:
        _set_questionnaire_supplementary_data(
            questionnaire_store=questionnaire_store, metadata=metadata, schema=g.schema
        )

    cookie_session["expires_in"] = get_session_timeout_in_seconds(g.schema)

    set_schema_context_in_cookie(g.schema)

    if account_service_url := runner_claims.get("account_service_url"):
        cookie_session["account_service_base_url"] = account_service_url

    if runner_claims.get("account_service_log_out_url"):
        cookie_session["account_service_log_out_url"] = runner_claims.get(
            "account_service_log_out_url"
        )  # pragma: no cover

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
    then fetch it, verify any schema supplementary lists are included in the fetched data, and add it to the questionnaire store

    Validation of the supplementary lists must be performed every time a survey launches, not just when the supplementary data is fetched
    as it is possible that the survey has changed but the dataset hasn't so the validity could have changed.
    """
    existing_sds_dataset_id = (
        questionnaire_store.data_stores.metadata.survey_metadata["sds_dataset_id"]
        if questionnaire_store.data_stores.metadata
        and questionnaire_store.data_stores.metadata.survey_metadata
        else None
    )

    if (
        not (new_sds_dataset_id := metadata["sds_dataset_id"])
        or existing_sds_dataset_id == new_sds_dataset_id
    ):
        # no need to fetch: either no supplementary data or it hasn't changed, just validate lists
        _validate_supplementary_data_lists(
            supplementary_data=questionnaire_store.data_stores.supplementary_data_store.raw_data,
            schema=schema,
        )
        return

    identifier = (
        get_ru_ref_without_check_letter(metadata["ru_ref"])
        if metadata["ru_ref"]
        else metadata["qid"]
    )

    supplementary_data = get_supplementary_data_v1(
        # Type ignore: survey_id and either ru_ref or qid are required for schemas that use supplementary data
        dataset_id=new_sds_dataset_id,
        identifier=identifier,  # type: ignore
        survey_id=metadata["survey_id"],  # type: ignore
    )
    logger.info(
        "fetched supplementary data",
        survey_id=metadata["survey_id"],
        sds_dataset_id=new_sds_dataset_id,
    )
    _validate_supplementary_data_lists(
        supplementary_data=supplementary_data["data"], schema=schema
    )
    _set_supplementary_data(
        questionnaire_store=questionnaire_store,
        schema=schema,
        supplementary_data=supplementary_data["data"],
    )


def _set_supplementary_data(
    *,
    questionnaire_store: QuestionnaireStore,
    schema: QuestionnaireSchema,
    supplementary_data: dict,
) -> None:
    """
    Adds the supplementary data to the questionnaire store which:
    1) removes any old list items and answers
    2) Updates block and section progress to reflect any newly unlocked questions due to supplementary data list changes
    """
    router = Router(schema=schema, data_stores=questionnaire_store.data_stores)
    base_questionnaire_store_updater = QuestionnaireStoreUpdaterBase(
        questionnaire_store=questionnaire_store, schema=schema, router=router
    )
    base_questionnaire_store_updater.set_supplementary_data(to_set=supplementary_data)
    base_questionnaire_store_updater.remove_dependent_blocks_and_capture_dependent_sections()
    base_questionnaire_store_updater.update_progress_for_dependent_sections()


def _validate_supplementary_data_lists(
    *, supplementary_data: dict, schema: QuestionnaireSchema
) -> None:
    """
    Validates that any lists the schema requires (which are those in the supplementary_data.lists property)
    are included in the supplementary data
    """
    supplementary_lists = supplementary_data.get("items", {}).keys()
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
    version = decrypted_token.get("version")

    try:
        return validate_runner_claims_v2(decrypted_token)

    except ValidationError as e:
        raise InvalidTokenException(f"Invalid runner claims version: {version}") from e


def get_questionnaire_claims(
    decrypted_token: Mapping, schema_metadata: Iterable[Mapping[str, str]]
) -> dict:
    try:
        claims = decrypted_token.get("survey_metadata", {}).get("data", {})
        return validate_questionnaire_claims(claims, schema_metadata, unknown=INCLUDE)

    except ValidationError as e:
        raise InvalidTokenException("Invalid questionnaire claims") from e
