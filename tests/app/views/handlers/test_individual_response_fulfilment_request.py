from datetime import datetime, timezone
from uuid import uuid4

import pytest
from freezegun import freeze_time

from app.data_models.metadata_proxy import MetadataProxy
from app.forms.validators import sanitise_mobile_number
from app.helpers.uuid_helper import is_valid_uuid4
from app.utilities.json import json_loads
from app.views.handlers.individual_response import (
    GB_ENG_REGION_CODE,
    GB_NIR_REGION_CODE,
    GB_WLS_REGION_CODE,
    IndividualResponseFulfilmentRequest,
)
from tests.app.parser.conftest import get_response_expires_at

DUMMY_MOBILE_NUMBER = "07700900258"


@freeze_time(datetime.now(tz=timezone.utc).isoformat())
def test_sms_fulfilment_request_payload():
    metadata = MetadataProxy(
        region_code="GB-ENG",
        case_id=str(uuid4()),
        tx_id="tx_id",
        response_id="response_id",
        account_service_url="account_service_url",
        collection_exercise_sid="collection_exercise_sid",
        response_expires_at=get_response_expires_at(),
    )

    fulfilment_request = IndividualResponseFulfilmentRequest(
        metadata, DUMMY_MOBILE_NUMBER
    )

    sms_json_message = json_loads(fulfilment_request.message)
    payload = sms_json_message["payload"]
    validate_uuids_in_payload(payload)

    expected_sms_payload = {
        "fulfilmentRequest": {
            "fulfilmentCode": "UACITA1",
            "contact": {"telNo": sanitise_mobile_number(DUMMY_MOBILE_NUMBER)},
        }
    }
    assert sms_json_message["payload"] == expected_sms_payload


@freeze_time(datetime.now(tz=timezone.utc).isoformat())
def test_postal_fulfilment_request_message():
    metadata = {
        "region_code": "GB-ENG",
        "case_id": str(uuid4()),
        "tx_id": "tx_id",
        "response_id": "response_id",
        "account_service_url": "account_service_url",
        "collection_exercise_sid": "collection_exercise_sid",
    }

    metadata = MetadataProxy.from_dict(metadata)

    fulfilment_request = IndividualResponseFulfilmentRequest(metadata)

    postal_json_message = json_loads(fulfilment_request.message)
    payload = postal_json_message["payload"]
    validate_uuids_in_payload(payload)

    expected_sms_payload = {
        "fulfilmentRequest": {
            "fulfilmentCode": "P_UAC_UACIPA1",
            "contact": {},
        }
    }
    assert payload == expected_sms_payload


def validate_uuids_in_payload(payload):
    individual_case_id = payload["fulfilmentRequest"].pop("individualCaseId")
    case_id = payload["fulfilmentRequest"].pop("caseId")

    assert is_valid_uuid4(individual_case_id) is True
    assert is_valid_uuid4(case_id) is True


@freeze_time(datetime.now(tz=timezone.utc).isoformat())
def test_individual_case_id_not_present_when_case_type_spg():
    metadata = {
        "region_code": "GB-ENG",
        "case_id": str(uuid4()),
        "tx_id": "tx_id",
        "response_id": "response_id",
        "account_service_url": "account_service_url",
        "collection_exercise_sid": "collection_exercise_sid",
        "survey_metadata": {
            "data": {
                "case_type": "SPG",
            }
        },
    }

    metadata = MetadataProxy.from_dict(metadata)

    fulfilment_request = IndividualResponseFulfilmentRequest(metadata)

    json_message = json_loads(fulfilment_request.message)
    assert "individualCaseId" not in json_message["payload"]["fulfilmentRequest"]


@freeze_time(datetime.now(tz=timezone.utc).isoformat())
def test_individual_case_id_not_present_when_case_type_ce():
    metadata = {
        "region_code": "GB-ENG",
        "case_id": str(uuid4()),
        "tx_id": "tx_id",
        "response_id": "response_id",
        "account_service_url": "account_service_url",
        "collection_exercise_sid": "collection_exercise_sid",
        "survey_metadata": {
            "data": {
                "case_type": "CE",
            }
        },
    }

    metadata = MetadataProxy.from_dict(metadata)

    fulfilment_request = IndividualResponseFulfilmentRequest(metadata)

    json_message = json_loads(fulfilment_request.message)
    assert "individualCaseId" not in json_message["payload"]["fulfilmentRequest"]


@pytest.mark.parametrize(
    "region_code, expected_fulfilment_code",
    [
        (GB_ENG_REGION_CODE, "UACITA1"),
        (GB_WLS_REGION_CODE, "UACITA2B"),
        (GB_NIR_REGION_CODE, "UACITA4"),
    ],
)
def test_fulfilment_code_for_sms(region_code, expected_fulfilment_code):
    metadata = {
        "region_code": region_code,
        "case_id": str(uuid4()),
        "case_type": "SPG",
        "tx_id": "tx_id",
        "response_id": "response_id",
        "account_service_url": "account_service_url",
        "collection_exercise_sid": "collection_exercise_sid",
    }

    metadata = MetadataProxy.from_dict(metadata)

    fulfilment_request = IndividualResponseFulfilmentRequest(
        metadata, DUMMY_MOBILE_NUMBER
    )
    json_message = json_loads(fulfilment_request.message)
    assert (
        json_message["payload"]["fulfilmentRequest"]["fulfilmentCode"]
        == expected_fulfilment_code
    )


@pytest.mark.parametrize(
    "region_code, expected_fulfilment_code",
    [
        (GB_ENG_REGION_CODE, "P_UAC_UACIPA1"),
        (GB_WLS_REGION_CODE, "P_UAC_UACIPA2B"),
        (GB_NIR_REGION_CODE, "P_UAC_UACIPA4"),
    ],
)
def test_fulfilment_code_for_postal(region_code, expected_fulfilment_code):
    metadata = {
        "region_code": region_code,
        "case_id": str(uuid4()),
        "case_type": "SPG",
        "tx_id": "tx_id",
        "response_id": "response_id",
        "account_service_url": "account_service_url",
        "collection_exercise_sid": "collection_exercise_sid",
    }

    metadata = MetadataProxy.from_dict(metadata)

    fulfilment_request = IndividualResponseFulfilmentRequest(metadata)

    json_message = json_loads(fulfilment_request.message)

    assert (
        json_message["payload"]["fulfilmentRequest"]["fulfilmentCode"]
        == expected_fulfilment_code
    )
