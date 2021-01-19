from unittest import TestCase
from unittest.mock import Mock, patch

from app.cloud_tasks.cloud_task_publishers import CloudTaskPublisher
from app.cloud_tasks.exceptions import CloudTaskCreationFailed


class TestCloudTaskPublisher(TestCase):
    def setUp(self) -> None:
        with patch(
            "google.auth._default._get_explicit_environ_credentials",
            return_value=(Mock(), "test-project-id"),
        ):
            self.cloudTaskPublisher = CloudTaskPublisher()

    def test_create_task(self):
        queue_name = "test"
        function_name = "test"
        payload = bytes("test", "utf-8")

        self.cloudTaskPublisher._client = Mock()

        self.cloudTaskPublisher.create_task(
            body=payload, queue_name=queue_name, function_name=function_name
        )

        self.cloudTaskPublisher._client.create_task.assert_called_once_with(
            request={
                "parent": self.cloudTaskPublisher._parent,
                "task": self.cloudTaskPublisher.get_task(
                    body=payload, function_name=function_name
                ),
            }
        )

    def test_create_task_raises_exception(self):
        queue_name = "test"
        function_name = "test"
        body = bytes("test", "utf-8")

        self.cloudTaskPublisher._create = Mock(side_effect=Exception)

        with self.assertRaises(CloudTaskCreationFailed):
            self.cloudTaskPublisher.create_task(
                body=body, queue_name=queue_name, function_name=function_name
            )
