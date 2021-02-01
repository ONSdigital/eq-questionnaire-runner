from google import auth
from google.api_core.retry import Retry
from google.cloud.tasks_v2 import CloudTasksClient, HttpMethod
from google.cloud.tasks_v2.types.task import Task
from structlog import get_logger

from .exceptions import CloudTaskCreationFailed

logger = get_logger(__name__)


class CloudTaskPublisher:
    def __init__(self, queue_name: str):
        self._client = CloudTasksClient()
        _, self._project_id = auth.default()

        self._parent = self._client.queue_path(
            self._project_id, "europe-west2", queue_name
        )

    def _get_task(self, body: bytes, function_name: str):
        service_account_email = (
            f"cloud-functions@{self._project_id}.iam.gserviceaccount.com"
        )

        url = f"https://europe-west2-{self._project_id}.cloudfunctions.net/{function_name}"

        return Task(
            {
                "http_request": {
                    "http_method": HttpMethod.POST,
                    "url": url,
                    "oidc_token": {"service_account_email": service_account_email},
                    "headers": {
                        "Content-type": "application/json",
                    },
                    "body": body,
                },
            }
        )

    @Retry()
    def _create_task_with_retry(self, body: bytes, function_name: str) -> Task:
        task = self._client.create_task(
            parent=self._parent,
            task=self._get_task(body=body, function_name=function_name),
        )
        return task

    def create_task(self, body: bytes, function_name: str) -> Task:
        logger.info("creating cloud task")

        try:
            task = self._create_task_with_retry(body, function_name)
            logger.info("task created successfully")  # pragma: no cover
            return task
        except Exception as exc:
            logger.exception(
                "task creation failed",
            )
            raise CloudTaskCreationFailed from exc


class LogCloudTaskPublisher:
    @staticmethod
    def create_task(body: bytes, function_name: str) -> None:
        logger.info(
            "creating cloud task",
            body=body,
            function_name=function_name,
        )
