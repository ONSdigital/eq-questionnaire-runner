import google
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.futures import Future
from structlog import get_logger

from app.publisher.publication_failed import PublicationFailed

logger = get_logger(__name__)


class PubSub(PublisherClient):
    def __init__(self, topic_id):
        super().__init__()

        _, project_id = google.auth.default()
        self.topic_path = super().topic_path(project_id, topic_id)

    def _publish(self, message):
        logger.info("publishing message")
        publish_future: Future = super().publish(self.topic_path, message)

        return publish_future

    def publish_and_resolve_message(self, message: bytes):
        publish_future = self._publish(message)
        try:
            # Resolve the future
            publish_future.result()
        except Exception as ex:  # pylint:disable=broad-except
            raise PublicationFailed(ex)


class LogPublisher:
    @staticmethod
    def publish_and_resolve_message(message):
        logger.info("publishing message")
        logger.info("message", message=message)
