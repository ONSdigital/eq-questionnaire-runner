from freezegun import freeze_time

from app.utilities.json import json_loads
from app.views.handlers.confirm_email import ConfirmationEmailFulfilmentRequest

from .conftest import time_to_freeze


@freeze_time(time_to_freeze)
def test_confirmation_email_fulfilment_request_message(
    fake_questionnaire_store, confirmation_email_fulfilment_schema
):
    email_address = "name@example.com"

    fulfilment_request = ConfirmationEmailFulfilmentRequest(
        email_address,
        fake_questionnaire_store.metadata,
        confirmation_email_fulfilment_schema,
    )

    confirmation_email_json_message = json_loads(fulfilment_request.message)

    expected_payload = {
        "email_address": "name@example.com",
        "display_address": fake_questionnaire_store.metadata["display_address"],
        "form_type": confirmation_email_fulfilment_schema.form_type,
        "language_code": fake_questionnaire_store.metadata["language_code"],
        "region_code": confirmation_email_fulfilment_schema.region_code,
        "tx_id": fake_questionnaire_store.metadata["tx_id"],
    }

    assert (
        confirmation_email_json_message["payload"]["fulfilmentRequest"]
        == expected_payload
    )
