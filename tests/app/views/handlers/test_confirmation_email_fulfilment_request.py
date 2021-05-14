import json
from datetime import datetime

import pytest
from dateutil.tz import tzutc
from freezegun import freeze_time

from app.data_models.session_data import SessionData
from app.questionnaire import QuestionnaireSchema
from app.utilities.simplejson import loads_json
from app.views.handlers.confirm_email import ConfirmationEmailFulfilmentRequest

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
    return QuestionnaireSchema(
        {
            "form_type": "H",
            "region_code": "GB-WLS",
            "submission": {"confirmation_email": True},
        }
    )


@freeze_time(time_to_freeze)
def test_confirmation_email_fulfilment_request_message(session_data, schema):
    email_address = "name@example.com"
    fulfilment_request = ConfirmationEmailFulfilmentRequest(
        email_address, session_data, schema
    )

    confirmation_email_json_message = loads_json(fulfilment_request.message)

    expected_payload = {
        "email_address": "name@example.com",
        "display_address": "68 Abingdon Road, Goathill",
        "form_type": schema.form_type,
        "language_code": session_data.language_code,
        "region_code": schema.region_code,
        "questionnaire_id": session_data.questionnaire_id,
        "tx_id": session_data.tx_id,
    }

    assert (
        confirmation_email_json_message["payload"]["fulfilmentRequest"]
        == expected_payload
    )
