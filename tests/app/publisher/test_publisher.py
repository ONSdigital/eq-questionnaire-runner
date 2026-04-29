from unittest import TestCase
from unittest.mock import Mock, patch, sentinel
from uuid import uuid4

from app.publisher import PubSubPublisher
from app.publisher.exceptions import PublicationFailed


class TestPubSub(TestCase):
    topic_id = "test-topic-id"
    topic_path = f"projects/test-project-id/topics/{topic_id}"

    def setUp(self) -> None:
        with patch(
            "app.publisher.publisher.google.auth._default._get_explicit_environ_credentials",
            return_value=(Mock(), "test-project-id"),
        ):
            self.publisher = PubSubPublisher()

    # pylint: disable=protected-access
    def test_publish(self):
        self.publisher._client.publish = Mock(return_value=sentinel.future)

        # Publish message.
        future = self.publisher._publish(self.topic_id, b"test-message")
        assert future is sentinel.future

        # Check the client call uses topic path and bytes payload.
        self.publisher._client.publish.assert_called_once_with(self.topic_path, b"test-message")

    def test_resolving_message_raises_exception_on_error(self):
        failing_future = Mock()
        failing_future.result.side_effect = Exception(
            "403 The request is missing a valid API key."
        )
        self.publisher._publish = Mock(return_value=failing_future)

        with self.assertRaises(PublicationFailed) as ex:
            # Resolve a mocked failed future to assert exception wrapping behavior.
            self.publisher.publish(
                self.topic_id,
                b"test-message",
                fulfilment_request_transaction_id=str(uuid4()),
            )

        error_message = str(ex.exception).lower()
        assert "403" in error_message
        assert "api key" in error_message
        self.publisher._publish.assert_called_once_with(self.topic_id, b"test-message")
