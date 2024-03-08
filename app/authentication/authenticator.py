from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from typing import Any, Generator, Mapping, MutableMapping, Optional
from uuid import uuid4

from blinker import ANY
from flask import Flask, Request, current_app
from flask import session as cookie_session
from flask_login import LoginManager, user_logged_out
from sdc.crypto.decrypter import decrypt
from structlog import contextvars, get_logger

from app.authentication.no_token_exception import NoTokenException
from app.authentication.user import User
from app.data_models import QuestionnaireStore
from app.data_models.session_data import SessionData
from app.data_models.session_store import SessionStore
from app.globals import (
    create_session_store,
    get_metadata,
    get_questionnaire_store,
    get_session_store,
)
from app.keys import KEY_PURPOSE_AUTHENTICATION
from app.settings import EQ_SESSION_ID, USER_IK

logger = get_logger()

login_manager = LoginManager()


@login_manager.user_loader
def user_loader(user_id: str) -> Optional[str]:
    logger.debug("loading user", user_id=user_id)
    return load_user()


@login_manager.request_loader
def request_load_user(
    request: Request,
) -> Optional[User]:
    logger.debug("load user")

    extend_session = not (
        request.endpoint == "session.session_expiry" and request.method == "GET"
    )

    return load_user(extend_session=extend_session)


@user_logged_out.connect_via(ANY)
def when_user_logged_out(
    sender_app: Flask, user: str  # pylint: disable=unused-argument
) -> None:
    logger.debug("log out user")
    session_store = get_session_store()
    if session_store:
        session_store.delete()
    cookie_session.pop(USER_IK, None)


def _extend_session_expiry(session_store: SessionStore) -> None:
    """
    Extends the expiration time of the session
    :param session_store:
    """
    session_timeout = cookie_session.get("expires_in")
    if session_timeout:
        new_expiration_time = datetime.now(tz=timezone.utc) + timedelta(
            seconds=session_timeout
        )

        # Only update expiry time if its greater than 60s different to what is currently set
        if (
            not session_store.expiration_time
            or (new_expiration_time - session_store.expiration_time).total_seconds()
            > 60
        ):
            session_store.expiration_time = new_expiration_time
            session_store.save()
            logger.debug("session expiry extended")


def _is_session_valid(session_store: SessionStore) -> bool:
    """
    Checks that the user's session has not expired
    :param session_store:
    :return: True if the session is valid else False
    """

    return (
        not session_store.expiration_time
        or session_store.expiration_time >= datetime.now(tz=timezone.utc)
    )


def load_user(extend_session: bool = True) -> Optional[User]:
    """
    Checks for the present of the JWT in the users sessions
    :return: A user object if a JWT token is available in the session

    :param extend_session: bool, whether to extend the session
    """
    session_store = get_session_store()

    if session_store and _is_session_valid(session_store):
        logger.debug("session exists")

        user_id = session_store.user_id
        user_ik = cookie_session.get(USER_IK)
        user = User(user_id, user_ik)

        if metadata := get_metadata(user):
            contextvars.bind_contextvars(tx_id=metadata.tx_id)

        if extend_session:
            _extend_session_expiry(session_store)

        return user

    logger.info(
        "session does not exist",
        user_ik_present=USER_IK in cookie_session,
        eq_session_id_present=EQ_SESSION_ID in cookie_session,
        session_store_exists=bool(session_store),
        session_expiration=(
            session_store.expiration_time.isoformat()
            if session_store and session_store.expiration_time
            else None
        ),
    )

    cookie_session.pop(USER_IK, None)


def _create_session_data_from_metadata(metadata: Mapping[str, Any]) -> SessionData:
    """
    Creates a SessionData object from metadata
    :param metadata: metadata parsed from jwt token
    """

    return SessionData(
        language_code=metadata.get("language_code"),
    )


@contextmanager
def create_session_questionnaire_store(
    metadata: MutableMapping,
) -> Generator[QuestionnaireStore, None, None]:
    """
    Context to manage creating and saving new session and questionnaire store
    :param metadata: metadata parsed from jwt token
    """
    # also clear the secure cookie data
    cookie_session.clear()

    # get the hashed user id for eq
    id_generator = current_app.eq["id_generator"]  # type: ignore
    user_id = id_generator.generate_id(metadata["response_id"])
    user_ik = id_generator.generate_ik(metadata["response_id"])

    eq_session_id = str(uuid4())

    # store the user ik and es_session_id in the cookie
    cookie_session[USER_IK] = user_ik
    cookie_session[EQ_SESSION_ID] = eq_session_id

    session_data = _create_session_data_from_metadata(metadata)
    create_session_store(eq_session_id, user_id, user_ik, session_data)

    questionnaire_store = get_questionnaire_store(user_id, user_ik)
    yield questionnaire_store
    questionnaire_store.set_metadata(metadata)
    questionnaire_store.save()

    logger.info("user authenticated")


def decrypt_token(encrypted_token: str | None) -> dict[str, Any]:
    if not encrypted_token:
        raise NoTokenException("Please provide a token")

    logger.debug("decrypting token")
    decrypted_token: dict[str, Any] = decrypt(
        token=encrypted_token,
        key_store=current_app.eq["key_store"],  # type: ignore
        key_purpose=KEY_PURPOSE_AUTHENTICATION,
        leeway=current_app.config["EQ_JWT_LEEWAY_IN_SECONDS"],
    )

    logger.debug("token decrypted")
    return decrypted_token
