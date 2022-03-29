import pytest

from app.secrets import REQUIRED_SECRETS, validate_required_secrets


def test_validate_required_secrets_fails_on_missing():
    secrets = {"secrets": {}}

    with pytest.raises(Exception) as exception:
        validate_required_secrets(secrets)

        assert "Missing Secret [EQ_SERVER_SIDE_STORAGE_USER_ID_SALT]" in str(
            exception.exception
        )


def test_validate_required_secrets_passes():
    secrets = {"secrets": {secret: "abc" for secret in REQUIRED_SECRETS}}
    assert validate_required_secrets(secrets) is None


def test_validate_required_secrets_fails_on_conditional_secret():
    secrets = {"secrets": {secret: "abc" for secret in REQUIRED_SECRETS}}

    with pytest.raises(Exception) as exception:
        validate_required_secrets(
            secrets, additional_required_secrets=["MY_REQUIRED_SECRET"]
        )

        assert "Missing Secret [MY_REQUIRED_SECRET]" in str(exception.exception)
