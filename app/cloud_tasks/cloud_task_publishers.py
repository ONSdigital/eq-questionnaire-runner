from typing import Mapping

from google import auth
from google.cloud.tasks_v2 import CloudTasksClient
from google.cloud.tasks_v2.types.task import Task
from structlog import get_logger

from .exceptions import CloudTaskCreationFailed

logger = get_logger(__name__)


class CloudTaskPublisher:
    def __init__(self):
        self._client = CloudTasksClient()

        _, self._project_id = auth.default()

    def _create(self, task: Mapping, queue_name: str) -> Task:
        logger.info("creating cloud task")

        self._parent = self._client.queue_path(
            self._project_id, "europe-west2", queue_name
        )

        return self._client.create_task(request={"parent": self._parent, "task": task})

    def create_task(self, task: Mapping, queue_name: str) -> None:
        try:
            self._create(task, queue_name)
            logger.info("task created successfully")  # pragma: no cover
        except Exception as ex:  # pylint:disable=broad-except
            logger.exception(
                "task creation failed",
            )
            raise CloudTaskCreationFailed(ex) from ex


class LogCloudTaskPublisher:
    def __init__(self):
        self._project_id = "test"

    @staticmethod
    def create_task(task: Mapping, queue_name: str) -> None:
        logger.info("creating cloud task", task=task, queue_name=queue_name)
