from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

from app.data_models import QuestionnaireStore
from app.data_models.answer import Answer
from app.data_models.answer_store import AnswerStore
from app.utilities.schema import load_schema_from_name
from app.views.contexts.view_submitted_response_context import (
    build_view_submitted_response_context,
)
from tests.app.app_context_test_case import AppContextTestCase


class TestViewSubmittedResponseContext(AppContextTestCase):
    def test_build_view_submitted_response_context(self):
        storage = Mock()
        storage.get_user_data = Mock(return_value=("{}", 1, None))
        questionnaire_store = QuestionnaireStore(storage)
        submitted_at_date_time = datetime.now(timezone.utc)
        questionnaire_store.submitted_at = submitted_at_date_time
        questionnaire_store.metadata = {
            "tx_id": "123456789",
            "ru_name": "Apple",
            "trad_as": "Apple",
        }
        questionnaire_store.answer_store = AnswerStore(
            [
                Answer("name-answer", "John Smith", None).to_dict(),
                Answer("address-answer", "NP10 8XG", None).to_dict(),
            ]
        )
        schema = load_schema_from_name("test_view_submitted_response", "en")

        context = build_view_submitted_response_context(
            "en", schema, questionnaire_store
        )

        assert context["submitted_at"] == submitted_at_date_time
        assert context["view_answers"] is True
        assert context["tx_id"] == "1234 - 56789"
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
        assert (
            context["summary"]["groups"][1]["blocks"][0]["question"]["answers"][0][
                "value"
            ]
            == "NP10 8XG"
        )
        assert (
            context["summary"]["groups"][1]["blocks"][0]["question"]["title"]
            == "What is your address?"
        )

    def test_view_answers_is_false_when_submitted_at_greater_than_45_mins(self):
        storage = Mock()
        storage.get_user_data = Mock(return_value=("{}", 1, None))
        questionnaire_store = QuestionnaireStore(storage)
        submitted_at_date_time = datetime.now(timezone.utc)
        questionnaire_store.submitted_at = submitted_at_date_time - timedelta(
            minutes=46
        )
        questionnaire_store.metadata = {
            "tx_id": "123456789",
            "ru_name": "Apple",
            "trad_as": "Apple",
        }
        questionnaire_store.answer_store = AnswerStore(
            [
                Answer("name-answer", "John Smith", None).to_dict(),
                Answer("address-answer", "NP10 8XG", None).to_dict(),
            ]
        )
        schema = load_schema_from_name("test_view_submitted_response", "en")

        context = build_view_submitted_response_context(
            "en", schema, questionnaire_store
        )

        assert context["view_answers"] is False
