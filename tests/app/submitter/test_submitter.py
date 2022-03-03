import uuid

import pytest
from pika.exceptions import AMQPError, NackError

from app.submitter import GCSFeedbackSubmitter, GCSSubmitter, RabbitMQSubmitter
from app.utilities.json import json_dumps


def test_rabbitmq_submitter_not_published_when_fails_to_connect_to_queue(
    rabbitmq_submitter, patch_blocking_connection
):
    # Given
    patch_blocking_connection.side_effect = AMQPError()

    # When
    published = rabbitmq_submitter.send_message(
        message={},
        tx_id="123",
        case_id="456",
    )

    # Then
    assert not published, "send_message should fail to publish message"


@pytest.mark.usefixtures("patch_blocking_connection")
def test_rabbitmq_submitter_published_when_message_sent(rabbitmq_submitter):
    # Given
    published = rabbitmq_submitter.send_message(
        message={},
        tx_id="123",
        case_id="456",
    )

    # Then
    assert published, "send_message should publish message"


def test_rabbitmq_submitter_secondary_succeeds_first_connection_fails(
    rabbitmq_submitter, patch_blocking_connection, patch_url_parameters, mocker
):
    # Given

    patch_blocking_connection.side_effect = [AMQPError(), mocker.Mock()]

    # When
    published = rabbitmq_submitter.send_message(
        message={},
        tx_id="12345",
        case_id="456",
    )

    # Then
    assert published, "send_message should publish message"
    # Check we create url for primary then secondary
    url_parameters_calls = [
        mocker.call("amqp://host1:5672/%2F"),
        mocker.call("amqp://host2:5672/%2F"),
    ]
    patch_url_parameters.assert_has_calls(url_parameters_calls)
    # Check we create connection twice, failing first then with self.url2
    assert patch_blocking_connection.call_count == 2


def test_rabbitmq_submitter_url_generation_with_credentials(
    patch_blocking_connection, patch_url_parameters, mocker
):
    # Given

    patch_blocking_connection.side_effect = [AMQPError(), mocker.Mock()]

    username = "testUsername"
    password = str(uuid.uuid4())

    submitter = RabbitMQSubmitter(
        host="host1",
        secondary_host="host2",
        port=5672,
        queue="test_queue",
        username=username,
        password=password,
    )

    # When
    published = submitter.send_message(
        message={},
        tx_id="12345",
        case_id="456",
    )

    # Then
    assert published, "send_message should publish message"
    # Check we create url for primary then secondary
    url_parameters_calls = [
        mocker.call(f"amqp://{username}:{password}@host1:5672/%2F"),
        mocker.call(f"amqp://{username}:{password}@host2:5672/%2F"),
    ]
    patch_url_parameters.assert_has_calls(url_parameters_calls)
    # Check we create connection twice, failing first then with self.url2
    assert patch_blocking_connection.call_count == 2


def test_rabbitmq_submitter_log_warning_message_when_fail_to_disconnect(
    rabbitmq_submitter, mocker
):
    # Given
    connection = mocker.Mock()
    error = AMQPError()
    connection.close.side_effect = [error]

    mocker.patch("app.submitter.submitter.BlockingConnection", return_value=connection)
    logger = mocker.patch("app.submitter.submitter.logger")
    # When
    published = rabbitmq_submitter.send_message(
        message={},
        tx_id="123",
        case_id="456",
    )

    # Then
    assert published
    logger.error.assert_called_once_with(
        "unable to close connection", category="rabbitmq", exc_info=error
    )


def test_rabbitmq_submitter_returns_false_when_fail_to_publish_message(
    rabbitmq_submitter, mocker
):
    # Given
    channel = mocker.Mock()
    channel.basic_publish = mocker.Mock(
        side_effect=NackError("Mock exception for basic_publish")
    )
    connection = mocker.Mock()
    connection.channel.side_effect = mocker.Mock(return_value=channel)
    mocker.patch("app.submitter.submitter.BlockingConnection", return_value=connection)
    # When
    published = rabbitmq_submitter.send_message(
        message={},
        tx_id="123",
        case_id="456",
    )

    # Then
    assert not published, "send_message should fail to publish message"


def test_rabbitmq_submitter_metadata_is_sent_in_header_when_message_sent(
    rabbitmq_submitter, mocker
):
    # Given
    channel = mocker.Mock()
    connection = mocker.Mock()
    connection.channel.side_effect = mocker.Mock(return_value=channel)
    mocker.patch("app.submitter.submitter.BlockingConnection", return_value=connection)
    # When
    rabbitmq_submitter.send_message(
        message={},
        tx_id="12345",
        case_id="98765",
    )

    # Then
    call_args = channel.basic_publish.call_args
    properties = call_args[1]["properties"]
    headers = properties.headers
    assert headers["tx_id"] == "12345"
    assert headers["case_id"] == "98765"


def test_gcs_submitter_sends_message(patch_client):
    gcs_submitter = GCSSubmitter(bucket_name="test_bucket")
    # When
    published = gcs_submitter.send_message(
        message={"test_data"},
        tx_id="123",
        case_id="456",
    )

    # Then
    bucket = patch_client.return_value.get_bucket.return_value
    blob = bucket.blob.return_value
    assert isinstance(blob.metadata, dict)

    blob_name = bucket.blob.call_args[0][0]
    assert blob_name == "123"

    blob_contents = blob.upload_from_string.call_args[0][0]
    assert blob_contents == b"{'test_data'}"

    assert published is True


def test_gcs_submitter_adds_metadata_when_sends_message(patch_client):
    gcs_submitter = GCSSubmitter(bucket_name="test_bucket")
    # When
    gcs_submitter.send_message(
        message={"test_data"},
        tx_id="123",
        case_id="456",
    )

    # Then
    bucket = patch_client.return_value.get_bucket.return_value
    blob = bucket.blob.return_value

    assert blob.metadata == {
        "tx_id": "123",
        "case_id": "456",
    }


def test_gcs_feedback_submitter_uploads_feedback(patch_client):
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

    payload.update(metadata)

    # When
    feedback_upload = feedback.upload(metadata, json_dumps(payload))

    # Then
    bucket = patch_client.return_value.get_bucket.return_value
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
