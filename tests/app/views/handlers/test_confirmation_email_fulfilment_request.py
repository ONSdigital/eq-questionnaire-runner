from freezegun import freeze_time

from app.utilities.json import json_loads
from app.views.handlers.confirm_email import ConfirmationEmailFulfilmentRequest
from tests.app.views.handlers.conftest import time_to_freeze


@freeze_time(time_to_freeze)
def test_confirmation_email_fulfilment_request_message(
    session_data, metadata, confirmation_email_fulfilment_schema
):
    email_address = "name@example.com"

    fulfilment_request = ConfirmationEmailFulfilmentRequest(
        email_address,
        session_data,
        metadata,
        confirmation_email_fulfilment_schema,
    )

    confirmation_email_json_message = json_loads(fulfilment_request.message)

    expected_payload = {
        "email_address": "name@example.com",
        "display_address": metadata["display_address"],
        "form_type": confirmation_email_fulfilment_schema.form_type,
        "language_code": session_data.language_code,
        "region_code": confirmation_email_fulfilment_schema.region_code,
        "tx_id": metadata.tx_id,
    }

    assert (
        confirmation_email_json_message["payload"]["fulfilmentRequest"]
        == expected_payload
    )
