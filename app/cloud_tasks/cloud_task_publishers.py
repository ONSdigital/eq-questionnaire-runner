from google import auth
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

        url = f"https://europe-west2-{self._project_id}.cloudfunctions.net/eq-submission-confirmation-consumer"
        self._task = {
            "http_request": {
                "http_method": HttpMethod.POST,
                "url": url,
                "oidc_token": {
                    "service_account_email": "cloud-task-http-function-invok@james-test-292314.iam.gserviceaccount.com"
                },
                "headers": {
                    "Content-type": "application/json",
                },
            },
        }

    def _create(self, payload: bytes) -> Task:
        logger.info("creating cloud task")
        task = self._task.copy()
        task["http_request"]["body"] = payload
        return self._client.create_task(request={"parent": self._parent, "task": task})

    def create_task(self, payload: bytes) -> None:
        try:
            self._create(payload)
            logger.info("task published successfully")  # pragma: no cover
        except Exception as ex:  # pylint:disable=broad-except
            logger.exception(
                "task creation failed",
            )
            raise CloudTaskCreationFailed(ex) from ex


class LogCloudTaskPublisher:
    @staticmethod
    def create_task(payload: bytes) -> None:
        logger.info("creating cloud task", payload=payload)
