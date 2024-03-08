# pylint: disable=redefined-outer-name
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from http.client import HTTPMessage

import fakeredis
import pytest
from mock import MagicMock
from mock.mock import Mock
from requests.adapters import ConnectTimeoutError, ReadTimeoutError
from urllib3.connectionpool import HTTPConnectionPool
from urllib3.response import HTTPResponse

from app.data_models import QuestionnaireStore
from app.data_models.answer_store import AnswerStore
from app.data_models.data_stores import DataStores
from app.data_models.list_store import ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.data_models.progress_store import ProgressStore
from app.data_models.session_data import SessionData
from app.data_models.session_store import SessionStore
from app.data_models.supplementary_data_store import (
    SupplementaryDataListMapping,
    SupplementaryDataStore,
)
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
    session_store = SessionStore(
        "user_ik",
        "pepper",
        "eq_session_id",
    )
    session_store.session_data = session_data
    session_store.user_id = "user_id"
    return session_store


@pytest.fixture
def fake_questionnaire_store():
    storage = MagicMock()
    storage.get_user_data = MagicMock(return_value=("{}", "ce_sid", 1, None))
    storage.add_or_update = MagicMock()
    store = QuestionnaireStore(storage)
    store.data_stores.metadata = MetadataProxy.from_dict(
        {
            "schema_name": "test_checkbox",
            "display_address": "68 Abingdon Road, Goathill",
            "tx_id": "tx_id",
            "language_code": "en",
        }
    )

    return store


@pytest.fixture
def fake_metadata():
    return MetadataProxy.from_dict(
        {
            "tx_id": "tx_id",
            "language_code": "en",
            "display_address": "68 Abingdon Road, Goathill",
        }
    )


@pytest.fixture
def session_data():
    return SessionData(
        language_code=None,
    )


@pytest.fixture
def session_data_with_language_code():
    return SessionData(
        language_code="en",
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
def supplementary_data_store():
    return SupplementaryDataStore()


@pytest.fixture
def data_stores():
    return DataStores()


@pytest.fixture
def publisher(mocker):
    mocker.patch(
        "app.publisher.publisher.google.auth._default._get_explicit_environ_credentials",
        return_value=(mocker.Mock(universe_domain="test"), "test-project-id"),
    )
    mocker.patch(
        "google.pubsub_v1.services.publisher.client.PublisherClient._compare_universes",
        return_value=True,
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


@pytest.fixture
def location():
    return Location("test-section", "test-block", "test-list", "list_item_id")


@pytest.fixture
def mock_autoescape_context(mocker):
    return mocker.Mock(autoescape=True)


@pytest.fixture
def mocked_response_content(mocker):
    decodable_content = Mock()
    decodable_content.decode.return_value = b"{}"
    mocker.patch("requests.models.Response.content", decodable_content)


@pytest.fixture
def mocked_make_request_with_timeout(
    mocker, mocked_response_content  # pylint: disable=unused-argument
):
    connect_timeout_error = ConnectTimeoutError("connect timed out")
    read_timeout_error = ReadTimeoutError(
        pool=None, message="read timed out", url="test-url"
    )

    response_not_timed_out = HTTPResponse(status=200, headers={}, msg=HTTPMessage())
    response_not_timed_out.drain_conn = Mock(return_value=None)

    return mocker.patch.object(
        HTTPConnectionPool,
        "_make_request",
        side_effect=[
            connect_timeout_error,
            read_timeout_error,
            response_not_timed_out,
        ],
    )


@pytest.fixture
def supplementary_data():
    return {
        "schema_version": "v1",
        "identifier": "12345678901",
        "note": {
            "title": "Volume of total production",
            "example": {
                "title": "Including",
                "description": "Sales across all UK stores",
            },
        },
        "guidance": "Some supplementary guidance about the survey",
        "items": {
            "products": [
                {
                    "identifier": 89929001,
                    "name": "Articles and equipment for sports or outdoor games",
                    "cn_codes": "2504 + 250610 + 2512 + 2519 + 2524",
                    "guidance": {"title": "Include", "description": "sportswear"},
                    "value_sales": {
                        "answer_code": "89929001",
                        "label": "Value of sales",
                    },
                },
                {
                    "identifier": "201630601",
                    "name": "Other Minerals",
                    "cn_codes": "5908 + 5910 + 591110 + 591120 + 591140",
                    "value_sales": {
                        "answer_code": "201630601",
                        "label": "Value of sales",
                    },
                },
            ]
        },
    }


@pytest.fixture
def supplementary_data_with_employees(supplementary_data):
    copy = deepcopy(supplementary_data)
    copy["items"]["employees"] = [
        {
            "identifier": "429001",
            "personal_details": {
                "forename": "Harry",
                "surname": "Potter",
                "address": {
                    "postcode": "BS1 1AJ",
                    "house_number": "12",
                    "city": "Bristol",
                },
            },
            "employment_details": {
                "job_title": "Customer assistant",
                "start_date": "2020-01-01",
                "salary": {
                    "payroll_number": "54345",
                    "value": "25000",
                    "currency": "GBP",
                },
            },
        },
        {
            "identifier": "529001",
            "personal_details": {
                "forename": "Bruce",
                "surname": "Wayne",
                "address": {
                    "postcode": "BS1 1HJ",
                    "house_number": "15",
                    "city": "Bristol",
                },
            },
            "employment_details": {
                "job_title": "Customer assistant",
                "start_date": "2019-03-01",
                "salary": {
                    "payroll_number": "4345",
                    "value": "27000",
                    "currency": "GBP",
                },
            },
        },
        {
            "identifier": "629011",
            "personal_details": {
                "forename": "Henry",
                "surname": "Green",
                "address": {
                    "postcode": "BS1 1HR",
                    "house_number": "11",
                    "city": "Bristol",
                },
            },
            "employment_details": {
                "job_title": "Warehouse operative",
                "start_date": "2022-10-01",
                "salary": {
                    "payroll_number": "28379",
                    "value": "29000",
                    "currency": "GBP",
                },
            },
        },
        {
            "identifier": "729011",
            "personal_details": {
                "forename": "Fourth",
                "surname": "Person",
                "address": {
                    "postcode": "BS1 1HO",
                    "house_number": "14",
                    "city": "Bristol",
                },
            },
            "employment_details": {
                "job_title": "Warehouse operative",
                "start_date": "2022-11-01",
                "salary": {
                    "payroll_number": "22238379",
                    "value": "29500",
                    "currency": "GBP",
                },
            },
        },
    ]
    return copy


@pytest.fixture
def supplementary_data_list_mappings():
    return {
        "products": [
            SupplementaryDataListMapping(identifier=89929001, list_item_id="item-1"),
            SupplementaryDataListMapping(identifier="201630601", list_item_id="item-2"),
        ],
    }


@pytest.fixture
def supplementary_data_list_mappings_extra_item():
    return {
        "products": [
            SupplementaryDataListMapping(identifier=89929001, list_item_id="item-1"),
            SupplementaryDataListMapping(identifier="201630601", list_item_id="item-2"),
            SupplementaryDataListMapping(identifier="103219277", list_item_id="item-3"),
        ],
    }


@pytest.fixture
def supplementary_data_employee_list_mappings():
    return {
        "employees": [
            SupplementaryDataListMapping(
                identifier="429001", list_item_id="employee-1"
            ),
            SupplementaryDataListMapping(
                identifier="529001", list_item_id="employee-2"
            ),
            SupplementaryDataListMapping(
                identifier="629011", list_item_id="employee-3"
            ),
            SupplementaryDataListMapping(
                identifier="729011", list_item_id="employee-4"
            ),
        ],
    }


@pytest.fixture
def supplementary_data_store_with_data(
    supplementary_data, supplementary_data_list_mappings
):
    return SupplementaryDataStore(
        supplementary_data=supplementary_data,
        list_mappings=supplementary_data_list_mappings,
    )


@pytest.fixture
def supplementary_data_store_with_data_extra_item(
    supplementary_data, supplementary_data_list_mappings_extra_item
):
    return SupplementaryDataStore(
        supplementary_data=supplementary_data,
        list_mappings=supplementary_data_list_mappings_extra_item,
    )


@pytest.fixture
def supplementary_data_store_with_employees(
    supplementary_data_with_employees,
    supplementary_data_list_mappings,
    supplementary_data_employee_list_mappings,
):
    return SupplementaryDataStore(
        supplementary_data=supplementary_data_with_employees,
        list_mappings={
            **supplementary_data_list_mappings,
            **supplementary_data_employee_list_mappings,
        },
    )
