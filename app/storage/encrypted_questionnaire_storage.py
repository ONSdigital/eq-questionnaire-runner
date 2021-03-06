import snappy
from flask import current_app
from structlog import get_logger

from app.data_models import QuestionnaireStore
from app.data_models.app_models import QuestionnaireState
from app.storage.storage_encryption import StorageEncryption

logger = get_logger()


class EncryptedQuestionnaireStorage:
    def __init__(self, user_id, user_ik, pepper):
        self._user_id = user_id
        self.encrypter = StorageEncryption(user_id, user_ik, pepper)

    def save(self, data):
        compressed_data = snappy.compress(data)
        encrypted_data = self.encrypter.encrypt_data(compressed_data)
        questionnaire_state = QuestionnaireState(
            self._user_id, encrypted_data, QuestionnaireStore.LATEST_VERSION
        )

        current_app.eq["storage"].put(questionnaire_state)

    def get_user_data(self):
        questionnaire_state = self._find_questionnaire_state()
        if questionnaire_state and questionnaire_state.state_data:
            version = questionnaire_state.version
            decrypted_data = self._get_snappy_compressed_data(
                questionnaire_state.state_data
            )
            return decrypted_data, version

        return None, None

    def delete(self):
        logger.debug("deleting users data", user_id=self._user_id)
        questionnaire_state = self._find_questionnaire_state()
        if questionnaire_state:
            current_app.eq["storage"].delete(questionnaire_state)

    def _find_questionnaire_state(self):
        logger.debug("getting questionnaire data", user_id=self._user_id)
        return current_app.eq["storage"].get(QuestionnaireState, self._user_id)

    def _get_snappy_compressed_data(self, data):
        decrypted_data = self.encrypter.decrypt_data(data)
        return snappy.uncompress(decrypted_data).decode()
