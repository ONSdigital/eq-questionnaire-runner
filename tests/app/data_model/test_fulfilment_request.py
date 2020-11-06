import json
from datetime import datetime
from typing import Mapping

from dateutil.tz import tzutc
from freezegun import freeze_time

from app.data_models import FulfilmentRequest
from app.helpers.uuid_helper import is_valid_uuid

time_to_freeze = datetime.now(tzutc()).replace(second=0, microsecond=0)


class TestFulfilmentRequest(FulfilmentRequest):
    def _payload(self) -> Mapping:
        return {}


@freeze_time(time_to_freeze)
def test_fulfilment_request_message():
    fulfilment_request = TestFulfilmentRequest()

    assert isinstance(fulfilment_request.message, bytes)
    json_message = json.loads(fulfilment_request.message)

    transaction_id = json_message["event"].pop("transactionId")
    assert is_valid_uuid(transaction_id, version=4) is True

    expected_json_message = {
        "event": {
            "type": "FULFILMENT_REQUESTED",
            "source": "QUESTIONNAIRE_RUNNER",
            "channel": "EQ",
            "dateTime": datetime.now(tz=tzutc()).isoformat(),
        },
        "payload": {},
    }

    assert json_message == expected_json_message
