from uuid import uuid4

from google.cloud import storage  # type: ignore
from pika import BasicProperties, BlockingConnection, URLParameters
from pika.exceptions import AMQPError, NackError, UnroutableError
from structlog import get_logger

from app.utilities.json import json_dumps

logger = get_logger()


class LogSubmitter:
    @staticmethod
    def send_message(message, tx_id, case_id):
        logger.info("sending message")
        logger.info(
            "message payload",
            message=message,
            case_id=case_id,
            tx_id=tx_id,
        )

        return True


class GCSSubmitter:
    def __init__(self, bucket_name):
        client = storage.Client()
        self.bucket = client.get_bucket(bucket_name)

    def send_message(self, message, tx_id, case_id):
        logger.info("sending message")

        blob = self.bucket.blob(tx_id)
        blob.metadata = {"tx_id": tx_id, "case_id": case_id}
        blob.upload_from_string(str(message).encode("utf8"))

        return True


class RabbitMQSubmitter:
    def __init__(self, host, secondary_host, port, queue, username=None, password=None):
        self.queue = queue
        if username and password:
            self.rabbitmq_url = f"amqp://{username}:{password}@{host}:{port}/%2F"
            self.rabbitmq_secondary_url = (
                f"amqp://{username}:{password}@{secondary_host}:{port}/%2F"
            )
        else:
            self.rabbitmq_url = f"amqp://{host}:{port}/%2F"
            self.rabbitmq_secondary_url = f"amqp://{secondary_host}:{port}/%2F"

    def _connect(self):
        try:
            logger.info(
                "attempt to open connection", server="primary", category="rabbitmq"
            )
            return BlockingConnection(URLParameters(self.rabbitmq_url))
        except AMQPError as e:
            logger.error(
                "unable to open connection",
                exc_info=e,
                server="primary",
                category="rabbitmq",
            )
            try:
                logger.info(
                    "attempt to open connection",
                    server="secondary",
                    category="rabbitmq",
                )
                return BlockingConnection(URLParameters(self.rabbitmq_secondary_url))
            except AMQPError as err:
                logger.error(
                    "unable to open connection",
                    exc_info=e,
                    server="secondary",
                    category="rabbitmq",
                )
                raise err

    @staticmethod
    def _disconnect(connection):
        try:
            if connection:
                logger.info("attempt to close connection", category="rabbitmq")
                connection.close()
        except AMQPError as e:
            logger.error("unable to close connection", exc_info=e, category="rabbitmq")

    def send_message(self, message, tx_id, case_id):
        """
        Sends a message to rabbit mq and returns a true or false depending on if it was successful
        :param message: The message to send to the rabbit mq queue
        :param tx_id: Transaction ID used to trace a transaction through the whole system.
        :param case_id: ID used to identify a single instance of a survey collection for a respondent
        :return: a boolean value indicating if it was successful
        """
        message_as_string = str(message)
        logger.info("sending message", category="rabbitmq")
        logger.info("message payload", message=message_as_string, category="rabbitmq")
        connection = None
        try:
            connection = self._connect()
            channel = connection.channel()

            channel.queue_declare(queue=self.queue, durable=True)
            properties = BasicProperties(headers={}, delivery_mode=2)

            properties.headers["tx_id"] = tx_id
            properties.headers["case_id"] = case_id

            channel.basic_publish(
                exchange="",
                routing_key=self.queue,
                body=message_as_string,
                mandatory=True,
                properties=properties,
            )

            logger.info("sent message", category="rabbitmq")

        except (AMQPError, NackError, UnroutableError) as e:
            logger.error("unable to send message", exc_info=e, category="rabbitmq")
            return False
        finally:
            if connection:
                self._disconnect(connection)

        return True


class GCSFeedbackSubmitter:
    def __init__(self, bucket_name):
        client = storage.Client()
        self.bucket = client.get_bucket(bucket_name)

    def upload(self, metadata, payload):
        blob = self.bucket.blob(str(uuid4()))
        blob.metadata = metadata
        blob.upload_from_string(json_dumps(payload).encode("utf8"))

        return True


class LogFeedbackSubmitter:
    @staticmethod
    def upload(metadata, payload):
        logger.info("uploading feedback")
        logger.info(
            "feedback message",
            metadata=metadata,
            payload=payload,
        )

        return True
