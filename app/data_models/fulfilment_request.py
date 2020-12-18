from abc import ABC, abstractmethod
from datetime import datetime
from typing import Mapping
from uuid import uuid4

import simplejson as json
from dateutil.tz import tzutc


class FulfilmentRequest(ABC):
    @abstractmethod
    def _payload(self) -> Mapping:
        pass  # pragma: no cover

    @property
    def message(self) -> bytes:
        message = {
            "event": {
                "type": "FULFILMENT_REQUESTED",
                "source": "QUESTIONNAIRE_RUNNER",
                "channel": "EQ",
                "dateTime": datetime.now(tz=tzutc()).isoformat(),
                "transactionId": str(uuid4()),
            },
            "payload": self._payload(),
        }
        return json.dumps(message).encode("utf-8")
