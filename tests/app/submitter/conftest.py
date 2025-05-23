import uuid

import pytest
from google.cloud.storage import Blob
from mock import MagicMock
from requests import Response

from app.authentication.auth_payload_versions import AuthPayloadVersion
from app.data_models import ListStore, QuestionnaireStore
from app.data_models.answer import Answer
from app.data_models.answer_store import AnswerStore
from app.data_models.metadata_proxy import MetadataProxy
from app.data_models.supplementary_data_store import SupplementaryDataStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.settings import ACCOUNT_SERVICE_BASE_URL_SOCIAL
from app.submitter import RabbitMQSubmitter
from tests.app.parser.conftest import get_response_expires_at

RAW_METADATA_V2 = {
    "version": AuthPayloadVersion.V2.value,
    "tx_id": str(uuid.uuid4()),
    "schema_name": "1_0000",
    "collection_exercise_sid": "test-sid",
    "account_service_url": ACCOUNT_SERVICE_BASE_URL_SOCIAL,
    "survey_metadata": {
        "data": {
            "period_id": "2016-02-01",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "12345678901A",
            "ru_name": "Apple",
            "case_type": "SPG",
            "form_type": "I",
            "case_ref": "1000000000000001",
            "display_address": "68 Abingdon Road, Goathill",
            "user_id": "789473423",
        },
    },
    "response_id": "1234567890123456",
    "case_id": str(uuid.uuid4()),
    "region_code": "GB-ENG",
    "channel": "RH",
    "jti": str(uuid.uuid4()),
    "response_expires_at": get_response_expires_at(),
}
METADATA_V2 = MetadataProxy.from_dict(RAW_METADATA_V2)


def get_questionnaire_store():
    user_answer = Answer(answer_id="GHI", value=0, list_item_id=None)

    storage = MagicMock()
    storage.get_user_data = MagicMock(return_value=("{}", "ce_sid", 1, None))
    storage.add_or_update = MagicMock()

    store = QuestionnaireStore(storage)

    store.data_stores.answer_store = AnswerStore()
    store.supplementary_data_store = SupplementaryDataStore()
    store.data_stores.answer_store.add_or_update(user_answer)
    store.data_stores.metadata = METADATA_V2

    store.data_stores.response_metadata = {
        "started_at": "2018-07-04T14:49:33.448608+00:00"
    }

    return store


@pytest.fixture
def fake_metadata_v2_schema_url():
    copy = RAW_METADATA_V2.copy()
    copy["schema_url"] = "https://schema_url.com"
    del copy["schema_name"]
    return MetadataProxy.from_dict(copy)


@pytest.fixture
def fake_metadata_v2_cir_instrument_id():
    copy = RAW_METADATA_V2.copy()
    copy["cir_instrument_id"] = "f0519981-426c-8b93-75c0-bfc40c66fe25"
    del copy["schema_name"]
    return MetadataProxy.from_dict(copy)


@pytest.fixture
def fake_response_metadata():
    response_metadata = {"started_at": "2018-07-04T14:49:33.448608+00:00"}
    return response_metadata


@pytest.fixture
def fake_questionnaire_schema():
    questionnaire = {"survey_id": "021", "data_version": "0.0.3"}

    return QuestionnaireSchema(questionnaire)


@pytest.fixture
def rabbitmq_submitter():
    return RabbitMQSubmitter(
        host="host1", secondary_host="host2", port=5672, queue="test_queue"
    )


@pytest.fixture
def patch_blocking_connection(mocker):
    return mocker.patch("app.submitter.submitter.BlockingConnection")


@pytest.fixture
def patch_url_parameters(mocker):
    return mocker.patch("app.submitter.submitter.URLParameters")


@pytest.fixture
def patch_gcs_client(mocker):
    return mocker.patch("app.submitter.submitter.storage.Client")


@pytest.fixture
def gcs_blob_with_retry(mocker):
    blob = Blob(name="some-blob", bucket=mocker.MagicMock())

    response_503 = Response()
    response_503.status_code = 503

    response_200 = Response()
    response_200._content = (  # pylint: disable=protected-access
        b'{"some-key":"some-value"}'
    )
    response_200.status_code = 200

    mock_transport_request = mocker.Mock(side_effect=[response_503, response_200])
    mock_transport = mocker.Mock()
    mock_transport.request = mock_transport_request
    blob._get_transport = mocker.Mock(  # pylint: disable=protected-access
        return_value=mock_transport
    )

    return blob


@pytest.fixture
def repeating_blocks_answer_store():
    return AnswerStore(
        [
            {"answer_id": "responsible-party-answer", "value": "Yes"},
            {"answer_id": "any-companies-or-branches-answer", "value": "Yes"},
            {
                "answer_id": "company-or-branch-name",
                "value": "CompanyA",
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "registration-number",
                "value": "123",
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "registration-date",
                "value": "2023-01-01",
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "authorised-trader-uk-radio",
                "value": "Yes",
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "authorised-trader-eu-radio",
                "value": "Yes",
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "company-or-branch-name",
                "value": "CompanyB",
                "list_item_id": "UHPLbX",
            },
            {
                "answer_id": "registration-number",
                "value": "456",
                "list_item_id": "UHPLbX",
            },
            {
                "answer_id": "registration-date",
                "value": "2023-01-01",
                "list_item_id": "UHPLbX",
            },
            {
                "answer_id": "authorised-trader-uk-radio",
                "value": "No",
                "list_item_id": "UHPLbX",
            },
            {
                "answer_id": "authorised-trader-eu-radio",
                "value": "No",
                "list_item_id": "UHPLbX",
            },
            {
                "answer_id": "any-other-trading-details",
                "value": "N/A",
            },
        ]
    )


@pytest.fixture
def repeating_blocks_list_store():
    return ListStore([{"items": ["PlwgoG", "UHPLbX"], "name": "companies"}])
