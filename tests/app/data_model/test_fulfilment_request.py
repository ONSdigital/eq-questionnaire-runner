from datetime import datetime, timezone
from typing import Mapping

from freezegun import freeze_time

from app.data_models import FulfilmentRequest
from app.helpers.uuid_helper import is_valid_uuid4
from app.utilities.json import json_loads

time_to_freeze = datetime.now(timezone.utc).replace(second=0, microsecond=0)


class TestFulfilmentRequest(FulfilmentRequest):
    def _payload(self) -> Mapping:
        return {}


@freeze_time(time_to_freeze)
def test_fulfilment_request_message():
    fulfilment_request = TestFulfilmentRequest()

    assert isinstance(fulfilment_request.message, bytes)
    json_message = json_loads(fulfilment_request.message)

    transaction_id = json_message["event"].pop("transactionId")
    assert is_valid_uuid4(transaction_id) is True

    expected_json_message = {
        "event": {
            "type": "FULFILMENT_REQUESTED",
            "source": "QUESTIONNAIRE_RUNNER",
            "channel": "EQ",
            "dateTime": datetime.now(tz=timezone.utc).isoformat(),
        },
        "payload": {},
    }

    assert json_message == expected_json_message
