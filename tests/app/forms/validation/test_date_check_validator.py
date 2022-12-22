import pytest
from wtforms.validators import StopValidation

from app.forms import error_messages


@pytest.mark.parametrize(
    "date",
    [
        "",
        "2016-12-",
        "2016--03",
        "-12-03",
        "2016-12-40",
        "2016-13-20",
        "20000-12-20",
        "2015-02-29",  # 2015 was not a leap year
    ],
)
def test_invalid_day_month_year(date_check, mock_form, mock_field, date):
    mock_form.data = date

    assert_invalid_date_error(date_check, mock_form, mock_field)


@pytest.mark.parametrize(
    "date",
    [
        "2016-",
        "-12",
        "2016-13",
        "20000-12",
    ],
)
def test_invalid_month_year(date_check, mock_form, mock_field, date):
    mock_form.data = date
    del mock_form.day

    assert_invalid_date_error(date_check, mock_form, mock_field)


@pytest.mark.parametrize(
    "year",
    [
        "20000",
        "200",
        "20",
    ],
)
def test_invalid_year(date_check, mock_form, mock_field, year):
    del mock_form.day
    del mock_form.month
    mock_form.year.data = year

    assert_invalid_date_error(date_check, mock_form, mock_field)


def test_invalid_data(date_check, mock_form, mock_field):
    del mock_form.day
    del mock_form.month
    del mock_form.year
    mock_form.data = "abc"

    assert_invalid_date_error(date_check, mock_form, mock_field)


@pytest.mark.parametrize(
    "date",
    [
        "2016-01-29",
        "2016-02-29",  # 2016 was a leap year
    ],
)
def test_valid_day_month_year(date_check, mock_form, mock_field, date):
    mock_form.data = date
    mock_form["year"].data = date.split("-")[0]
    try:
        date_check(mock_form, mock_field)
    except StopValidation:
        pytest.fail("Valid day month year raised StopValidation")


def test_valid_month_year(date_check, mock_form, mock_field):
    del mock_form.day
    mock_form.data = "2016-12"
    mock_form["year"].data = "2016"

    try:
        date_check(mock_form, mock_field)
    except StopValidation:
        pytest.fail("Valid month year raised StopValidation")


def test_valid_year(date_check, mock_form, mock_field):
    del mock_form.day
    del mock_form.month
    mock_form.data = "2016"
    mock_form["year"].data = "2016"

    try:
        date_check(mock_form, mock_field)
    except StopValidation:
        pytest.fail("Valid year raised StopValidation")


def assert_invalid_date_error(date_check, mock_form, mock_field):
    with pytest.raises(StopValidation) as ite:
        date_check(mock_form, mock_field)
    assert error_messages["INVALID_DATE"] == str(ite.value)
