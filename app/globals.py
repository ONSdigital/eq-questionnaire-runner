from datetime import datetime, timedelta
from types import MappingProxyType
from typing import Union

from dateutil.tz import tzutc
from flask import current_app, g
from flask import session as cookie_session
from structlog import get_logger

from app.authentication.user import User
from app.data_models import QuestionnaireStore
from app.data_models.answer_store import AnswerStore
from app.data_models.session_store import SessionStore
from app.questionnaire import QuestionnaireSchema
from app.settings import EQ_SESSION_ID, USER_IK
from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage

logger = get_logger()


def get_questionnaire_store(user_id: str, user_ik: str) -> QuestionnaireStore:
    # Sets up a single QuestionnaireStore instance per request.
    store = g.get("_questionnaire_store")
    if store is None:
        secret_store = current_app.eq["secret_store"]  # type: ignore
        pepper = secret_store.get_secret_by_name(
            "EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER"
        )
        storage = EncryptedQuestionnaireStorage(user_id, user_ik, pepper)
        # pylint: disable=assigning-non-slot
        store = g._questionnaire_store = QuestionnaireStore(storage)

    return store


def get_session_store() -> Union[SessionStore, None]:
    if USER_IK not in cookie_session or EQ_SESSION_ID not in cookie_session:
        return None

    # Sets up a single SessionStore instance per request context.
    store = g.get("_session_store")

    if store is None:
        secret_store = current_app.eq["secret_store"]  # type: ignore
        pepper = secret_store.get_secret_by_name(
            "EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER"
        )
        # pylint: disable=assigning-non-slot
        store = g._session_store = SessionStore(
            cookie_session[USER_IK], pepper, cookie_session[EQ_SESSION_ID]
        )

    return store if store.session_data else None


def get_session_timeout_in_seconds(schema: QuestionnaireSchema) -> int:
    """
    Gets the session timeout in seconds from the schema/env variable.
    :return: Timeout in seconds
    """
    default_session_timeout = current_app.config["EQ_SESSION_TIMEOUT_SECONDS"]
    schema_session_timeout = schema.json.get("session_timeout_in_seconds")
    timeout = (
        schema_session_timeout
        if schema_session_timeout and schema_session_timeout < default_session_timeout
        else default_session_timeout
    )

    return timeout


def create_session_store(
    eq_session_id: str, user_id: str, user_ik: str, session_data: str
) -> None:
    secret_store = current_app.eq["secret_store"]  # type: ignore
    pepper = secret_store.get_secret_by_name(
        "EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER"
    )
    session_timeout_in_seconds = get_session_timeout_in_seconds(g.schema)
    expires_at = datetime.now(tz=tzutc()) + timedelta(
        seconds=session_timeout_in_seconds
    )

    # pylint: disable=protected-access, assigning-non-slot
    g._session_store = (
        SessionStore(user_ik, pepper)
        .create(eq_session_id, user_id, session_data, expires_at)
        .save()
    )


def get_metadata(user: User) -> Union[None, MappingProxyType]:
    if user.is_anonymous:
        logger.debug("anonymous user requesting metadata get instance")
        return None

    questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
    return questionnaire_store.metadata


def get_answer_store(user: User) -> AnswerStore:
    questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
    return questionnaire_store.answer_store
