import pytest


@pytest.fixture
def mock_form(mocker):
    return mocker.MagicMock()


@pytest.fixture
def mock_field(mocker):
    return mocker.Mock()
