import json
from datetime import datetime
from uuid import uuid4

import pytest
from dateutil.tz import tzutc
from freezegun import freeze_time

from app.helpers.uuid_helper import is_valid_uuid
from app.views.handlers.individual_response import (
    GB_ENG_REGION_CODE,
    GB_NIR_REGION_CODE,
    GB_WLS_REGION_CODE,
    FulfilmentRequest,
)

DUMMY_MOBILE_NUMBER = "07700900258"


@freeze_time(datetime.utcnow().isoformat())
def test_sms_fulfilment_request_payload():
    metadata = {"region_code": "GB-ENG", "case_id": str(uuid4())}
    fulfilment_request = FulfilmentRequest(metadata, DUMMY_MOBILE_NUMBER)

    assert isinstance(fulfilment_request.payload, bytes)

    sms_json_payload = json.loads(fulfilment_request.payload)
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
    metadata = {"region_code": "GB-ENG", "case_id": str(uuid4())}
    fulfilment_request = FulfilmentRequest(metadata)

    assert isinstance(fulfilment_request.payload, bytes)

    postal_json_payload = json.loads(fulfilment_request.payload)
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
    metadata = {"region_code": "GB-ENG", "case_id": str(uuid4()), "case_type": "SPG"}
    fulfilment_request = FulfilmentRequest(metadata)

    assert isinstance(fulfilment_request.payload, bytes)

    json_payload = json.loads(fulfilment_request.payload)

    assert "individualCaseId" not in json_payload["payload"]["fulfilmentRequest"]


@pytest.mark.parametrize(
    "region_code, expected_fulfilment_code",
    [
        (GB_ENG_REGION_CODE, "UACITA1"),
        (GB_WLS_REGION_CODE, "UACITA2B"),
        (GB_NIR_REGION_CODE, "UACITA4"),
    ],
)
def test_fulfilment_code_for_sms(region_code, expected_fulfilment_code):
    metadata = {"region_code": region_code, "case_id": str(uuid4()), "case_type": "SPG"}
    fulfilment_request = FulfilmentRequest(metadata, DUMMY_MOBILE_NUMBER)
    json_payload = json.loads(fulfilment_request.payload)

    assert (
        json_payload["payload"]["fulfilmentRequest"]["fulfilmentCode"]
        == expected_fulfilment_code
    )


@pytest.mark.parametrize(
    "region_code, expected_fulfilment_code",
    [
        (GB_ENG_REGION_CODE, "P_UAC_UACIP1"),
        (GB_WLS_REGION_CODE, "P_UAC_UACIP2B"),
        (GB_NIR_REGION_CODE, "P_UAC_UACIP4"),
    ],
)
def test_fulfilment_code_for_postal(region_code, expected_fulfilment_code):
    metadata = {"region_code": region_code, "case_id": str(uuid4()), "case_type": "SPG"}
    fulfilment_request = FulfilmentRequest(metadata)
    json_payload = json.loads(fulfilment_request.payload)

    assert (
        json_payload["payload"]["fulfilmentRequest"]["fulfilmentCode"]
        == expected_fulfilment_code
    )
