import json
from datetime import datetime

import pytest
from dateutil.tz import tzutc
from freezegun import freeze_time

from app.data_models.session_data import SessionData
from app.helpers.uuid_helper import is_valid_uuid
from app.questionnaire import QuestionnaireSchema
from app.views.handlers.confirmation_email import ConfirmationEmailFulfilmentRequest

time_to_freeze = datetime.now(tzutc()).replace(second=0, microsecond=0)


@pytest.fixture()
@freeze_time(time_to_freeze)
def session_data():
    return SessionData(
        tx_id="123",
        schema_name="some_schema_name",
        display_address="68 Abingdon Road, Goathill",
        period_str=None,
        language_code="cy",
        launch_language_code="en",
        survey_url=None,
        ru_name=None,
        ru_ref=None,
        submitted_time=datetime.now(tzutc()).isoformat(),
        response_id="321",
        questionnaire_id="987",
        case_id="789",
    )


@pytest.fixture()
def schema():
    return QuestionnaireSchema({"form_type": "H", "region_code": "GB-WLS"})


@freeze_time(time_to_freeze)
def test_confirmation_email_fulfilment_request_payload(session_data, schema):
    email_address = "name@example.com"
    fulfilment_request = ConfirmationEmailFulfilmentRequest(
        email_address, session_data, schema
    )

    assert isinstance(fulfilment_request.payload, bytes)

    confirmation_email_json_payload = json.loads(fulfilment_request.payload)

    transaction_id = confirmation_email_json_payload["event"].pop("transactionId")
    assert is_valid_uuid(transaction_id, version=4) is True

    expected_payload = {
        "event": {
            "type": "FULFILMENT_REQUESTED",
            "source": "QUESTIONNAIRE_RUNNER",
            "channel": "EQ",
            "dateTime": datetime.now(tz=tzutc()).isoformat(),
        },
        "payload": {
            "fulfilmentRequest": {
                "email_address": email_address,
                "form_type": "H",
                "region_code": "GB-WLS",
                "questionnaire_id": "987",
                "tx_id": "123",
                "language_code": "cy",
                "display_address": "68 Abingdon Road, Goathill",
                "submitted_at": datetime.now(tz=tzutc()).isoformat(),
            }
        },
    }

    assert confirmation_email_json_payload == expected_payload
