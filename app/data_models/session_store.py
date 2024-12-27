from __future__ import annotations

from datetime import datetime

from flask import current_app
from jwcrypto.common import base64url_decode
from structlog import get_logger

from app.data_models.app_models import EQSession
from app.data_models.session_data import SessionData
from app.storage.storage_encryption import StorageEncryption
from app.utilities.json import json_loads

logger = get_logger()


class SessionStore:
    def __init__(
        self, user_ik: str, pepper: str, eq_session_id: str | None = None
    ) -> None:
        self.eq_session_id = eq_session_id
        self.user_id: str | None = None
        self.user_ik = user_ik
        self.session_data: SessionData | None = None
        self._eq_session: EQSession | None = None
        self.pepper = pepper
        if eq_session_id:
            self._load()

    @property
    def expiration_time(self) -> datetime | None:
        """
        Checking if expires_at is available can be removed soon after deployment,
        it is only needed to cater for in-flight sessions.
        """
        if self._eq_session and self._eq_session.expires_at:
            return self._eq_session.expires_at

    @expiration_time.setter
    def expiration_time(self, expires_at: datetime) -> None:
        """
        Checking if expires_at is available can be removed soon after deployment,
        it is only needed to cater for in-flight sessions.
        """
        if self._eq_session and self._eq_session.expires_at:
            self._eq_session.expires_at = expires_at

    def create(
        self,
        eq_session_id: str,
        user_id: str,
        session_data: SessionData,
        expires_at: datetime,
    ) -> SessionStore:
        """
        Create a new eq_session and associate it with the user_id specified
        """
        self.eq_session_id = eq_session_id
        self.user_id = user_id
        self.session_data = session_data
        self._eq_session = EQSession(
            eq_session_id=self.eq_session_id,
            user_id=self.user_id,
            expires_at=expires_at,
            session_data=None,
        )

        return self

    def save(self) -> SessionStore:
        """
        save session
        """
        if self._eq_session:
            self._eq_session.session_data = StorageEncryption(
                self.user_id, self.user_ik, self.pepper
            ).encrypt_data(vars(self.session_data))

            current_app.eq["storage"].put(self._eq_session, overwrite=True)  # type: ignore

        return self

    def delete(self) -> None:
        """
        deletes user session from database
        """
        if self._eq_session:
            current_app.eq["storage"].delete(self._eq_session)  # type: ignore

            self._eq_session = None
            self.eq_session_id = None
            self.user_id = None
            self.session_data = None

    def _load(self) -> None:
        logger.debug(
            "finding eq_session_id in database", eq_session_id=self.eq_session_id
        )
        self._eq_session: EQSession | None = current_app.eq["storage"].get(EQSession, self.eq_session_id)  # type: ignore

        if self._eq_session and self._eq_session.session_data:
            self.user_id = self._eq_session.user_id

            encrypted_session_data = self._eq_session.session_data
            session_data_as_bytes = StorageEncryption(
                self.user_id, self.user_ik, self.pepper
            ).decrypt_data(encrypted_session_data)

            session_data_as_str = session_data_as_bytes.decode()
            # for backwards compatibility
            # session data used to be base64 encoded before encryption
            try:
                session_data_as_str = base64url_decode(session_data_as_str).decode()
            except ValueError:
                pass

            self.session_data = json_loads(
                session_data_as_str, object_hook=lambda d: SessionData(**d)
            )

            logger.debug(
                "found matching eq_session for eq_session_id in database",
                session_id=self._eq_session.eq_session_id,
                user_id=self._eq_session.user_id,
            )
        else:
            logger.debug(
                "eq_session_id not found in database", eq_session_id=self.eq_session_id
            )
