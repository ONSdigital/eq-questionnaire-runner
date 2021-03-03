import unittest
from unittest.mock import Mock

from wtforms.validators import ValidationError

from app.forms import error_messages
from app.forms.validators import EmailTLDCheck


class TestEmailTLDValidator(unittest.TestCase):
    def test_tld_single_character(self):
        validator = EmailTLDCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = "a@a.a"

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_EMAIL_FORMAT"], str(ite.exception))

    def test_tld_non_alpha_character(self):
        validator = EmailTLDCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = "a@a.a9"

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_EMAIL_FORMAT"], str(ite.exception))

    def test_tld_invalid_unicode(self):
        validator = EmailTLDCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = "a@a.\x94"

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages["INVALID_EMAIL_FORMAT"], str(ite.exception))
