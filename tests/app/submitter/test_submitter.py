import uuid
from unittest import TestCase

from mock import Mock, call, patch
from pika.exceptions import AMQPError

from app.submitter import GCSFeedbackSubmitter, GCSSubmitter, RabbitMQSubmitter


class TestRabbitMQSubmitter(TestCase):
    def setUp(self):
        self.queue = "test_queue"
        self.host1 = "host1"
        self.host2 = "host2"
        self.port = 5672

        self.submitter = RabbitMQSubmitter(
            host=self.host1, secondary_host=self.host2, port=self.port, queue=self.queue
        )

    def test_when_fail_to_connect_to_queue_then_published_false(self):
        # Given
        with patch("app.submitter.submitter.BlockingConnection") as connection:
            connection.side_effect = AMQPError()

            # When
            published = self.submitter.send_message(
                message={},
                tx_id="123",
                questionnaire_id="0123456789000000",
                case_id="456",
            )

            # Then
            self.assertFalse(published, "send_message should fail to publish message")

    def test_when_message_sent_then_published_true(self):
        # Given
        with patch("app.submitter.submitter.BlockingConnection"):
            published = self.submitter.send_message(
                message={},
                tx_id="123",
                questionnaire_id="0123456789000000",
                case_id="456",
            )

            # When

            # Then
            self.assertTrue(published, "send_message should publish message")

    def test_when_first_connection_fails_then_secondary_succeeds(self):
        # Given
        with patch("app.submitter.submitter.BlockingConnection") as connection, patch(
            "app.submitter.submitter.URLParameters"
        ) as url_parameters:
            secondary_connection = Mock()
            connection.side_effect = [AMQPError(), secondary_connection]

            # When
            published = self.submitter.send_message(
                message={},
                tx_id="12345",
                questionnaire_id="0123456789000000",
                case_id="456",
            )

            # Then
            self.assertTrue(published, "send_message should publish message")
            # Check we create url for primary then secondary
            url_parameters_calls = [
                call("amqp://{}:{}/%2F".format(self.host1, self.port)),
                call("amqp://{}:{}/%2F".format(self.host2, self.port)),
            ]
            url_parameters.assert_has_calls(url_parameters_calls)
            # Check we create connection twice, failing first then with self.url2
            self.assertEqual(connection.call_count, 2)

    def test_url_generation_with_credentials(self):
        # Given
        with patch("app.submitter.submitter.BlockingConnection") as connection, patch(
            "app.submitter.submitter.URLParameters"
        ) as url_parameters:
            secondary_connection = Mock()
            connection.side_effect = [AMQPError(), secondary_connection]

            username = "testUsername"
            password = str(uuid.uuid4())

            submitter = RabbitMQSubmitter(
                host=self.host1,
                secondary_host=self.host2,
                port=self.port,
                queue=self.queue,
                username=username,
                password=password,
            )

            # When
            published = submitter.send_message(
                message={},
                tx_id="12345",
                questionnaire_id="0123456789000000",
                case_id="456",
            )

            # Then
            self.assertTrue(published, "send_message should publish message")
            # Check we create url for primary then secondary
            url_parameters_calls = [
                call(
                    "amqp://{}:{}@{}:{}/%2F".format(
                        username, password, self.host1, self.port
                    )
                ),
                call(
                    "amqp://{}:{}@{}:{}/%2F".format(
                        username, password, self.host2, self.port
                    )
                ),
            ]
            url_parameters.assert_has_calls(url_parameters_calls)
            # Check we create connection twice, failing first then with self.url2
            self.assertEqual(connection.call_count, 2)

    def test_when_fail_to_disconnect_then_log_warning_message(self):
        # Given
        connection = Mock()
        error = AMQPError()
        connection.close.side_effect = [error]

        with patch(
            "app.submitter.submitter.BlockingConnection", return_value=connection
        ), patch("app.submitter.submitter.logger") as logger:
            # When
            published = self.submitter.send_message(
                message={},
                tx_id="123",
                questionnaire_id="0123456789000000",
                case_id="456",
            )

            # Then
            self.assertTrue(published)
            logger.error.assert_called_once_with(
                "unable to close connection", category="rabbitmq", exc_info=error
            )

    def test_when_fail_to_publish_message_then_returns_false(self):
        # Given
        channel = Mock()
        channel.basic_publish = Mock(return_value=False)
        connection = Mock()
        connection.channel.side_effect = Mock(return_value=channel)
        with patch(
            "app.submitter.submitter.BlockingConnection", return_value=connection
        ):
            # When
            published = self.submitter.send_message(
                message={},
                tx_id="123",
                questionnaire_id="0123456789000000",
                case_id="456",
            )

            # Then
            self.assertFalse(published, "send_message should fail to publish message")

    def test_when_message_sent_then_metadata_is_sent_in_header(self):
        # Given
        channel = Mock()
        connection = Mock()
        connection.channel.side_effect = Mock(return_value=channel)
        with patch(
            "app.submitter.submitter.BlockingConnection", return_value=connection
        ):
            # When
            self.submitter.send_message(
                message={},
                tx_id="12345",
                questionnaire_id="0123456789000000",
                case_id="98765",
            )

            # Then
            call_args = channel.basic_publish.call_args
            properties = call_args[1]["properties"]
            headers = properties.headers
            self.assertEqual(headers["tx_id"], "12345")
            self.assertEqual(headers["questionnaire_id"], "0123456789000000")
            self.assertEqual(headers["case_id"], "98765")

    def test_when_message_sent_then_case_id_not_in_header_if_missing(self):
        # Given
        channel = Mock()
        connection = Mock()
        connection.channel.side_effect = Mock(return_value=channel)
        with patch(
            "app.submitter.submitter.BlockingConnection", return_value=connection
        ):
            # When
            self.submitter.send_message(
                message={}, tx_id="12345", questionnaire_id="0123456789000000"
            )

            # Then
            call_args = channel.basic_publish.call_args
            properties = call_args[1]["properties"]
            headers = properties.headers
            self.assertEqual(headers["tx_id"], "12345")
            self.assertEqual(headers["questionnaire_id"], "0123456789000000")


class TestGCSSubmitter(TestCase):
    @staticmethod
    def test_send_message():
        with patch("app.submitter.submitter.storage.Client") as client:
            # Given
            submitter = GCSSubmitter(bucket_name="test_bucket")

            # When
            published = submitter.send_message(
                message={"test_data"},
                tx_id="123",
                questionnaire_id="0123456789000000",
                case_id="456",
            )

            # Then
            bucket = client.return_value.get_bucket.return_value
            blob = bucket.blob.return_value
            assert isinstance(blob.metadata, dict)

            blob_name = bucket.blob.call_args[0][0]
            assert blob_name == "123"

            blob_contents = blob.upload_from_string.call_args[0][0]
            assert blob_contents == b"{'test_data'}"

            assert published is True

    @staticmethod
    def test_send_message_adds_metadata():
        with patch("app.submitter.submitter.storage.Client") as client:
            # Given
            submitter = GCSSubmitter(bucket_name="test_bucket")

            # When
            submitter.send_message(
                message={"test_data"},
                tx_id="123",
                questionnaire_id="0123456789000000",
                case_id="456",
            )

            # Then
            bucket = client.return_value.get_bucket.return_value
            blob = bucket.blob.return_value

            assert blob.metadata == {
                "tx_id": "123",
                "questionnaire_id": "0123456789000000",
                "case_id": "456",
            }


class TestGCSFeedbackSubmitter(TestCase):
    @staticmethod
    @patch("app.submitter.submitter.storage.Client")
    def test_upload_feedback(client):
        # Given
        feedback = GCSFeedbackSubmitter(bucket_name="feedback")

        metadata = {
            "feedback_count": 1,
            "feedback_submission_date": "2021-03-23",
            "form_type": "H",
            "language_code": "cy",
            "region_code": "GB-ENG",
            "tx_id": "12345",
        }

        payload = {
            "feedback-type": "Feedback type",
            "feedback-text": "Feedback text",
        }

        # When
        feedback_upload = feedback.upload(metadata, payload)

        # Then
        bucket = client.return_value.get_bucket.return_value
        blob = bucket.blob.return_value

        assert blob.metadata["feedback_count"] == 1
        assert blob.metadata["feedback_submission_date"] == "2021-03-23"
        assert blob.metadata["form_type"] == "H"
        assert blob.metadata["language_code"] == "cy"
        assert blob.metadata["tx_id"] == "12345"
        assert blob.metadata["region_code"] == "GB-ENG"

        blob_contents = blob.upload_from_string.call_args[0][0]

        assert (
            blob_contents
            == b'{"feedback-type": "Feedback type", "feedback-text": "Feedback text", '
            b'"feedback_count": 1, "feedback_submission_date": "2021-03-23", '
            b'"form_type": "H", "language_code": "cy", "region_code": "GB-ENG", "tx_id": "12345"}'
        )
        assert feedback_upload is True
