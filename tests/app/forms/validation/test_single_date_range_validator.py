import pytest
from wtforms.validators import ValidationError

from app.forms import error_messages
from app.forms.validators import SingleDatePeriodCheck
from app.questionnaire.rules.utils import parse_datetime


@pytest.mark.parametrize(
    "validator, data, error_type, error_message",
    (
        (
            SingleDatePeriodCheck(minimum_date=parse_datetime("2016-03-31")),
            "2016-01-29",
            "SINGLE_DATE_PERIOD_TOO_EARLY",
            {"min": "30 March 2016"},
        ),
        (
            SingleDatePeriodCheck(maximum_date=parse_datetime("2016-03-31")),
            "2016-04-29",
            "SINGLE_DATE_PERIOD_TOO_LATE",
            {"max": "1 April 2016"},
        ),
    ),
)
@pytest.mark.usefixtures("app")
def test_single_date_period_invalid_raises_ValidationError(
    validator, data, error_type, error_message, mock_form, mock_field
):

    mock_form.data = data

    with pytest.raises(ValidationError) as exc:
        validator(mock_form, mock_field)

    assert error_messages[error_type] % error_message == str(exc.value)


@pytest.mark.usefixtures("app")
def test_single_date_period_custom_message_invalid_raises(mock_form, mock_field):
    maximum_date = parse_datetime("2016-03-31")
    message = {"SINGLE_DATE_PERIOD_TOO_LATE": "Test %(max)s"}
    validator = SingleDatePeriodCheck(messages=message, maximum_date=maximum_date)
    mock_form.data = "2016-04-29"

    with pytest.raises(ValidationError) as exc:
        validator(mock_form, mock_field)

    assert "Test 1 April 2016" == str(exc.value)


def test_valid_single_date_period(mock_form, mock_field):
    minimum_date = parse_datetime("2016-03-20")
    maximum_date = parse_datetime("2016-03-31")
    validator = SingleDatePeriodCheck(
        minimum_date=minimum_date, maximum_date=maximum_date
    )

    mock_form.data = "2016-03-26"

    validator(mock_form, mock_field)


def test_messages_are_merged():
    messages = {"SINGLE_DATE_PERIOD_TOO_LATE": "Test %(max)s"}
    validator = SingleDatePeriodCheck(messages=messages)

    assert len(validator.messages) > 1
