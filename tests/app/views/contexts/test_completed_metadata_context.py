# pylint: disable=redefined-outer-name
from datetime import datetime, timezone
from functools import cache

import pytest

from app.data_models.session_data import SessionData
from app.views.contexts.thank_you_context import build_default_thank_you_context


@cache
def submitted_at():
    return datetime.now(timezone.utc)


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


def test_context_includes_period_str_if_available(fake_session_data):
    fake_session_data.period_str = "some name"

    context = build_default_thank_you_context(fake_session_data, submitted_at())

    assert context["period_str"] == "some name"


def test_context_includes_ru_name_if_available(fake_session_data):
    fake_session_data.ru_name = "some name"

    context = build_default_thank_you_context(fake_session_data, submitted_at())

    assert context["ru_name"] == "some name"


def test_context_does_not_include_period_str_and_ru_name_by_default(fake_session_data):
    context = build_default_thank_you_context(fake_session_data, submitted_at())
    assert "ru_name" not in context
    assert "period_str" not in context
