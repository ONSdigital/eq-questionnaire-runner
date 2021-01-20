from unittest import TestCase, mock
from unittest.mock import Mock, patch

from google.cloud.tasks_v2 import CreateTaskRequest

from app.cloud_tasks import CloudTaskPublisher
from app.cloud_tasks.exceptions import CloudTaskCreationFailed


class TestCloudTaskPublisher(TestCase):
    PROJECT_ID = "test-project-id"

    def setUp(self) -> None:
        with patch(
            "google.auth._default._get_explicit_environ_credentials",
            return_value=(Mock(), self.PROJECT_ID),
        ):
            self.cloud_task_publisher = CloudTaskPublisher()

    def test_create_task(self):
        queue_name = "test"
        function_name = "test"
        body = bytes("test", "utf-8")

        # Mock the actual call within the gRPC stub, and fake the request.
        with mock.patch.object(
            type(self.cloud_task_publisher._client.transport.create_task), "__call__"
        ) as call:

            # Designate an appropriate return value for the call.
            call.return_value = self.cloud_task_publisher.get_task(
                body=body, function_name=function_name
            )
            self.cloud_task_publisher.create_task(
                body=body, queue_name=queue_name, function_name=function_name
            )

            # Establish that the underlying gRPC stub method was called.
            assert len(call.mock_calls) == 1
            _, args, _ = call.mock_calls[0]
            assert args[0] == CreateTaskRequest(
                mapping={
                    "parent": f"projects/{self.PROJECT_ID}/locations/europe-west2/queues/test",
                    "task": self.cloud_task_publisher.get_task(
                        body=body, function_name=function_name
                    ),
                }
            )

    def test_create_task_raises_exception(self):
        queue_name = "test"
        function_name = "test"
        body = bytes("test", "utf-8")

        self.cloud_task_publisher._create = Mock(side_effect=Exception)

        with self.assertRaises(CloudTaskCreationFailed):
            self.cloud_task_publisher.create_task(
                body=body, queue_name=queue_name, function_name=function_name
            )
