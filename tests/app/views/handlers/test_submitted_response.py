from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

from app.data_models import QuestionnaireStore
from app.data_models.answer import Answer
from app.data_models.answer_store import AnswerStore
from app.data_models.session_data import SessionData
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.utilities.schema import load_schema_from_name
from app.views.handlers.submitted_response import (
    SubmittedResponse,
    SubmittedResponseExpired,
    SubmittedResponseNotEnabled,
)
from tests.app.app_context_test_case import AppContextTestCase


class TestSubmittedResponse(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self.session_data = SessionData(
            tx_id="123456789",
            schema_name="schema_name",
            response_id="response_id",
            period_str="period_str",
            language_code="cy",
            launch_language_code="en",
            survey_url=None,
            ru_name="ru_name",
            ru_ref="ru_ref",
            case_id="0123456789000000",
        )

    def test_enabled(self):
        submitted_at_date_time = datetime.now(timezone.utc)
        questionnaire_store = self.questionnaire_store_mock()
        questionnaire_store.submitted_at = submitted_at_date_time
        questionnaire_store.answer_store = AnswerStore(
            [
                Answer("name-answer", "John Smith", None).to_dict(),
            ]
        )
        schema = load_schema_from_name("test_view_submitted_response", "en")

        submitted_response = SubmittedResponse(
            schema, questionnaire_store, self.session_data, "en"
        )
        context = submitted_response.get_context()

        assert context["submitted_at"] == submitted_at_date_time
        assert context["tx_id"] == "1234-56789"
        assert context["summary"]["answers_are_editable"] == False
        assert context["summary"]["collapsible"] == False
        assert (
            context["summary"]["groups"][0]["blocks"][0]["question"]["answers"][0][
                "value"
            ]
            == "John Smith"
        )
        assert (
            context["summary"]["groups"][0]["blocks"][0]["question"]["title"]
            == "What is your name?"
        )

    def test_expired(self):
        questionnaire_store = self.questionnaire_store_mock()
        questionnaire_store.submitted_at = datetime(
            2021, 8, 12, 10, 30, 0, tzinfo=timezone.utc
        )

        schema = load_schema_from_name("test_view_submitted_response", "en")
        with self.assertRaises(SubmittedResponseExpired):
            SubmittedResponse(schema, questionnaire_store, self.session_data, "en")

    def test_not_enabled(self):
        questionnaire_store = self.questionnaire_store_mock()

        with self.assertRaises(SubmittedResponseNotEnabled):
            SubmittedResponse(
                QuestionnaireSchema({}), questionnaire_store, self.session_data, "en"
            )

    @staticmethod
    def questionnaire_store_mock():
        storage = Mock()
        storage.get_user_data = Mock(return_value=("{}", 1, None))
        return QuestionnaireStore(storage)
