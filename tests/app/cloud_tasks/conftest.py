import pytest

from app.cloud_tasks import CloudTaskPublisher


@pytest.fixture
def cloud_task_publisher(mocker):
    mocker.patch(
        "google.auth._default._get_explicit_environ_credentials",
        return_value=(mocker.Mock, "test-project-id"),
    )
    return CloudTaskPublisher()
