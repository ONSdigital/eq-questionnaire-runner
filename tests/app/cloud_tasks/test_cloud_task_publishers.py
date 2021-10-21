from unittest import TestCase, mock
from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

from google.api_core.exceptions import DeadlineExceeded, ServiceUnavailable
from google.cloud.tasks_v2 import CreateTaskRequest
from google.cloud.tasks_v2.types.task import Task

from app.cloud_tasks import CloudTaskPublisher
from app.cloud_tasks.exceptions import CloudTaskCreationFailed


# pylint: disable=protected-access
class TestCloudTaskPublisher(TestCase):
    PROJECT_ID = "test-project-id"
    queue_name = "test"
    function_name = "test"
    body = bytes("test", "utf-8")
    transaction_id = str(uuid4())

    def setUp(self) -> None:
        with patch(
            "google.auth._default._get_explicit_environ_credentials",
            return_value=(Mock(), self.PROJECT_ID),
        ):
            self.cloud_task_publisher = CloudTaskPublisher()

    def test_create_task(self):
        # Mock the actual call within the gRPC stub, and fake the request.
        with mock.patch.object(
            type(self.cloud_task_publisher._client.transport.create_task), "__call__"
        ) as call:
            # Designate an appropriate return value for the call.
            call.return_value = self.cloud_task_publisher._get_task(
                body=self.body, function_name=self.function_name
            )
            self.cloud_task_publisher.create_task(
                body=self.body,
                queue_name=self.queue_name,
                function_name=self.function_name,
                fulfilment_request_transaction_id=self.transaction_id,
            )

            # Establish that the underlying gRPC stub method was called.
            assert len(call.mock_calls) == 1
            _, args, _ = call.mock_calls[0]
            assert args[0] == CreateTaskRequest(
                mapping={
                    "parent": f"projects/{self.PROJECT_ID}/locations/europe-west2/queues/test",
                    "task": self.cloud_task_publisher._get_task(
                        body=self.body, function_name=self.function_name
                    ),
                }
            )

    def test_create_task_raises_exception_on_non_transient_error(self):
        mock_create_task = MagicMock()
        mock_create_task.side_effect = DeadlineExceeded("test")
        self.cloud_task_publisher._client.create_task = mock_create_task

        with self.assertRaises(CloudTaskCreationFailed):
            self.cloud_task_publisher.create_task(
                body=self.body,
                queue_name=self.queue_name,
                function_name=self.function_name,
                fulfilment_request_transaction_id=self.transaction_id,
            )

    def test_create_task_transient_error_retries(self):
        mock_create_task = MagicMock()
        mock_create_task.side_effect = [ServiceUnavailable("test"), Task()]
        self.cloud_task_publisher._client.create_task = mock_create_task
        self.cloud_task_publisher.create_task(
            body=self.body,
            queue_name=self.queue_name,
            function_name=self.function_name,
            fulfilment_request_transaction_id=self.transaction_id,
        )

        self.assertEqual(mock_create_task.call_count, 2)
