from abc import ABC, abstractmethod

import google.auth
from google.cloud.pubsub import PublisherClient
from google.cloud.pubsub_v1.futures import Future
from structlog import get_logger

from app.publisher.exceptions import PublicationFailed

logger = get_logger(__name__)


class Publisher(ABC):
    @abstractmethod
    def publish(self, topic_id, message):
        pass  # pragma: no cover


class PubSubPublisher(Publisher):
    def __init__(self):
        self._client = PublisherClient()
        _, self._project_id = google.auth.default()

    def _publish(self, topic_id, message):
        logger.info("publishing message", topic_id=topic_id)
        topic_path = self._client.topic_path(self._project_id, topic_id)
        response: Future = self._client.publish(topic_path, message)
        return response

    def publish(self, topic_id, message: bytes):
        response = self._publish(topic_id, message)
        try:
            # Resolve the future
            message_id = response.result()
            logger.info(  # pragma: no cover
                "message published successfully",
                topic_id=topic_id,
                message_id=message_id,
            )
        except Exception as ex:  # pylint:disable=broad-except
            logger.exception(
                "message publication failed",
                topic_id=topic_id,
            )
            raise PublicationFailed(ex)


class LogPublisher(Publisher):
    def publish(self, topic_id, message: bytes):
        logger.info("publishing message", topic_id=topic_id, message=message)
