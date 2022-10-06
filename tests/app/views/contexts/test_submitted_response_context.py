from datetime import datetime, timedelta, timezone

import pytest
from flask import Flask
from flask_babel import format_datetime
from mock import Mock

from app.data_models import QuestionnaireStore
from app.data_models.answer import Answer
from app.data_models.answer_store import AnswerStore
from app.data_models.metadata_proxy import MetadataProxy
from app.settings import VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS
from app.submitter.converter_v2 import NoMetadataException
from app.survey_config.survey_type import SurveyType
from app.utilities.schema import load_schema_from_name
from app.views.contexts.view_submitted_response_context import (
    build_view_submitted_response_context,
)

SUBMITTED_AT = datetime.now(timezone.utc)
SCHEMA = load_schema_from_name("test_view_submitted_response", "en")


def test_build_view_submitted_response_context_summary(app: Flask):
    with app.app_context():
        questionnaire_store = fake_questionnaire_store()
        context = build_view_submitted_response_context(
            "en", SCHEMA, questionnaire_store, SurveyType.DEFAULT
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
            "en", SCHEMA, questionnaire_store, SurveyType.DEFAULT
        )

        assert context["submitted_text"] == "Answers submitted for <span>Apple</span>"


def test_build_view_submitted_response_context_submitted_text_social(app: Flask):
    with app.app_context():
        questionnaire_store = fake_questionnaire_store()
        context = build_view_submitted_response_context(
            "en", SCHEMA, questionnaire_store, SurveyType.SOCIAL
        )

        assert context["submitted_text"] == "Answers submitted."


def test_build_view_submitted_response_context_submitted_text_with_trad_as(app: Flask):
    with app.app_context():
        questionnaire_store = fake_questionnaire_store_with_trad_as()
        context = build_view_submitted_response_context(
            "en", SCHEMA, questionnaire_store, SurveyType.DEFAULT
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
            "en", SCHEMA, questionnaire_store, SurveyType.DEFAULT
        )

        assert context["view_submitted_response"]["expired"] is True
        assert "summary" not in context


def test_build_view_submitted_response_no_submitted_at(app: Flask):
    with app.app_context():
        questionnaire_store = fake_questionnaire_store_no_submitted_at()
        with pytest.raises(Exception):
            build_view_submitted_response_context(
                "en", SCHEMA, questionnaire_store, SurveyType.DEFAULT
            )


def test_summary_headers_without_change_link(
    app: Flask,
):
    with app.app_context():
        questionnaire_store = fake_questionnaire_store()
        context = build_view_submitted_response_context(
            "en", SCHEMA, questionnaire_store, SurveyType.DEFAULT
        )
        assert context["summary"]["headers"] == ["Question", "Answer given"]


def test_no_metadata_raises_error(
    app: Flask,
):
    with app.app_context():
        questionnaire_store = fake_questionnaire_store()

        questionnaire_store.metadata = None

        with pytest.raises(NoMetadataException):
            build_view_submitted_response_context(
                "en", SCHEMA, questionnaire_store, SurveyType.DEFAULT
            )


def fake_questionnaire_store():
    storage = Mock()
    storage.get_user_data = Mock(return_value=("{}", "ce_sid", 1, None))
    questionnaire_store = QuestionnaireStore(storage)
    questionnaire_store.metadata = MetadataProxy.from_dict(
        {"tx_id": "tx_id", "ru_name": "Apple"}
    )
    questionnaire_store.submitted_at = SUBMITTED_AT
    questionnaire_store.answer_store = AnswerStore(
        [
            Answer("name-answer", "John Smith", None).to_dict(),
            Answer("address-answer", "NP10 8XG", None).to_dict(),
        ]
    )
    return questionnaire_store


def fake_questionnaire_store_with_trad_as():
    storage = Mock()
    storage.get_user_data = Mock(return_value=("{}", "ce_sid", 1, None))
    questionnaire_store = QuestionnaireStore(storage)
    questionnaire_store.metadata = MetadataProxy.from_dict(
        {"tx_id": "tx_id", "ru_name": "Apple", "trad_as": "Apple Inc"}
    )
    questionnaire_store.submitted_at = SUBMITTED_AT
    questionnaire_store.answer_store = AnswerStore()
    return questionnaire_store


def format_submitted_on_description():
    date = format_datetime(SUBMITTED_AT, format="dd LLLL yyyy")
    time = format_datetime(SUBMITTED_AT, format="HH:mm")
    return f"{date} at {time}"


def fake_questionnaire_store_no_submitted_at():
    storage = Mock()
    storage.get_user_data = Mock(return_value=("{}", "ce_sid", 1, None))
    questionnaire_store = QuestionnaireStore(storage)
    questionnaire_store.submitted_at = None
    questionnaire_store.metadata = {}
    questionnaire_store.answer_store = AnswerStore()
    return questionnaire_store
