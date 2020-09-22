import unittest
from unittest.mock import Mock, patch

from wtforms.validators import StopValidation, ValidationError

from app.forms import error_messages
from app.forms.validators import MobileNumberCheck


# pylint: disable=no-member
@patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="en_GB"))
class TestPhoneNumberValidator(unittest.TestCase):
    def test_string_number_too_long(self):
        validator = MobileNumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = "078123456789101112"

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_MOBILE_NUMBER"], str(ite.exception))

    def test_string_invalid_chars(self):
        validator = MobileNumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = "`-tykg07812345678"

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_MOBILE_NUMBER"], str(ite.exception))

    def test_non_numeric_string_invalid(self):
        validator = MobileNumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = "07812e45678"

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_MOBILE_NUMBER"], str(ite.exception))

    def test_numeric_exponential_invalid(self):
        validator = MobileNumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = "2E2"

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_MOBILE_NUMBER"], str(ite.exception))

    def test_space_invalid(self):
        validator = MobileNumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = " "

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_MOBILE_NUMBER"], str(ite.exception))

    def test_brackets_valid(self):
        validator = MobileNumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = "(07812) {395623}"

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail("Valid phone number raised StopValidation")

    def test_country_code_valid(self):
        validator = MobileNumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = "+0447812 395623"

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail("Valid phone number raised StopValidation")
