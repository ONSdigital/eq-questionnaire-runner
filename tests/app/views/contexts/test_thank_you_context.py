from datetime import datetime, timezone
from functools import cache

import pytest
from flask import Flask

from app.data_models.session_data import SessionData
from app.views.contexts.thank_you_context import build_thank_you_context


@cache
def submitted_at():
    return datetime.now(timezone.utc)


@cache
def survey_type_default():
    return "default"


@cache
def survey_type_social():
    return "social"


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


def test_context_correct_if_survey_type_social(fake_session_data, app: Flask):
    with app.app_context():

        context = build_thank_you_context(
            fake_session_data, submitted_at(), survey_type_social()
        )

        assert context["submission_text"] == "Your answers have been submitted."
        assert len(context["metadata_items"]) == 1


def test_context_correct_if_survey_type_default(fake_session_data, app: Flask):
    with app.app_context():
        fake_session_data.ru_name = "ESSENTIAL ENTERPRISE LTD"
        context = build_thank_you_context(
            fake_session_data, submitted_at(), survey_type_default()
        )

        assert (
            context["submission_text"]
            == "Your answers have been submitted for <span>ESSENTIAL ENTERPRISE LTD</span>."
        )
        assert len(context["metadata_items"]) == 2


def test_context_correct_if_survey_type_default_and_trad_as_present(
    fake_session_data, app: Flask
):
    with app.app_context():
        fake_session_data.ru_name = "ESSENTIAL ENTERPRISE LTD"
        fake_session_data.trad_as = "123"
        context = build_thank_you_context(
            fake_session_data, submitted_at(), survey_type_default()
        )

        assert (
            context["submission_text"]
            == "Your answers have been submitted for <span>ESSENTIAL ENTERPRISE LTD</span> (123)."
        )
