import pytest
from wtforms.validators import StopValidation, ValidationError

from app.forms import error_messages
from app.forms.validators import DecimalPlaces


@pytest.mark.parametrize(
    "value",
    (
        [None],
        [""],
        ["a"],
        ["2E2"],
    ),
)
@pytest.mark.usefixtures("gb_locale")
def test_number_validator_raises_StopValidation(
    number_check, value, mock_form, mock_field
):
    mock_field.raw_data = value

    with pytest.raises(StopValidation) as exc:
        number_check(mock_form, mock_field)

    assert error_messages["INVALID_NUMBER"] == str(exc.value)


@pytest.mark.usefixtures("gb_locale")
def test_decimal_validator_raises_StopValidation(mock_form, mock_field):
    validator = DecimalPlaces(2)
    mock_field.raw_data = ["1.234"]

    with pytest.raises(ValidationError) as exc:
        validator(mock_form, mock_field)

    assert error_messages["INVALID_DECIMAL"] % {"max": 2} == str(exc.value)


@pytest.mark.parametrize(
    "value",
    (
        ["0"],
        ["10"],
        ["-10"],
    ),
)
@pytest.mark.usefixtures("gb_locale")
def test_number_validator(number_check, value, mock_form, mock_field):
    mock_field.raw_data = value
    number_check(mock_form, mock_field)
