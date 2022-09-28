# pylint: disable=redefined-outer-name
import uuid

import pytest
from google.cloud.storage import Blob
from google.resumable_media import InvalidResponse
from mock import MagicMock
from requests import Response

from app.data_models import QuestionnaireStore
from app.data_models.answer import Answer
from app.data_models.answer_store import AnswerStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.settings import ACCOUNT_SERVICE_BASE_URL_SOCIAL
from app.submitter import RabbitMQSubmitter
from app.utilities.metadata_parser import validate_runner_claims
from app.utilities.metadata_parser_v2 import (
    validate_questionnaire_claims,
    validate_runner_claims_v2,
)


@pytest.fixture
def fake_metadata():
    def parse_metadata(claims, schema_metadata):
        runner_claims = validate_runner_claims(claims)
        questionnaire_claims = validate_questionnaire_claims(claims, schema_metadata)
        return {**runner_claims, **questionnaire_claims}

    schema_metadata = [
        {"name": "user_id", "type": "string"},
        {"name": "period_id", "type": "string"},
        {"name": "ref_p_start_date", "type": "string"},
        {"name": "ref_p_end_date", "type": "string"},
        {"name": "display_address", "type": "string"},
        {"name": "case_ref", "type": "string"},
    ]

    metadata = parse_metadata(
        {
            "tx_id": str(uuid.uuid4()),
            "user_id": "789473423",
            "schema_name": "1_0000",
            "collection_exercise_sid": "test-sid",
            "account_service_url": f"{ACCOUNT_SERVICE_BASE_URL_SOCIAL}/",
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
        },
        schema_metadata,
    )

    return metadata


@pytest.fixture
def fake_metadata_v2():
    def parse_metadata_v2(claims, schema_metadata):
        runner_claims = validate_runner_claims_v2(claims)
        questionnaire_claims = validate_questionnaire_claims(
            claims["survey_metadata"]["data"], schema_metadata
        )

        for key, value in questionnaire_claims.items():
            runner_claims["survey_metadata"]["data"][key] = value

        return runner_claims

    schema_metadata = [
        {"name": "user_id", "type": "string"},
        {"name": "period_id", "type": "string"},
        {"name": "ref_p_start_date", "type": "string"},
        {"name": "ref_p_end_date", "type": "string"},
        {"name": "display_address", "type": "string"},
        {"name": "case_ref", "type": "string"},
    ]

    metadata = parse_metadata_v2(
        {
            "version": "v2",
            "tx_id": str(uuid.uuid4()),
            "schema_name": "1_0000",
            "collection_exercise_sid": "test-sid",
            "account_service_url": f"{ACCOUNT_SERVICE_BASE_URL_SOCIAL}/",
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
        },
        schema_metadata,
    )

    return metadata


@pytest.fixture
def fake_response_metadata():
    response_metadata = {"started_at": "2018-07-04T14:49:33.448608+00:00"}
    return response_metadata


@pytest.fixture
def fake_questionnaire_store_v2(fake_metadata_v2, fake_response_metadata):
    user_answer = Answer(answer_id="GHI", value=0, list_item_id=None)

    storage = MagicMock()
    storage.get_user_data = MagicMock(return_value=("{}", "ce_sid", 1, None))
    storage.add_or_update = MagicMock()

    store = QuestionnaireStore(storage)

    store.answer_store = AnswerStore()
    store.answer_store.add_or_update(user_answer)
    store.metadata = MetadataProxy.from_dict(fake_metadata_v2)
    store.response_metadata = fake_response_metadata

    return store


@pytest.fixture
def fake_questionnaire_store(fake_metadata, fake_response_metadata):
    user_answer = Answer(answer_id="GHI", value=0, list_item_id=None)

    storage = MagicMock()
    storage.get_user_data = MagicMock(return_value=("{}", "ce_sid", 1, None))
    storage.add_or_update = MagicMock()

    store = QuestionnaireStore(storage)

    store.answer_store = AnswerStore()
    store.answer_store.add_or_update(user_answer)
    store.metadata = MetadataProxy.from_dict(fake_metadata)
    store.response_metadata = fake_response_metadata

    return store


@pytest.fixture
def fake_questionnaire_store_no_ref_p_end_date():
    user_answer = Answer(answer_id="GHI", value=0, list_item_id=None)

    storage = MagicMock()
    storage.get_user_data = MagicMock(return_value=("{}", "ce_sid", 1, None))
    storage.add_or_update = MagicMock()

    store = QuestionnaireStore(storage)

    store.answer_store = AnswerStore()
    store.answer_store.add_or_update(user_answer)
    store.metadata = MetadataProxy.from_dict(
        {
            "response_id": "1",
            "account_service_url": "account_service_url",
            "tx_id": "tx_id",
            "collection_exercise_sid": "collection_exercise_sid",
            "case_id": "case_id",
        }
    )

    return store


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
