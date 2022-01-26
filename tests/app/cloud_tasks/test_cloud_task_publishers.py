from uuid import uuid4

import pytest
from google.api_core.exceptions import DeadlineExceeded, ServiceUnavailable
from google.cloud.tasks_v2 import CreateTaskRequest
from google.cloud.tasks_v2.types.task import Task

from app.cloud_tasks.exceptions import CloudTaskCreationFailed

PROJECT_ID = "test-project-id"
QUEUE_NAME = "test"
FUNCTION_NAME = "test"
BODY = bytes("test", "utf-8")
TRANSACTION_ID = str(uuid4())


def test_create_task(
    mocker,
    cloud_task_publisher,
    project_id=PROJECT_ID,
    queue_name=QUEUE_NAME,
    function_name=FUNCTION_NAME,
    body=BODY,
    transaction_id=TRANSACTION_ID,
):
    # Mock the actual call within the gRPC stub, and fake the request.
    call = mocker.patch.object(
        type(
            cloud_task_publisher._client.transport.create_task  # pylint: disable=protected-access
        ),
        "__call__",
    )
    # Designate an appropriate return value for the call.
    call.return_value = (
        cloud_task_publisher._get_task(  # pylint: disable=protected-access
            body=body, function_name=function_name
        )
    )
    cloud_task_publisher.create_task(
        body=body,
        queue_name=queue_name,
        function_name=function_name,
        fulfilment_request_transaction_id=transaction_id,
    )
    # Establish that the underlying gRPC stub method was called.
    assert len(call.mock_calls) == 1
    _, args, _ = call.mock_calls[0]
    assert args[0] == CreateTaskRequest(
        mapping={
            "parent": f"projects/{project_id}/locations/europe-west2/queues/test",
            "task": cloud_task_publisher._get_task(  # pylint: disable=protected-access
                body=body, function_name=function_name
            ),
        }
    )


def test_create_task_raises_exception_on_non_transient_error(
    mocker,
    cloud_task_publisher,
    queue_name=QUEUE_NAME,
    function_name=FUNCTION_NAME,
    body=BODY,
    transaction_id=TRANSACTION_ID,
):
    mock_create_task = mocker.Mock()
    mock_create_task.side_effect = DeadlineExceeded("test")
    cloud_task_publisher._client.create_task = (  # pylint: disable=protected-access
        mock_create_task
    )

    with pytest.raises(CloudTaskCreationFailed):
        cloud_task_publisher.create_task(
            body=body,
            queue_name=queue_name,
            function_name=function_name,
            fulfilment_request_transaction_id=transaction_id,
        )


def test_create_task_transient_error_retries(
    mocker,
    cloud_task_publisher,
    queue_name=QUEUE_NAME,
    function_name=FUNCTION_NAME,
    body=BODY,
    transaction_id=TRANSACTION_ID,
):
    mock_create_task = mocker.Mock()
    mock_create_task.side_effect = [ServiceUnavailable("test"), Task()]
    cloud_task_publisher._client.create_task = (  # pylint: disable=protected-access
        mock_create_task
    )
    cloud_task_publisher.create_task(
        body=body,
        queue_name=queue_name,
        function_name=function_name,
        fulfilment_request_transaction_id=transaction_id,
    )

    assert mock_create_task.call_count == 2
