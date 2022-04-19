from typing import Mapping, Optional
from uuid import uuid4

from google.cloud import storage  # type: ignore
from google.cloud.storage.retry import DEFAULT_RETRY
from pika import BasicProperties, BlockingConnection, URLParameters
from pika.exceptions import AMQPError, NackError, UnroutableError
from structlog import get_logger

logger = get_logger()

MetadataType = Mapping[str, str]


class LogSubmitter:
    @staticmethod
    def send_message(message: str, tx_id: str, case_id: str) -> bool:
        logger.info("sending message")
        logger.info(
            "message payload",
            message=message,
            case_id=case_id,
            tx_id=tx_id,
        )

        return True


class GCSSubmitter:
    def __init__(self, bucket_name: str) -> None:
        client = storage.Client()
        self.bucket = client.get_bucket(bucket_name)

    def send_message(self, message: str, tx_id: str, case_id: str) -> bool:
        logger.info("sending message")

        blob = self.bucket.blob(tx_id)
        blob.metadata = {"tx_id": tx_id, "case_id": case_id}

        # DEFAULT_RETRY is not idempotent.
        # However, this behaviour was deemed acceptable for our use case.
        blob.upload_from_string(str(message).encode("utf8"), retry=DEFAULT_RETRY)

        return True


class RabbitMQSubmitter:
    def __init__(
        self,
        host: str,
        secondary_host: str,
        port: int,
        queue: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        self.queue = queue
        if username and password:
            self.rabbitmq_url = f"amqp://{username}:{password}@{host}:{port}/%2F"
            self.rabbitmq_secondary_url = (
                f"amqp://{username}:{password}@{secondary_host}:{port}/%2F"
            )
        else:
            self.rabbitmq_url = f"amqp://{host}:{port}/%2F"
            self.rabbitmq_secondary_url = f"amqp://{secondary_host}:{port}/%2F"

    def _connect(self) -> BlockingConnection:
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
    def _disconnect(connection: Optional[BlockingConnection]) -> None:
        try:
            if connection:
                logger.info("attempt to close connection", category="rabbitmq")
                connection.close()
        except AMQPError as e:
            logger.error("unable to close connection", exc_info=e, category="rabbitmq")

    def send_message(self, message: str, tx_id: str, case_id: str) -> bool:
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
    def __init__(self, bucket_name: str) -> None:
        client = storage.Client()
        self.bucket = client.get_bucket(bucket_name)

    def upload(self, metadata: MetadataType, payload: str) -> bool:
        blob = self.bucket.blob(str(uuid4()))
        blob.metadata = metadata

        # DEFAULT_RETRY is not idempotent.
        # However, this behaviour was deemed acceptable for our use case.
        blob.upload_from_string(payload.encode("utf8"), retry=DEFAULT_RETRY)

        return True


class LogFeedbackSubmitter:
    @staticmethod
    def upload(metadata: MetadataType, payload: str) -> bool:
        logger.info("uploading feedback")
        logger.info(
            "feedback message",
            metadata=metadata,
            payload=payload,
        )

        return True
