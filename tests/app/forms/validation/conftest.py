import pytest

from app.forms.validators import DateCheck, DateRangeCheck, DateRequired


@pytest.fixture
def date_check():
    return DateCheck()


@pytest.fixture
def date_required():
    return DateRequired()


@pytest.fixture
def get_date_range_check():
    def _date_range_check(messages=None, period_min=None, period_max=None):
        return DateRangeCheck(
            messages=messages, period_min=period_min, period_max=period_max
        )

    return _date_range_check


@pytest.fixture
def mock_form(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_field(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_period_from(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_period_to(mocker):
    return mocker.Mock()
