from datetime import datetime, timedelta, timezone

import pytest
from flask import Flask
from flask_babel import format_datetime
from mock import Mock

from app.data_models import QuestionnaireStore
from app.data_models.answer import Answer
from app.data_models.answer_store import AnswerStore
from app.settings import VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS
from app.submitter.converter_v2 import NoMetadataException
from app.survey_config.survey_type import SurveyType
from app.utilities.schema import load_schema_from_name
from app.views.contexts.view_submitted_response_context import (
    build_view_submitted_response_context,
)
from tests.app.questionnaire.conftest import get_metadata

SUBMITTED_AT = datetime.now(timezone.utc)
SCHEMA = load_schema_from_name("test_view_submitted_response", "en")


def test_build_view_submitted_response_context_summary(app: Flask):
    with app.app_context():
        questionnaire_store = fake_questionnaire_store(
            {"tx_id": "tx_id", "ru_name": "Apple"}, SUBMITTED_AT
        )
        context = build_view_submitted_response_context(
            "en", SCHEMA, questionnaire_store, SurveyType.DEFAULT
        )

        assert context["summary"]["answers_are_editable"] is False
        assert context["summary"]["collapsible"] is False
        assert context["view_submitted_response"]["expired"] is False
        assert (
            context["summary"]["sections"][0]["groups"][0]["blocks"][0]["question"][
                "answers"
            ][0]["value"]
            == "John Smith"
        )
        assert (
            context["summary"]["sections"][0]["groups"][0]["blocks"][0]["question"][
                "title"
            ]
            == "What is your name?"
        )
        assert (
            context["summary"]["sections"][0]["groups"][1]["blocks"][0]["question"][
                "answers"
            ][0]["value"]
            == "NP10 8XG"
        )
        assert (
            context["summary"]["sections"][0]["groups"][1]["blocks"][0]["question"][
                "title"
            ]
            == "What is your address?"
        )


def test_view_submitted_response_context_submitted_text_with_ru_name(app: Flask):
    with app.app_context():
        questionnaire_store = fake_questionnaire_store(
            {"tx_id": "tx_id", "ru_name": "Apple"}, SUBMITTED_AT
        )
        context = build_view_submitted_response_context(
            "en", SCHEMA, questionnaire_store, SurveyType.DEFAULT
        )

        assert context["submitted_text"] == "Answers submitted for <span>Apple</span>"


@pytest.mark.parametrize(
    "survey_type",
    (
        (SurveyType.SOCIAL),
        (SurveyType.HEALTH),
    ),
)
def test_view_submitted_response_context_submitted_text_without_ru_name(
    app: Flask, survey_type
):
    with app.app_context():
        questionnaire_store = fake_questionnaire_store({"tx_id": "tx_id"}, SUBMITTED_AT)
        context = build_view_submitted_response_context(
            "en", SCHEMA, questionnaire_store, survey_type
        )

        assert context["submitted_text"] == "Answers submitted."


def test_build_view_submitted_response_context_submitted_text_with_trad_as(app: Flask):
    with app.app_context():
        questionnaire_store = fake_questionnaire_store(
            {"tx_id": "tx_id", "ru_name": "Apple", "trad_as": "Apple Inc"}, SUBMITTED_AT
        )
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
        questionnaire_store = fake_questionnaire_store(
            {"tx_id": "tx_id", "ru_name": "Apple"}, SUBMITTED_AT
        )
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
        questionnaire_store = fake_questionnaire_store({}, None)
        with pytest.raises(Exception):
            build_view_submitted_response_context(
                "en", SCHEMA, questionnaire_store, SurveyType.DEFAULT
            )


def test_no_metadata_raises_error(
    app: Flask,
):
    with app.app_context():
        questionnaire_store = fake_questionnaire_store({}, SUBMITTED_AT)

        questionnaire_store.data_stores.metadata = None

        with pytest.raises(NoMetadataException):
            build_view_submitted_response_context(
                "en", SCHEMA, questionnaire_store, SurveyType.DEFAULT
            )


def fake_questionnaire_store(metadata, submitted_at):
    storage = Mock()
    storage.get_user_data = Mock(return_value=("{}", "ce_sid", 1, None))
    questionnaire_store = QuestionnaireStore(storage)
    questionnaire_store.data_stores.metadata = get_metadata(metadata)
    questionnaire_store.submitted_at = submitted_at
    questionnaire_store.data_stores.answer_store = AnswerStore(
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
