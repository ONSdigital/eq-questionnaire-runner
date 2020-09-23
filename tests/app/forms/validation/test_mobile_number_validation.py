import unittest
from unittest.mock import Mock, patch

from wtforms.validators import ValidationError

from app.forms import error_messages
from app.forms.validators import MobileNumberCheck, sanitise_mobile_number


# pylint: disable=no-member
@patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="en_GB"))
class TestPhoneNumberValidator(unittest.TestCase):
    def test_sanitise_mobile_number(self):
        assert sanitise_mobile_number("0.7.8.1.2.3.9.5.6.2.3.") == "7812395623"
        assert sanitise_mobile_number("0447812\t395623") == "7812395623"
        assert sanitise_mobile_number("07812-(395623)") == "7812395623"
        assert sanitise_mobile_number("/0781/239/5623") == "7812395623"
        assert sanitise_mobile_number("0447812 395623") == "7812395623"
        assert sanitise_mobile_number("+0447812 395623") == "7812395623"
        assert sanitise_mobile_number("[07812] 395623") == "7812395623"
        assert sanitise_mobile_number("(07812) {395623}") == "7812395623"
        assert sanitise_mobile_number("+044044789345") == "044789345"
        assert sanitise_mobile_number(" 09[8./{}756gf}/{h]fgh") == "98756gfhfgh"

    def test_string_number_too_long(self):
        validator = MobileNumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = "078123456789101112"

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_MOBILE_NUMBER"], str(ite.exception))

    def test_string_invalid_chars(self):
        validator = MobileNumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = "`-tykg07812345678"

        with self.assertRaises(ValidationError) as ite:
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

    def test_valid_mobile_number(self):
        validator = MobileNumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = "+0447812 395623"

        try:
            validator(mock_form, mock_field)
        except ValidationError:
            self.fail("Valid phone number raised ValidationError")
