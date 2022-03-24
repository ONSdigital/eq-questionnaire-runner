# pylint: disable=redefined-outer-name

from datetime import datetime, timedelta, timezone

import fakeredis
import pytest

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress_store import ProgressStore
from app.data_models.session_data import SessionData
from app.data_models.session_store import SessionStore
from app.publisher import PubSubPublisher
from app.questionnaire.location import Location
from app.setup import create_app
from app.storage.datastore import Datastore
from tests.app.mock_data_store import MockDatastore

RESPONSE_EXPIRY = datetime(2021, 11, 10, 8, 54, 22, tzinfo=timezone.utc)


@pytest.fixture
def app(mocker):
    setting_overrides = {"LOGIN_DISABLED": True, "SERVER_NAME": "test.localdomain"}
    mocker.patch("app.setup.datastore.Client", MockDatastore)
    mocker.patch("app.setup.redis.Redis", fakeredis.FakeStrictRedis)
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
def fixture_session_store(session_data):
    session_store = SessionStore("user_ik", "pepper", "eq_session_id")
    session_store.session_data = session_data
    return session_store


@pytest.fixture
def session_data():
    return SessionData(
        tx_id="tx_id",
        schema_name="test_checkbox",
        period_str="period_str",
        language_code=None,
        launch_language_code=None,
        survey_url=None,
        ru_name="ru_name",
        ru_ref="ru_ref",
        response_id="response_id",
        trad_as="trading_as",
        case_id="case_id",
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


@pytest.fixture
def answer_store():
    return AnswerStore()


@pytest.fixture
def list_store():
    return ListStore()


@pytest.fixture
def progress_store():
    return ProgressStore()


@pytest.fixture
def publisher(mocker):
    mocker.patch(
        "app.publisher.publisher.google.auth._default._get_explicit_environ_credentials",
        return_value=(mocker.Mock(), "test-project-id"),
    )
    return PubSubPublisher()


@pytest.fixture
def gb_locale(mocker):
    mocker.patch(
        "app.jinja_filters.flask_babel.get_locale",
        mocker.MagicMock(return_value="en_GB"),
    )


@pytest.fixture
def datastore(mock_client):
    return Datastore(mock_client)


@pytest.fixture
def current_location():
    return Location(section_id="some-section", block_id="some-block")
