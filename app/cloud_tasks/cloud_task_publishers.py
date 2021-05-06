from google import auth
from google.api_core.retry import Retry
from google.cloud.tasks_v2 import CloudTasksClient, HttpMethod
from google.cloud.tasks_v2.types.task import Task
from structlog import get_logger

from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

from .exceptions import CloudTaskCreationFailed

logger = get_logger(__name__)

tracer_provider = TracerProvider()
cloud_trace_exporter = CloudTraceSpanExporter()
tracer_provider.add_span_processor(
    BatchExportSpanProcessor(cloud_trace_exporter)
)
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer(__name__)


class CloudTaskPublisher:
    def __init__(self):
        self._client = CloudTasksClient()

        _, self._project_id = auth.default()

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
    def _create_task_with_retry(
        self, body: bytes, function_name: str, parent: str
    ) -> Task:
        task = self._client.create_task(
            parent=parent,
            task=self._get_task(body=body, function_name=function_name),
        )

        return task

    def create_task(
        self,
        body: bytes,
        queue_name: str,
        function_name: str,
        fulfilment_request_transaction_id: str,
    ) -> Task:

        parent = self._client.queue_path(self._project_id, "europe-west2", queue_name)
        try:
            task = self._create_task_with_retry(body, function_name, parent)
            logger.info(
                "task created successfully",
                fulfilment_request_transaction_id=fulfilment_request_transaction_id,
            )
            return task
        except Exception as exc:
            logger.exception(
                "task creation failed",
                fulfilment_request_transaction_id=fulfilment_request_transaction_id,
            )
            raise CloudTaskCreationFailed from exc


class LogCloudTaskPublisher:
    @staticmethod
    def create_task(
        body: bytes,
        queue_name: str,
        function_name: str,
        fulfilment_request_transaction_id: str,
    ) -> None:
        with tracer.start_as_current_span("cloud task") as current_span:
            logger.info(
                "creating cloud task",
                body=body,
                queue_name=queue_name,
                function_name=function_name,
                fulfilment_request_transaction_id=fulfilment_request_transaction_id,
            )
            current_span.add_event(name="create task")
