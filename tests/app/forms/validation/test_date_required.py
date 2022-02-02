import pytest
from wtforms.validators import StopValidation

from app.forms import error_messages


def test_day_month_year_required_empty(date_required, mock_form, mock_field):
    mock_form.day.data = ""
    mock_form.month.data = ""
    mock_form.year.data = ""

    assert_mandatory_date_error(date_required, mock_field, mock_form)


def test_month_year_required_empty(date_required, mock_form, mock_field):
    del mock_form.day
    mock_form.month.data = ""
    mock_form.year.data = ""

    assert_mandatory_date_error(date_required, mock_field, mock_form)


def test_year_required_empty(date_required, mock_form, mock_field):
    del mock_form.day
    del mock_form.month
    mock_form.year.data = ""

    assert_mandatory_date_error(date_required, mock_field, mock_form)


def test_valid_day_month_year(date_required, mock_form, mock_field):
    mock_form.day.data = "01"
    mock_form.month.data = "01"
    mock_form.year.data = "2015"

    try:
        date_required(mock_form, mock_field)
    except StopValidation:
        pytest.fail("Valid day month year raised StopValidation")


def test_valid_month_year(date_required, mock_form, mock_field):
    mock_form.month.data = "01"
    mock_form.year.data = "2017"

    try:
        date_required(mock_form, mock_field)
    except StopValidation:
        pytest.fail("Valid month year raised StopValidation")


def test_valid_year(date_required, mock_form, mock_field):
    mock_form.year.data = "2017"

    try:
        date_required(mock_form, mock_field)
    except StopValidation:
        pytest.fail("Valid year raised StopValidation")


def assert_mandatory_date_error(date_required, mock_field, mock_form):
    with pytest.raises(StopValidation) as ite:
        date_required(mock_form, mock_field)
    assert error_messages["MANDATORY_DATE"] == str(ite.value)
