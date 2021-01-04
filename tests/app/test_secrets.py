from unittest import TestCase

from app.secrets import REQUIRED_SECRETS, validate_required_secrets


class TestSecrets(TestCase):
    def test_validate_required_secrets_fails_on_missing(self):

        secrets = {"secrets": {}}

        with self.assertRaises(Exception) as exception:
            validate_required_secrets(secrets)

        self.assertIn(
            "Missing Secret [EQ_SERVER_SIDE_STORAGE_USER_ID_SALT]",
            str(exception.exception),
        )

    def test_validate_required_secrets_passes(self):
        secrets = {"secrets": {secret: "abc" for secret in REQUIRED_SECRETS}}
        self.assertIsNone(validate_required_secrets(secrets))

    def test_validate_required_secrets_fails_on_conditional_secret(self):
        secrets = {"secrets": {secret: "abc" for secret in REQUIRED_SECRETS}}

        with self.assertRaises(Exception) as exception:
            validate_required_secrets(
                secrets, additional_required_secrets=["MY_REQUIRED_SECRET"]
            )

            self.assertIn(
                "Missing Secret [MY_REQUIRED_SECRET]",
                str(exception.exception),
            )
