from abc import ABC, abstractmethod
from typing import Any

import google.auth
from google.cloud.pubsub import PublisherClient
from google.cloud.pubsub_v1 import publisher
from google.cloud.pubsub_v1.futures import Future
from structlog import get_logger

from app.publisher.exceptions import PublicationFailed

logger = get_logger(__name__)


class Publisher(ABC):
    @abstractmethod
    def publish(
        self, topic_id: str, message: bytes, fulfilment_request_transaction_id: str
    ) -> None:
        pass  # pragma: no cover


class PubSubPublisher(Publisher):
    def __init__(self) -> None:
        self._client = PublisherClient()
        _, self._project_id = google.auth.default()

    def _publish(self, topic_id: str, message: bytes) -> "publisher.futures.Future":
        logger.info("publishing message", topic_id=topic_id)
        topic_path = self._client.topic_path(self._project_id, topic_id)
        response: Future = self._client.publish(topic_path, message)
        return response

    def publish(
        self, topic_id: str, message: bytes, fulfilment_request_transaction_id: str
    ) -> None:
        response = self._publish(topic_id, message)
        try:
            # Resolve the future
            message_id = response.result()
            logger.info(  # pragma: no cover
                "message published successfully",
                topic_id=topic_id,
                message_id=message_id,
                fulfilment_request_transaction_id=fulfilment_request_transaction_id,
            )
        except Exception as exc:
            logger.exception(
                "message publication failed",
                topic_id=topic_id,
            )
            raise PublicationFailed(exc) from exc


class LogPublisher(Publisher):
    def publish(
        self, topic_id: str, message: bytes, fulfilment_request_transaction_id: str
    ) -> None:
        logger.info(
            "publishing message",
            topic_id=topic_id,
            message=message,
            fulfilment_request_transaction_id=fulfilment_request_transaction_id,
        )
