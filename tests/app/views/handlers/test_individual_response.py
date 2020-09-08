# pylint: disable=protected-access

import json
from datetime import datetime
from unittest.mock import MagicMock, Mock
from uuid import uuid4

import pytest
from dateutil.tz import tzutc
from freezegun import freeze_time

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress_store import ProgressStore
from app.data_models.questionnaire_store import QuestionnaireStore
from app.helpers.uuid_helper import is_valid_uuid
from app.views.handlers import IndividualResponseHandler
from app.views.handlers.individual_response import (
    GB_ENG_REGION_CODE,
    GB_NIR_REGION_CODE,
    GB_WLS_REGION_CODE,
)

DUMMY_MOBILE_NUMBER = "07700900258"


def get_questionnaire_store_mock(metadata):
    metadata = metadata or {}
    answer_store = MagicMock(spec=AnswerStore)
    progress_store = MagicMock(spec=ProgressStore)
    progress_store.locations = list()
    list_store = MagicMock(spec=ListStore)
    questionnaire_store = MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        metadata={"region_code": "GB-ENG", "case_id": str(uuid4()), **metadata},
    )

    return questionnaire_store


def get_individual_response_handler(metadata=None):
    individual_response = IndividualResponseHandler(
        block_definition=None,
        schema=MagicMock(),
        questionnaire_store=get_questionnaire_store_mock(metadata),
        language=Mock(),
        request_args={},
        form_data=Mock(),
        list_item_id=None,
    )

    return individual_response


@freeze_time(datetime.utcnow().isoformat())
def test_sms_fulfilment_request_payload():
    individual_response_handler = get_individual_response_handler()
    sms_payload = individual_response_handler._get_fulfilment_request_payload(
        mobile_number=DUMMY_MOBILE_NUMBER
    )
    assert isinstance(sms_payload, bytes)

    sms_json_payload = json.loads(sms_payload)
    transaction_id = sms_json_payload["event"].pop("transactionId")
    individual_case_id = sms_json_payload["payload"]["fulfilmentRequest"].pop(
        "individualCaseId"
    )
    case_id = sms_json_payload["payload"]["fulfilmentRequest"].pop("caseId")

    assert is_valid_uuid(transaction_id, version=4) is True
    assert is_valid_uuid(individual_case_id, version=4) is True
    assert is_valid_uuid(case_id, version=4) is True

    expected_sms_payload = {
        "event": {
            "type": "FULFILMENT_REQUESTED",
            "source": "QUESTIONNAIRE_RUNNER",
            "channel": "EQ",
            "dateTime": datetime.now(tz=tzutc()).isoformat(),
        },
        "payload": {
            "fulfilmentRequest": {
                "fulfilmentCode": "UACITA1",
                "contact": {"telNo": DUMMY_MOBILE_NUMBER},
            }
        },
    }
    assert sms_json_payload == expected_sms_payload


@freeze_time(datetime.utcnow().isoformat())
def test_postal_fulfilment_request_payload():
    individual_response_handler = get_individual_response_handler()
    postal_payload = individual_response_handler._get_fulfilment_request_payload()
    assert isinstance(postal_payload, bytes)

    postal_json_payload = json.loads(postal_payload)
    transaction_id = postal_json_payload["event"].pop("transactionId")
    individual_case_id = postal_json_payload["payload"]["fulfilmentRequest"].pop(
        "individualCaseId"
    )
    case_id = postal_json_payload["payload"]["fulfilmentRequest"].pop("caseId")

    assert is_valid_uuid(transaction_id, version=4) is True
    assert is_valid_uuid(individual_case_id, version=4) is True
    assert is_valid_uuid(case_id, version=4) is True

    expected_sms_payload = {
        "event": {
            "type": "FULFILMENT_REQUESTED",
            "source": "QUESTIONNAIRE_RUNNER",
            "channel": "EQ",
            "dateTime": datetime.now(tz=tzutc()).isoformat(),
        },
        "payload": {
            "fulfilmentRequest": {
                "fulfilmentCode": "P_UAC_UACIP1",
                "contact": {},
            }
        },
    }
    assert postal_json_payload == expected_sms_payload


@freeze_time(datetime.utcnow().isoformat())
def test_individual_case_id_not_present_when_case_type_spg():
    individual_response_handler = get_individual_response_handler(
        metadata={"case_type": "SPG"}
    )
    payload = individual_response_handler._get_fulfilment_request_payload()
    assert isinstance(payload, bytes)

    sms_json_payload = json.loads(payload)

    assert "individualCaseId" not in sms_json_payload["payload"]["fulfilmentRequest"]


@pytest.mark.parametrize(
    "region_code, expected_fulfilment_code",
    [
        (GB_ENG_REGION_CODE, "UACITA1"),
        (GB_WLS_REGION_CODE, "UACITA2B"),
        (GB_NIR_REGION_CODE, "UACITA4"),
    ],
)
def test_fulfilment_code(region_code, expected_fulfilment_code):
    individual_response_handler = get_individual_response_handler(
        metadata={"region_code": region_code}
    )
    fulfilment_code = individual_response_handler._get_fulfilment_code(
        mobile_number=DUMMY_MOBILE_NUMBER
    )

    assert fulfilment_code == expected_fulfilment_code


@pytest.mark.parametrize(
    "region_code, expected_fulfilment_code",
    [
        (GB_ENG_REGION_CODE, "P_UAC_UACIP1"),
        (GB_WLS_REGION_CODE, "P_UAC_UACIP2B"),
        (GB_NIR_REGION_CODE, "P_UAC_UACIP4"),
    ],
)
def test_fulfilment_code_for_postal(region_code, expected_fulfilment_code):
    individual_response_handler = get_individual_response_handler(
        metadata={"region_code": region_code}
    )
    fulfilment_code = individual_response_handler._get_fulfilment_code()

    assert fulfilment_code == expected_fulfilment_code
