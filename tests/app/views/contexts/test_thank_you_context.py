from datetime import datetime, timedelta, timezone

import pytest
from flask import Flask

from app.data_models.session_data import SessionData
from app.utilities.schema import load_schema_from_name
from app.views.contexts.thank_you_context import build_thank_you_context

SURVEY_TYPE_DEFAULT = "default"
SURVEY_TYPE_SOCIAL = "social"
SUBMITTED_AT = datetime.now(timezone.utc)
SCHEMA = load_schema_from_name("test_view_submitted_response", "en")


@pytest.fixture
def fake_session_data():
    return SessionData(
        tx_id="tx_id",
        schema_name="some_schema_name",
        language_code=None,
        launch_language_code=None,
        survey_url=None,
        ru_ref="ru_ref",
        response_id="response_id",
        case_id="case_id",
        period_str=None,
        ru_name=None,
    )


def test_social_survey_context(fake_session_data, app: Flask):
    with app.app_context():

        context = build_thank_you_context(
            fake_session_data, SUBMITTED_AT, SURVEY_TYPE_SOCIAL, SCHEMA
        )

        assert context["submission_text"] == "Your answers have been submitted."
        assert len(context["metadata"]["itemsList"]) == 1


def test_default_survey_context(fake_session_data, app: Flask):
    with app.app_context():
        fake_session_data.ru_name = "ESSENTIAL ENTERPRISE LTD"
        context = build_thank_you_context(
            fake_session_data, SUBMITTED_AT, SURVEY_TYPE_DEFAULT, SCHEMA
        )

        assert (
            context["submission_text"]
            == "Your answers have been submitted for <span>ESSENTIAL ENTERPRISE LTD</span>."
        )
        assert len(context["metadata"]["itemsList"]) == 2


def test_view_submitted_response_enabled_is_true_when_set_in_schema(
    fake_session_data, app: Flask
):
    with app.app_context():
        context = build_thank_you_context(
            fake_session_data, SUBMITTED_AT, SURVEY_TYPE_DEFAULT, SCHEMA
        )

        assert context["view_submitted_response_enabled"] is True


def test_view_submitted_response_enabled_is_false_when_not_set_in_schema(
    fake_session_data, app: Flask
):
    with app.app_context():
        schema = load_schema_from_name("test_title", "en")

        context = build_thank_you_context(
            fake_session_data, SUBMITTED_AT, SURVEY_TYPE_DEFAULT, schema
        )

        assert context["view_submitted_response_enabled"] is False


def test_view_submitted_response_expired_is_false_when_submitted_at_less_than_expiry_time(
    fake_session_data, app: Flask
):
    with app.app_context():
        context = build_thank_you_context(
            fake_session_data, SUBMITTED_AT, SURVEY_TYPE_DEFAULT, SCHEMA
        )

        assert context["view_submitted_response_expired"] is False
        assert context["view_submitted_response_url"] == "/submitted/view-response/"


def test_view_submitted_response_expired_is_true_when_submitted_at_less_than_expiry_time(
    fake_session_data, app: Flask
):
    submitted_at = SUBMITTED_AT - timedelta(minutes=46)

    with app.app_context():

        context = build_thank_you_context(
            fake_session_data, submitted_at, SURVEY_TYPE_DEFAULT, SCHEMA
        )

        assert context["view_submitted_response_expired"] is True
        assert context["view_submitted_response_url"] is None


def test_default_survey_context_with_trad_as(fake_session_data, app: Flask):
    with app.app_context():
        fake_session_data.ru_name = "ESSENTIAL ENTERPRISE LTD"
        fake_session_data.trad_as = "123"
        context = build_thank_you_context(
            fake_session_data, SUBMITTED_AT, SURVEY_TYPE_DEFAULT, SCHEMA
        )

        assert (
            context["submission_text"]
            == "Your answers have been submitted for <span>ESSENTIAL ENTERPRISE LTD</span> (123)."
        )
        assert len(context["metadata"]["itemsList"]) == 2


def test_custom_guidance(fake_session_data, app: Flask):
    with app.app_context():
        custom_guidance = {"contents": [{"description": "Custom guidance"}]}
        context = build_thank_you_context(
            fake_session_data,
            SUBMITTED_AT,
            SURVEY_TYPE_DEFAULT,
            SCHEMA,
            custom_guidance,
        )

        assert context["guidance"] == custom_guidance
