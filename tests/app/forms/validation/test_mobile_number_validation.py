import unittest
from unittest.mock import Mock, patch

from wtforms.validators import ValidationError

from app.forms import error_messages
from app.forms.validators import MobileNumberCheck, sanitise_mobile_number


# pylint: disable=no-member
@patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="en_GB"))
class TestPhoneNumberValidator(unittest.TestCase):
    def test_sanitise_mobile_number(self):
        assert sanitise_mobile_number("0.7.7.0.0.9.0.0.1.1.1.") == "7700900111"
        assert sanitise_mobile_number("0447700\t900222") == "7700900222"
        assert sanitise_mobile_number("07700-(900333)") == "7700900333"
        assert sanitise_mobile_number("/0770/090/0444") == "7700900444"
        assert sanitise_mobile_number("00447700 900555") == "7700900555"
        assert sanitise_mobile_number("0447700 900555") == "7700900555"
        assert sanitise_mobile_number("+447700 900666") == "7700900666"
        assert sanitise_mobile_number("[07700] 900777") == "7700900777"
        assert sanitise_mobile_number("(07700) {900888}") == "7700900888"
        assert sanitise_mobile_number("+440447700900999") == "0447700900999"
        assert sanitise_mobile_number(" 09[8./{}756gf}/{h]fgh") == "98756gfhfgh"

    def test_string_number_too_long(self):
        validator = MobileNumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = "7700900111789101112"

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_MOBILE_NUMBER"], str(ite.exception))

    def test_string_invalid_chars(self):
        validator = MobileNumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = "`-tykg07700900222"

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_MOBILE_NUMBER"], str(ite.exception))

    def test_non_numeric_string_invalid(self):
        validator = MobileNumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = "07700e90033"

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_MOBILE_NUMBER"], str(ite.exception))

    def test_non_utf8_string_invalid(self):
        validator = MobileNumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = "൦൧൨൩൪൫൬൭൮൯"

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_MOBILE_NUMBER"], str(ite.exception))
