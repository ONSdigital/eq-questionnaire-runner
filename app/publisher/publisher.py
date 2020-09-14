from abc import ABC, abstractmethod

import google
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.futures import Future
from structlog import get_logger

from app.publisher.publication_failed import PublicationFailed

logger = get_logger(__name__)


class Publisher(ABC):
    @abstractmethod
    def publish(self, topic_id, message):
        pass  # pragma: no cover


class PubSub(Publisher):
    def __init__(self):
        self._client = PublisherClient()
        _, self._project_id = google.auth.default()

    def _publish(self, topic_id, message):
        logger.info("publishing message", topic_id=topic_id)
        topic_path = self._client.topic_path(self._project_id, topic_id)
        publish_future: Future = self._client.publish(topic_path, message)
        return publish_future

    def publish(self, topic_id, message: bytes):
        publish_future = self._publish(topic_id, message)
        try:
            # Resolve the future
            message_id = publish_future.result()
            logger.info(  # pragma: no cover
                "message published successfully",
                topic_id=topic_id,
                message_id=message_id,
            )
        except Exception as ex:  # pylint:disable=broad-except
            logger.error(
                "message publication failed",
                topic_id=topic_id,
                exc_info=ex,
            )
            raise PublicationFailed(ex)


class LogPublisher(Publisher):
    def publish(self, topic_id, message: bytes):
        logger.info("publishing message", topic_id=topic_id, message=message)
