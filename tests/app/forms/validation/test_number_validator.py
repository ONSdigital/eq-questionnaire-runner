import unittest
from unittest.mock import Mock, patch

from wtforms.validators import StopValidation, ValidationError

from app.forms import error_messages
from app.forms.validators import DecimalPlaces, NumberCheck


# pylint: disable=no-member
@patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="en_GB"))
class TestNumberValidator(unittest.TestCase):
    """
    Number validator uses the raw data from the input, which is in a list
    """

    def test_none_invalid(self):
        validator = NumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = [None]

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_NUMBER"], str(ite.exception))

    def test_empty_string_invalid(self):
        validator = NumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = [""]

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_NUMBER"], str(ite.exception))

    def test_non_numeric_string_invalid(self):
        validator = NumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ["a"]

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_NUMBER"], str(ite.exception))

    def test_numeric_exponential_invalid(self):
        validator = NumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ["2E2"]

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_NUMBER"], str(ite.exception))

    def test_decimal_number_invalid(self):
        validator = DecimalPlaces(2)

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ["1.234"]

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        error_message = error_messages["INVALID_DECIMAL"] % {"max": 2}
        self.assertEqual(error_message, str(ite.exception))

    def test_space_invalid(self):
        validator = NumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = [" "]

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_NUMBER"], str(ite.exception))

    def test_zero_valid(self):
        validator = NumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ["0"]

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail("Valid number raised StopValidation")

    def test_positive_number_valid(self):
        validator = NumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ["10"]

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail("Valid number raised StopValidation")

    def test_negative_number_valid(self):
        validator = NumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ["-10"]

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail("Valid number raised StopValidation")
