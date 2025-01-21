from datetime import datetime

import snappy
from flask import current_app
from structlog import get_logger

from app.data_models import QuestionnaireStore
from app.data_models.app_models import QuestionnaireState
from app.storage.storage_encryption import StorageEncryption

logger = get_logger()


class EncryptedQuestionnaireStorage:
    def __init__(self, user_id: str, user_ik: str, pepper: str) -> None:
        self._user_id = user_id
        self.encrypter = StorageEncryption(user_id, user_ik, pepper)

    def save(
        self,
        data: str,
        collection_exercise_sid: str,
        submitted_at: datetime | None = None,
        expires_at: datetime | None = None,
    ) -> None:
        compressed_data = snappy.compress(data)
        encrypted_data = self.encrypter.encrypt_data(compressed_data)
        questionnaire_state = QuestionnaireState(
            self._user_id,
            encrypted_data,
            collection_exercise_sid,
            QuestionnaireStore.LATEST_VERSION,
            submitted_at,
            expires_at,
        )

        current_app.eq["storage"].put(questionnaire_state)  # type: ignore

    def get_user_data(
        self,
    ) -> tuple[None, None, None, None] | tuple[str, str, int, datetime | None]:
        questionnaire_state = self._find_questionnaire_state()
        if questionnaire_state and questionnaire_state.state_data:
            version = questionnaire_state.version
            submitted_at = questionnaire_state.submitted_at
            collection_exercise_sid = questionnaire_state.collection_exercise_sid
            decrypted_data = self._get_snappy_compressed_data(
                questionnaire_state.state_data
            )
            return decrypted_data, collection_exercise_sid, version, submitted_at

        return None, None, None, None

    def delete(self) -> None:
        logger.debug("deleting users data", user_id=self._user_id)
        questionnaire_state = self._find_questionnaire_state()
        if questionnaire_state:
            current_app.eq["storage"].delete(questionnaire_state)  # type: ignore

    def _find_questionnaire_state(self) -> QuestionnaireState | None:
        logger.debug("getting questionnaire data", user_id=self._user_id)
        state: QuestionnaireState = current_app.eq["storage"].get(QuestionnaireState, self._user_id)  # type: ignore
        return state

    def _get_snappy_compressed_data(self, data: str) -> str:
        decrypted_data = self.encrypter.decrypt_data(data)
        uncompressed_data: str = snappy.uncompress(decrypted_data).decode()
        return uncompressed_data
