import unittest

from wtforms.validators import ValidationError

from app.forms import error_messages
from app.forms.validators import EmailConfirmationLimitExceededCheck


class TestEmailValidation(unittest.TestCase):
    def setUp(self):
        self.validator = EmailConfirmationLimitExceededCheck()

    def test_max_confirmation_limit_exceeded(self):
        with self.assertRaises(ValidationError) as ite:
            self.validator()
        self.assertEqual(
            error_messages["MAX_EMAIL_CONFIRMATION_LIMIT_EXCEEDED"], str(ite.exception)
        )
