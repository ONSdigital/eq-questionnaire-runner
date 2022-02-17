import pytest


@pytest.fixture
def mock_form(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_field(mocker):
    return mocker.Mock()
