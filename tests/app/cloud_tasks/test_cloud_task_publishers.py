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
        payload = bytes("test", "utf-8")
        task = self.cloudTaskPublisher._task.copy()
        task["http_request"]["body"] = payload

        self.cloudTaskPublisher._client = Mock()

        self.cloudTaskPublisher.create_task(payload=payload, queue_name=queue_name)

        self.cloudTaskPublisher._client.create_task.assert_called_once_with(
            request={"parent": self.cloudTaskPublisher._parent, "task": task}
        )

    def test_create_task_raises_exception(self):
        queue_name = "test"
        payload = bytes("test", "utf-8")

        self.cloudTaskPublisher._create = Mock(side_effect=Exception)

        with self.assertRaises(CloudTaskCreationFailed):
            self.cloudTaskPublisher.create_task(payload=payload, queue_name=queue_name)
