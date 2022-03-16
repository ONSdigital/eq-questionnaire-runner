import pytest
from wtforms.validators import ValidationError

from app.forms import error_messages
from app.forms.validators import MobileNumberCheck, sanitise_mobile_number


@pytest.mark.parametrize(
    "unsanitized_number, expected",
    (
        ("0.7.7.0.0.9.0.0.1.1.1.", "7700900111"),
        ("0447700\t900222", "7700900222"),
        ("07700-(900333)", "7700900333"),
        ("/0770/090/0444", "7700900444"),
        ("00447700 900555", "7700900555"),
        ("0447700 900555", "7700900555"),
        ("+447700 900666", "7700900666"),
        ("[07700] 900777", "7700900777"),
        ("(07700) {900888}", "7700900888"),
        ("+440447700900999", "0447700900999"),
        (" 09[8./{}756gf}/{h]fgh", "98756gfhfgh"),
        ("7700900222", "7700900222"),
        ("07700900222", "7700900222"),
    ),
)
def test_sanitise_mobile_number(unsanitized_number, expected):
    assert sanitise_mobile_number(unsanitized_number) == expected


@pytest.mark.parametrize(
    "number",
    (
        "7700900111789101112",
        "`-tykg07700900222",
        "07700e90033",
        "06700900222",
        "൦൧൨൩൪൫൬൭൮൯",
    ),
)
def test_invalid_numbers_raise_ValidationError(number, mock_form, mock_field):
    validator = MobileNumberCheck()
    mock_field.data = number

    with pytest.raises(ValidationError) as exc:
        validator(mock_form, mock_field)

    assert error_messages["INVALID_MOBILE_NUMBER"] == str(exc.value)
