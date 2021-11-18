from datetime import datetime, timezone

from app.data_models import QuestionnaireStore
from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage
from tests.app.app_context_test_case import AppContextTestCase
from tests.app.conftest import RESPONSE_EXPIRY


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
        encrypted.save(
            data="test",
            collection_exercise_sid="ce_sid",
            expires_at=RESPONSE_EXPIRY,
        )
        # check we can decrypt the data
        self.assertEqual(
            (
                "test",
                "ce_sid",
                QuestionnaireStore.LATEST_VERSION,
                None,
                RESPONSE_EXPIRY,
            ),
            encrypted.get_user_data(),
        )

    def test_store_and_get_with_submitted_at(self):
        now = datetime.now(timezone.utc).replace(microsecond=0)
        encrypted = EncryptedQuestionnaireStorage(
            user_id="1", user_ik="2", pepper="pepper"
        )
        encrypted.save(
            data="test",
            collection_exercise_sid="ce_sid",
            submitted_at=now,
            expires_at=RESPONSE_EXPIRY,
        )

        self.assertEqual(
            (
                "test",
                "ce_sid",
                QuestionnaireStore.LATEST_VERSION,
                now,
                RESPONSE_EXPIRY,
            ),
            encrypted.get_user_data(),
        )

    def test_store(self):
        data = "test"
        self.assertIsNone(self.storage.save(data, "ce_sid"))
        self.assertIsNotNone(
            self.storage.get_user_data()
        )  # pylint: disable=protected-access

    def test_get(self):
        data = "test"
        self.storage.save(
            data,
            "ce_sid",
            expires_at=RESPONSE_EXPIRY,
        )
        self.assertEqual(
            (
                data,
                "ce_sid",
                QuestionnaireStore.LATEST_VERSION,
                None,
                RESPONSE_EXPIRY,
            ),
            self.storage.get_user_data(),
        )

    def test_delete(self):
        data = "test"
        self.storage.save(
            data,
            "ce_sid",
            expires_at=RESPONSE_EXPIRY,
        )
        self.assertEqual(
            (
                data,
                "ce_sid",
                QuestionnaireStore.LATEST_VERSION,
                None,
                RESPONSE_EXPIRY,
            ),
            self.storage.get_user_data(),
        )
        self.storage.delete()
        self.assertEqual(
            (None, None, None, None, None), self.storage.get_user_data()
        )  # pylint: disable=protected-access
