import pytest
from wtforms.validators import StopValidation

from app.forms import error_messages
from app.forms.validators import EmailTLDCheck


@pytest.mark.parametrize(
    "email",
    (
        "a@a.a",
        "a@a.a9",
        "a@a.\x94",
    ),
)
def test_tld_invalid_emails(email, mock_form, mock_field):
    validator = EmailTLDCheck()
    mock_field.data = email

    with pytest.raises(StopValidation) as exc:
        validator(mock_form, mock_field)

    assert error_messages["INVALID_EMAIL_FORMAT"] == str(exc.value)
