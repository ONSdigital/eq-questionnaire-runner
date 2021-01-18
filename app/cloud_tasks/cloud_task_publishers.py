from google import auth
from google.cloud.tasks_v2 import CloudTasksClient, HttpMethod
from google.cloud.tasks_v2.types.task import Task
from structlog import get_logger

from app.settings import SUBMISSION_CONFIRMATION_CLOUD_FUNCTION_NAME

from .exceptions import CloudTaskCreationFailed

logger = get_logger(__name__)


class CloudTaskPublisher:
    def __init__(self):
        self._client = CloudTasksClient()

        _, self._project_id = auth.default()

    def _create(self, payload: bytes, queue_name: str) -> Task:
        logger.info("creating cloud task")

        self._parent = self._client.queue_path(
            self._project_id, "europe-west2", queue_name
        )

        url = f"https://europe-west2-{self._project_id}.cloudfunctions.net/{SUBMISSION_CONFIRMATION_CLOUD_FUNCTION_NAME}"
        task = {
            "http_request": {
                "http_method": HttpMethod.POST,
                "url": url,
                "oidc_token": {
                    "service_account_email": f"cloud-functions@{self._project_id}.iam.gserviceaccount.com"
                },
                "headers": {
                    "Content-type": "application/json",
                },
                "body": payload,
            },
        }
        return self._client.create_task(request={"parent": self._parent, "task": task})

    def create_task(self, payload: bytes, queue_name: str) -> None:
        try:
            self._create(payload, queue_name)
            logger.info("task published successfully")  # pragma: no cover
        except Exception as ex:  # pylint:disable=broad-except
            logger.exception(
                "task creation failed",
            )
            raise CloudTaskCreationFailed(ex) from ex


class LogCloudTaskPublisher:
    @staticmethod
    def create_task(payload: bytes, queue_name: str) -> None:
        logger.info("creating cloud task", payload=payload, queue_name=queue_name)
