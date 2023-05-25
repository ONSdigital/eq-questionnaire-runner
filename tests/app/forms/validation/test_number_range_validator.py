import pytest
from wtforms.validators import ValidationError

from app.forms import error_messages
from app.forms.validators import NumberRange


@pytest.mark.parametrize(
    "minimum, maximum, value, min_excl, max_excl, error_type, error_dict",
    (
        (0, None, -10, False, False, "NUMBER_TOO_SMALL", {"min": 0}),
        (
            None,
            9999999999,
            10000000000,
            False,
            False,
            "NUMBER_TOO_LARGE",
            {"max": "9,999,999,999"},
        ),
        (
            10,
            100,
            10,
            True,
            False,
            "NUMBER_TOO_SMALL_EXCLUSIVE",
            {"min": "10"},
        ),
        (
            10,
            100,
            "NaN",
            False,
            True,
            "INVALID_NUMBER",
            {"max": "100"},
        ),
        (
            None,
            1000,
            1000,
            False,
            True,
            "NUMBER_TOO_LARGE_EXCLUSIVE",
            {"max": "1,000"},
        ),
    ),
)
@pytest.mark.usefixtures("gb_locale")
def test_number_range_validator_raises_ValidationError(
    minimum,
    maximum,
    value,
    min_excl,
    max_excl,
    error_type,
    error_dict,
    mock_form,
    mock_field,
):
    validator = NumberRange(
        minimum=minimum,
        maximum=maximum,
        minimum_exclusive=min_excl,
        maximum_exclusive=max_excl,
    )
    mock_field.data = value
    mock_field.raw_data = [value]

    with pytest.raises(ValidationError) as exc:
        validator(mock_form, mock_field)

    assert error_messages[error_type] % error_dict == str(exc.value)


@pytest.mark.usefixtures("gb_locale")
def test_number_range_validator_nan_check_passes(mock_form, mock_field, value=None):
    validator = NumberRange(
        minimum=10,
        maximum=100,
        minimum_exclusive=False,
        maximum_exclusive=False,
    )
    mock_field.data = value
    mock_field.raw_data = [value]

    validator(mock_form, mock_field)


@pytest.mark.usefixtures("gb_locale")
def test_number_range_validator_nan_check_raises_exception(
    mock_form, mock_field, value="NaN"
):
    validator = NumberRange(
        minimum=10,
        maximum=100,
        minimum_exclusive=False,
        maximum_exclusive=False,
    )
    mock_field.data = value
    mock_field.raw_data = [value]

    with pytest.raises(ValidationError):
        validator(mock_form, mock_field)


@pytest.mark.parametrize(
    "minimum, maximum, value",
    (
        (0, 10, 10),
        (0, 9999999999, 0),
        (None, None, 9999999999),
    ),
)
@pytest.mark.usefixtures("gb_locale")
def test_number_range_validator(minimum, maximum, value, mock_form, mock_field):
    validator = NumberRange(minimum=minimum, maximum=maximum)
    mock_field.data = value
    mock_field.raw_data = [value]

    validator(mock_form, mock_field)
