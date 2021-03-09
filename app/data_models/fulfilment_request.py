from abc import ABC, abstractmethod
from datetime import datetime
from functools import cached_property
from typing import Mapping
from uuid import uuid4

import simplejson as json
from dateutil.tz import tzutc


class FulfilmentRequest(ABC):
    @abstractmethod
    def _payload(self) -> Mapping:
        pass  # pragma: no cover

    @cached_property
    def transactionId(self) -> str:
        return str(uuid4())

    @property
    def message(self) -> bytes:
        message = {
            "event": {
                "type": "FULFILMENT_REQUESTED",
                "source": "QUESTIONNAIRE_RUNNER",
                "channel": "EQ",
                "dateTime": datetime.now(tz=tzutc()).isoformat(),
                "transactionId": self.transactionId,
            },
            "payload": self._payload(),
        }
        return json.dumps(message).encode("utf-8")
