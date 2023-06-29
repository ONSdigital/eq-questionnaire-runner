# pylint: disable=redefined-outer-name
import uuid

import pytest
from google.cloud.storage import Blob
from google.resumable_media import InvalidResponse
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

METADATA_V1 = MetadataProxy.from_dict(
    {
        "tx_id": str(uuid.uuid4()),
        "user_id": "789473423",
        "schema_name": "1_0000",
        "collection_exercise_sid": "test-sid",
        "account_service_url": ACCOUNT_SERVICE_BASE_URL_SOCIAL,
        "period_id": "2016-02-01",
        "period_str": "2016-01-01",
        "ref_p_start_date": "2016-02-02",
        "ref_p_end_date": "2016-03-03",
        "ru_ref": "432423423423",
        "response_id": "1234567890123456",
        "ru_name": "Apple",
        "return_by": "2016-07-07",
        "case_id": str(uuid.uuid4()),
        "form_type": "I",
        "case_type": "SPG",
        "region_code": "GB-ENG",
        "channel": "RH",
        "display_address": "68 Abingdon Road, Goathill",
        "case_ref": "1000000000000001",
        "jti": str(uuid.uuid4()),
        "response_expires_at": get_response_expires_at(),
    }
)

METADATA_V2 = MetadataProxy.from_dict(
    {
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
                "ru_ref": "432423423423",
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
)


def get_questionnaire_store(version):
    user_answer = Answer(answer_id="GHI", value=0, list_item_id=None)

    storage = MagicMock()
    storage.get_user_data = MagicMock(return_value=("{}", "ce_sid", 1, None))
    storage.add_or_update = MagicMock()

    store = QuestionnaireStore(storage)

    store.answer_store = AnswerStore()
    store.supplementary_data_store = SupplementaryDataStore()
    store.answer_store.add_or_update(user_answer)
    store.metadata = METADATA_V2 if version is AuthPayloadVersion.V2 else METADATA_V1
    store.response_metadata = {"started_at": "2018-07-04T14:49:33.448608+00:00"}

    return store


@pytest.fixture
def fake_metadata():
    return METADATA_V1


@pytest.fixture
def fake_metadata_v2():
    return METADATA_V2


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
    blob = Blob(name="some-blob", bucket=mocker.Mock())

    response_503 = Response()
    response_503.status_code = 503

    response_200 = Response()
    response_200._content = (  # pylint: disable=protected-access
        b'{"some-key":"some-value"}'
    )
    response_200.status_code = 200

    mock_transport_request = mocker.Mock(
        side_effect=[InvalidResponse(response_503), response_200]
    )
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
