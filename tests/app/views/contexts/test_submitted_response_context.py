from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

from flask import Flask
from flask_babel import format_datetime

from app.data_models import QuestionnaireStore
from app.data_models.answer import Answer
from app.data_models.answer_store import AnswerStore
from app.settings import VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS
from app.utilities.schema import load_schema_from_name
from app.views.contexts.view_submitted_response_context import (
    build_view_submitted_response_context,
)
from tests.app.conftest import RESPONSE_EXPIRY

SUBMITTED_AT = datetime.now(timezone.utc)
SCHEMA = load_schema_from_name("test_view_submitted_response", "en")


def test_build_view_submitted_response_context_summary(app: Flask):
    with app.app_context():
        questionnaire_store = fake_questionnaire_store()
        context = build_view_submitted_response_context(
            "en", SCHEMA, questionnaire_store, "default"
        )

        assert context["summary"]["answers_are_editable"] is False
        assert context["summary"]["collapsible"] is False
        assert context["view_submitted_response"]["expired"] is False
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


def test_build_view_submitted_response_context_submitted_text(app: Flask):
    with app.app_context():
        questionnaire_store = fake_questionnaire_store()
        context = build_view_submitted_response_context(
            "en", SCHEMA, questionnaire_store, "default"
        )

        assert context["submitted_text"] == "Answers submitted for <span>Apple</span>"


def test_build_view_submitted_response_context_submitted_text_social(app: Flask):
    with app.app_context():
        questionnaire_store = fake_questionnaire_store()
        questionnaire_store.metadata["trad_as"] = "Apple Inc"
        context = build_view_submitted_response_context(
            "en", SCHEMA, questionnaire_store, "social"
        )

        assert context["submitted_text"] == "Answers submitted."


def test_build_view_submitted_response_context_submitted_text_with_trad_as(app: Flask):
    with app.app_context():
        questionnaire_store = fake_questionnaire_store()
        questionnaire_store.metadata["trad_as"] = "Apple Inc"
        context = build_view_submitted_response_context(
            "en", SCHEMA, questionnaire_store, "default"
        )

        assert (
            context["submitted_text"]
            == "Answers submitted for <span>Apple</span> (Apple Inc)"
        )


def test_view_submitted_response_expired(
    app: Flask,
):
    with app.app_context():
        questionnaire_store = fake_questionnaire_store()
        questionnaire_store.submitted_at = datetime.now(timezone.utc) - timedelta(
            seconds=VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS
        )
        context = build_view_submitted_response_context(
            "en", SCHEMA, questionnaire_store, "default"
        )

        assert context["view_submitted_response"]["expired"] is True
        assert "summary" not in context


def fake_questionnaire_store():
    storage = Mock()
    storage.get_user_data = Mock(
        return_value=(
            "{}",
            "ce_sid",
            1,
            None,
            RESPONSE_EXPIRY,
        )
    )
    questionnaire_store = QuestionnaireStore(storage)
    questionnaire_store.submitted_at = SUBMITTED_AT
    questionnaire_store.metadata = {"tx_id": "123456789", "ru_name": "Apple"}
    questionnaire_store.answer_store = AnswerStore(
        [
            Answer("name-answer", "John Smith", None).to_dict(),
            Answer("address-answer", "NP10 8XG", None).to_dict(),
        ]
    )
    return questionnaire_store


def format_submitted_on_description():
    date = format_datetime(SUBMITTED_AT, format="dd LLLL yyyy")
    time = format_datetime(SUBMITTED_AT, format="HH:mm")
    return f"{date} at {time}"
