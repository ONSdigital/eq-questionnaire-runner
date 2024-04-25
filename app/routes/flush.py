from datetime import datetime, timezone
from typing import Iterable, TypeAlias

from flask import Blueprint, Response, current_app, request, session
from sdc.crypto.decrypter import decrypt
from sdc.crypto.encrypter import encrypt
from sdc.crypto.key_store import KeyStore
from structlog import contextvars, get_logger

from app.authentication.user import User
from app.authentication.user_id_generator import UserIDGenerator
from app.data_models import QuestionnaireStore
from app.data_models.metadata_proxy import MetadataProxy
from app.globals import get_metadata, get_questionnaire_store
from app.keys import KEY_PURPOSE_AUTHENTICATION, KEY_PURPOSE_SUBMISSION
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.router import Router
from app.questionnaire.routing_path import RoutingPath
from app.submitter import GCSSubmitter, LogSubmitter, RabbitMQSubmitter
from app.submitter.converter_v2 import convert_answers_v2
from app.submitter.submission_failed import SubmissionFailedException
from app.utilities.bind_context import bind_contextvars_schema_from_metadata
from app.utilities.json import json_dumps
from app.utilities.schema import load_schema_from_metadata
from app.views.handlers.submission import get_receipting_metadata

flush_blueprint = Blueprint("flush", __name__)

logger = get_logger()

Submitter: TypeAlias = GCSSubmitter | LogSubmitter | RabbitMQSubmitter


@flush_blueprint.route("/flush", methods=["POST"])
def flush_data() -> Response:
    if session:
        session.clear()

    encrypted_token = request.args.get("token")

    if not encrypted_token or encrypted_token is None:
        return Response(status=403)

    decrypted_token = decrypt(
        token=encrypted_token,
        key_store=_get_keystore(),
        key_purpose=KEY_PURPOSE_AUTHENTICATION,
        leeway=current_app.config["EQ_JWT_LEEWAY_IN_SECONDS"],
    )

    roles = decrypted_token.get("roles")

    if roles and "flusher" in roles:
        user = _get_user(decrypted_token["response_id"])

        if metadata := get_metadata(user):
            contextvars.bind_contextvars(
                tx_id=metadata.tx_id,
                ce_id=metadata.collection_exercise_sid,
            )
            bind_contextvars_schema_from_metadata(metadata)

        if _submit_data(user):
            return Response(status=200)
        return Response(status=404)
    return Response(status=403)


def _submit_data(user: User) -> bool:
    questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)

    if questionnaire_store and questionnaire_store.data_stores.answer_store:
        # Type ignore: The presence of an answer_store implicitly verifies that there must be metadata populated and thus can safely be used non-optionally.
        metadata: MetadataProxy = questionnaire_store.data_stores.metadata  # type: ignore
        submitted_at = datetime.now(timezone.utc)
        schema = load_schema_from_metadata(
            metadata=metadata, language_code=metadata.language_code
        )

        router = Router(
            schema=schema,
            data_stores=questionnaire_store.data_stores,
        )
        full_routing_path = router.full_routing_path()

        message: str = _get_converted_answers_message(
            full_routing_path=full_routing_path,
            questionnaire_store=questionnaire_store,
            schema=schema,
            submitted_at=submitted_at,
        )

        encrypted_message = encrypt(message, _get_keystore(), KEY_PURPOSE_SUBMISSION)

        additional_metadata = get_receipting_metadata(metadata)

        # Type ignore: Instance attribute 'eq' is a dict with key "submitter" with value of type GCSSubmitter, LogSubmitter or RabbitMQSubmitter
        submitter: Submitter = current_app.eq["submitter"]  # type: ignore

        sent = submitter.send_message(
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
    full_routing_path: Iterable[RoutingPath],
    questionnaire_store: QuestionnaireStore,
    schema: QuestionnaireSchema,
    submitted_at: datetime,
) -> str:
    """
    This gets converted answer message based on the selected version, currently only v2 is supported so `app.submitter.converter_v2.convert_answers_v2` is used
    Returns:
        object: str
    """
    return json_dumps(
        convert_answers_v2(
            schema=schema,
            questionnaire_store=questionnaire_store,
            full_routing_path=full_routing_path,
            submitted_at=submitted_at,
            flushed=True,
        )
    )


def _get_user(response_id: str) -> User:
    # Type ignore: Instance attribute 'eq' is a dict with key "id_generator" with value of type UserIDGenerator
    id_generator: UserIDGenerator = current_app.eq["id_generator"]  # type: ignore
    user_id = id_generator.generate_id(response_id)
    user_ik = id_generator.generate_ik(response_id)
    return User(user_id, user_ik)


def _get_keystore() -> KeyStore:
    # Type ignore: Instance attribute 'eq' is a dict with key "key_store" with value of type KeyStore
    key_store: KeyStore = current_app.eq["key_store"]  # type: ignore
    return key_store
