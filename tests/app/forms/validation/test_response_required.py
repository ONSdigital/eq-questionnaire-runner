import pytest
from wtforms.validators import StopValidation

from app.forms.validators import ResponseRequired


@pytest.mark.parametrize(
    "message, raw_data",
    (
        ("test_response_empty_invalid", [""]),
        ("test_response_blank_invalid", ["                           "]),
    ),
)
def test_response_invalid_raises_StopValidation(
    raw_data, message, mock_form, mock_field
):
    validator = ResponseRequired(message)
    mock_field.raw_data = raw_data
    mock_field.errors = []

    with pytest.raises(StopValidation) as exc:
        validator(mock_form, mock_field)

    assert message == str(exc.value)


@pytest.mark.parametrize(
    "message, raw_data, strip_whitespace",
    (
        ("test_required_empty", ["Here is some valid input"], True),
        (
            "test_required_contains_content",
            ["           Here is some valid input             "],
            True,
        ),
        (
            "test_response_blank_valid_when_whitespace_on",
            ["                      "],
            False,
        ),
    ),
)
def test_response(raw_data, message, strip_whitespace, mock_form, mock_field):
    validator = ResponseRequired(message, strip_whitespace=strip_whitespace)
    mock_field.raw_data = raw_data
    mock_field.errors = []

    validator(mock_form, mock_field)
