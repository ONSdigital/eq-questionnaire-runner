from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

from app.data_models import QuestionnaireStore
from app.data_models.answer import Answer
from app.data_models.answer_store import AnswerStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.utilities.schema import load_schema_from_name
from app.views.handlers.view_submitted_response import (
    ViewSubmittedResponse,
    ViewSubmittedResponseExpired,
    ViewSubmittedResponseNotEnabled,
)
from tests.app.app_context_test_case import AppContextTestCase


class TestViewSubmittedResponse(AppContextTestCase):
    def test_expired(self):
        questionnaire_store = self.questionnaire_store_mock()
        questionnaire_store.submitted_at = datetime(
            2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc
        )

        schema = load_schema_from_name("test_view_submitted_response", "en")
        with self.assertRaises(ViewSubmittedResponseExpired):
            ViewSubmittedResponse(schema, questionnaire_store, "en")

    def test_not_enabled(self):
        questionnaire_store = self.questionnaire_store_mock()

        with self.assertRaises(ViewSubmittedResponseNotEnabled):
            ViewSubmittedResponse(QuestionnaireSchema({}), questionnaire_store, "en")

    @staticmethod
    def questionnaire_store_mock():
        storage = Mock()
        storage.get_user_data = Mock(return_value=("{}", 1, None))
        return QuestionnaireStore(storage)
