from unittest import TestCase, mock

from google.cloud.pubsub_v1.proto.pubsub_pb2 import PubsubMessage
from mock import Mock, sentinel

from app.publisher.publication_failed import PublicationFailed
from app.publisher.publisher import PubSub


class TestPubSub(TestCase):
    def setUp(self) -> None:
        self.publisher = PubSub(topic_id="test-topic-id")

    def test_pub_sub_topic_path(self):
        assert self.publisher.topic_path == "projects/None/topics/test-topic-id"

    # pylint: disable=protected-access
    def test_publish(self):
        future = sentinel.future
        future.add_done_callback = Mock(spec=["__call__"])

        # Use a mock in lieu of the actual batch class.
        batch = Mock(spec=self.publisher._batch_class)

        # Set the mock up to accepts the message.
        batch.publish.side_effect = (future,)

        self.publisher._set_batch(self.publisher.topic_path, batch)

        # Publish message.
        future = self.publisher._publish(b"test-message")
        assert future is sentinel.future

        # Check mock.
        batch.publish.assert_has_calls([mock.call(PubsubMessage(data=b"test-message"))])

    def test_resolving_message_raises_exception_on_error(self):
        with self.assertRaises(PublicationFailed) as ex:
            # Try resolve the future with an invalid project id.
            self.publisher.publish_and_resolve_message(b"test-message")

        assert (
            "404 Requested project not found or user does not have access to it"
            in str(ex.exception)
        )
