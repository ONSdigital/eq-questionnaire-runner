from datetime import datetime, timezone

from flask import Blueprint, Response, current_app, request, session
from sdc.crypto.decrypter import decrypt
from sdc.crypto.encrypter import encrypt
from structlog import contextvars, get_logger

from app.authentication.auth_payload_version import AuthPayloadVersion
from app.authentication.user import User
from app.data_models import QuestionnaireStore
from app.data_models.metadata_proxy import MetadataProxy
from app.globals import get_answer_store, get_metadata, get_questionnaire_store
from app.keys import KEY_PURPOSE_AUTHENTICATION, KEY_PURPOSE_SUBMISSION
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.router import Router
from app.questionnaire.routing_path import RoutingPath
from app.submitter.converter import convert_answers
from app.submitter.converter_v2 import convert_answers_v2
from app.submitter.submission_failed import SubmissionFailedException
from app.utilities.json import json_dumps
from app.utilities.schema import load_schema_from_metadata
from app.views.handlers.submission import get_receipting_metadata

flush_blueprint = Blueprint("flush", __name__)

logger = get_logger()


@flush_blueprint.route("/flush", methods=["POST"])
def flush_data():
    if session:
        session.clear()

    encrypted_token = request.args.get("token")

    if not encrypted_token or encrypted_token is None:
        return Response(status=403)

    decrypted_token = decrypt(
        token=encrypted_token,
        key_store=current_app.eq["key_store"],
        key_purpose=KEY_PURPOSE_AUTHENTICATION,
        leeway=current_app.config["EQ_JWT_LEEWAY_IN_SECONDS"],
    )

    roles = decrypted_token.get("roles")

    if roles and "flusher" in roles:
        user = _get_user(decrypted_token["response_id"])

        if metadata := get_metadata(user):
            contextvars.bind_contextvars(tx_id=metadata.tx_id)
        if _submit_data(user):
            return Response(status=200)
        return Response(status=404)
    return Response(status=403)


def _submit_data(user):
    answer_store = get_answer_store(user)

    if answer_store:
        questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
        answer_store = questionnaire_store.answer_store
        metadata = questionnaire_store.metadata
        response_metadata = questionnaire_store.response_metadata
        progress_store = questionnaire_store.progress_store
        list_store = questionnaire_store.list_store
        submitted_at = datetime.now(timezone.utc)
        schema = load_schema_from_metadata(
            metadata=metadata, language_code=metadata.language_code
        )

        router = Router(
            schema,
            answer_store,
            list_store,
            progress_store,
            metadata,
            response_metadata,
        )
        full_routing_path = router.full_routing_path()

        message: str = _get_converted_answers_message(
            full_routing_path, metadata, questionnaire_store, schema, submitted_at
        )

        encrypted_message = encrypt(
            message, current_app.eq["key_store"], KEY_PURPOSE_SUBMISSION
        )

        additional_metadata = get_receipting_metadata(metadata)

        sent = current_app.eq["submitter"].send_message(
            encrypted_message,
            tx_id=metadata.tx_id,
            case_id=metadata.case_id,
            **additional_metadata,
        )

        if not sent:
            raise SubmissionFailedException()

        get_questionnaire_store(user.user_id, user.user_ik).delete()
        logger.info("successfully flushed answers")
        return True

    logger.info("no answers found to flush")
    return False


def _get_converted_answers_message(
    full_routing_path: RoutingPath,
    metadata: MetadataProxy,
    questionnaire_store: QuestionnaireStore,
    schema: QuestionnaireSchema,
    submitted_at: datetime,
) -> str:
    """
    This gets converted answer message based on the selected version.
    For version 1 `app.submitter.converter.convert_answers` is used whereas for version 2 `app.submitter.converter_v2.convert_answers_v2` is used
    Returns:
        object: str
    """
    answer_converter = (
        convert_answers_v2
        if metadata.version is AuthPayloadVersion.V2
        else convert_answers
    )
    return json_dumps(
        answer_converter(
            schema,
            questionnaire_store,
            full_routing_path,
            submitted_at,
            flushed=True,
        )
    )


def _get_user(response_id):
    id_generator = current_app.eq["id_generator"]
    user_id = id_generator.generate_id(response_id)
    user_ik = id_generator.generate_ik(response_id)
    return User(user_id, user_ik)
