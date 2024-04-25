from datetime import datetime, timedelta, timezone

import pytest
from flask import Flask

from app.survey_config.survey_type import SurveyType
from app.utilities.schema import load_schema_from_name
from app.views.contexts.thank_you_context import build_thank_you_context
from tests.app.questionnaire.conftest import get_metadata

SURVEY_TYPE_DEFAULT = SurveyType.DEFAULT
SURVEY_TYPE_SOCIAL = SurveyType.SOCIAL
SURVEY_TYPE_HEALTH = SurveyType.HEALTH
SUBMITTED_AT = datetime.now(timezone.utc)
SCHEMA = load_schema_from_name("test_view_submitted_response", "en")


def test_default_survey_context(app: Flask):
    with app.app_context():
        context = build_thank_you_context(
            SCHEMA,
            get_metadata(extra_metadata={"ru_name": "ESSENTIAL ENTERPRISE LTD"}),
            SUBMITTED_AT,
            SURVEY_TYPE_DEFAULT,
        )

        assert (
            context["submission_text"]
            == "Your answers have been submitted for <span>ESSENTIAL ENTERPRISE LTD</span>"
        )
        assert len(context["metadata"]["itemsList"]) == 2


@pytest.mark.parametrize(
    "survey_type",
    (
        (SURVEY_TYPE_SOCIAL),
        (SURVEY_TYPE_HEALTH),
    ),
)
def test_survey_context_without_ru_name(app: Flask, survey_type):
    with app.app_context():
        context = build_thank_you_context(
            SCHEMA, get_metadata(), SUBMITTED_AT, survey_type
        )

        assert context["submission_text"] == "Your answers have been submitted."
        assert len(context["metadata"]["itemsList"]) == 1


def test_default_survey_context_with_trad_as(app: Flask):
    with app.app_context():
        context = build_thank_you_context(
            SCHEMA,
            get_metadata(
                extra_metadata={"ru_name": "ESSENTIAL ENTERPRISE LTD", "trad_as": "EE"}
            ),
            SUBMITTED_AT,
            SURVEY_TYPE_DEFAULT,
        )

        assert (
            context["submission_text"]
            == "Your answers have been submitted for <span>ESSENTIAL ENTERPRISE LTD</span> (EE)"
        )
        assert len(context["metadata"]["itemsList"]) == 2


def test_view_submitted_response_enabled(app: Flask):
    with app.app_context():
        context = build_thank_you_context(
            SCHEMA, get_metadata(), SUBMITTED_AT, SURVEY_TYPE_DEFAULT
        )

        assert context["view_submitted_response"]["enabled"] is True


def test_view_submitted_response_not_enabled(app: Flask):
    with app.app_context():
        schema = load_schema_from_name("test_title", "en")

        context = build_thank_you_context(
            schema, get_metadata(), SUBMITTED_AT, SURVEY_TYPE_DEFAULT
        )

        assert context["view_submitted_response"]["enabled"] is False


def test_view_submitted_response_not_expired(app: Flask):
    with app.app_context():
        context = build_thank_you_context(
            SCHEMA, get_metadata(), SUBMITTED_AT, SURVEY_TYPE_DEFAULT
        )

        assert context["view_submitted_response"]["expired"] is False
        assert context["view_submitted_response"]["url"] == "/submitted/view-response/"


def test_view_submitted_response_expired(app: Flask):
    submitted_at = SUBMITTED_AT - timedelta(minutes=46)

    with app.app_context():
        context = build_thank_you_context(
            SCHEMA, get_metadata(), submitted_at, SURVEY_TYPE_DEFAULT
        )

        assert context["view_submitted_response"]["expired"] is True


def test_custom_guidance(app: Flask):
    with app.app_context():
        custom_guidance = {"contents": [{"description": "Custom guidance"}]}
        context = build_thank_you_context(
            SCHEMA,
            get_metadata(),
            SUBMITTED_AT,
            SURVEY_TYPE_DEFAULT,
            custom_guidance,
        )

        assert context["guidance"] == custom_guidance
