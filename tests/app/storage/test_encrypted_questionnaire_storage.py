from datetime import datetime, timezone

from flask import current_app

from app.data_models import QuestionnaireStore
from app.data_models.app_models import QuestionnaireState
from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage
from app.storage.storage_encryption import StorageEncryption
from tests.app.app_context_test_case import AppContextTestCase


def _save_state_data(user_id, data, state_version=QuestionnaireStore.LATEST_VERSION):
    encryption = StorageEncryption(user_id, "mock", "mock")

    state_data = encryption.encrypt_data(data)

    questionnaire_state = QuestionnaireState(user_id, state_data, state_version, None)
    current_app.eq["storage"].put(questionnaire_state)


class TestEncryptedQuestionnaireStorage(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self.storage = EncryptedQuestionnaireStorage("user_id", "user_ik", "pepper")

    def test_encrypted_storage_requires_user_id(self):
        with self.assertRaises(ValueError):
            EncryptedQuestionnaireStorage(None, "key", "pepper")

    def test_encrypted_storage_requires_user_ik(self):
        with self.assertRaises(ValueError):
            EncryptedQuestionnaireStorage("1", None, "pepper")

    def test_store_and_get_without_submitted_at(self):
        encrypted = EncryptedQuestionnaireStorage(
            user_id="1", user_ik="2", pepper="pepper"
        )
        encrypted.save(data="test")
        # check we can decrypt the data
        self.assertEqual(
            ("test", QuestionnaireStore.LATEST_VERSION, None), encrypted.get_user_data()
        )

    def test_store_and_get_with_submitted_at(self):
        now = datetime.now(timezone.utc).replace(microsecond=0)
        encrypted = EncryptedQuestionnaireStorage(
            user_id="1", user_ik="2", pepper="pepper"
        )
        encrypted.save(data="test", submitted_at=now)

        self.assertEqual(
            ("test", QuestionnaireStore.LATEST_VERSION, now),
            encrypted.get_user_data(),
        )

    def test_store(self):
        data = "test"
        self.assertIsNone(self.storage.save(data))
        self.assertIsNotNone(
            self.storage.get_user_data()
        )  # pylint: disable=protected-access

    def test_get(self):
        data = "test"
        self.storage.save(data)
        self.assertEqual(
            (data, QuestionnaireStore.LATEST_VERSION, None),
            self.storage.get_user_data(),
        )

    def test_delete(self):
        data = "test"
        self.storage.save(data)
        self.assertEqual(
            (data, QuestionnaireStore.LATEST_VERSION, None),
            self.storage.get_user_data(),
        )
        self.storage.delete()
        self.assertEqual(
            (None, None, None), self.storage.get_user_data()
        )  # pylint: disable=protected-access
