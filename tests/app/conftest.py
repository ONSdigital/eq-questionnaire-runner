from datetime import datetime, timedelta, timezone

import pytest

from app.data_models.session_data import SessionData
from app.data_models.session_store import SessionStore
from app.setup import create_app

RESPONSE_EXPIRY = datetime(2021, 11, 10, 8, 54, 22, tzinfo=timezone.utc)


@pytest.fixture
def app():
    setting_overrides = {"LOGIN_DISABLED": True}
    the_app = create_app(setting_overrides=setting_overrides)

    return the_app


@pytest.fixture
def answer_schema_dropdown():
    return {
        "type": "Dropdown",
        "id": "mandatory-checkbox-with-mandatory-dropdown-detail-answer",
        "mandatory": True,
        "label": "Please specify heat level",
        "placeholder": "Select heat level",
        "options": [
            {"label": "Mild", "value": "Mild"},
            {"label": "Medium", "value": "Medium"},
            {"label": "Hot", "value": "Hot"},
        ],
    }


@pytest.fixture
def answer_schema_number():
    return {
        "mandatory": False,
        "id": "other-answer",
        "label": "Please enter a number of items",
        "type": "Number",
        "parent_id": "checkbox-question-numeric-detail",
    }


@pytest.fixture
def answer_schema_textfield():
    return {
        "mandatory": False,
        "id": "other-answer",
        "label": "Please specify",
        "type": "TextField",
        "parent_id": "checkbox-question-textfield-detail",
    }


@pytest.fixture
def expires_at():
    return datetime.now(timezone.utc) + timedelta(seconds=5)


@pytest.fixture(name="session_store")
def fixture_session_store():
    return SessionStore("user_ik", "pepper", "eq_session_id")


@pytest.fixture
def session_data():
    return SessionData(
        tx_id="tx_id",
        schema_name="some_schema_name",
        response_id="response_id",
        period_str="period_str",
        language_code=None,
        launch_language_code=None,
        survey_url=None,
        ru_name="ru_name",
        ru_ref="ru_ref",
        case_id="case_id",
    )


@pytest.fixture
def mock_get_session_store(mocker, session_store):
    return mocker.patch(
        "app.authentication.authenticator.get_session_store", return_value=session_store
    )


@pytest.fixture
def mock_get_metadata(mocker):
    return mocker.patch("app.authentication.roles.get_metadata")


@pytest.fixture
def mock_current_user(mocker):
    return mocker.patch("app.authentication.roles.current_user")


@pytest.fixture
def mock_redis_put(mocker):
    return mocker.patch("app.storage.redis.Redis.put")
