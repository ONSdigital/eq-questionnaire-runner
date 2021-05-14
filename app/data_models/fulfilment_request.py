from abc import ABC, abstractmethod
from datetime import datetime
from functools import cached_property
from typing import Mapping
from uuid import uuid4

from dateutil.tz import tzutc

from app.utilities.simplejson import dumps_json


class FulfilmentRequest(ABC):
    @abstractmethod
    def _payload(self) -> Mapping:
        pass  # pragma: no cover

    @cached_property
    def transaction_id(self) -> str:
        return str(uuid4())

    @property
    def message(self) -> bytes:
        message = {
            "event": {
                "type": "FULFILMENT_REQUESTED",
                "source": "QUESTIONNAIRE_RUNNER",
                "channel": "EQ",
                "dateTime": datetime.now(tz=tzutc()).isoformat(),
                "transactionId": self.transaction_id,
            },
            "payload": self._payload(),
        }
        return dumps_json(message).encode("utf-8")
