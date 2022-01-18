from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from app.authentication.jti_claim_storage import JtiTokenUsed, use_jti_claim
from app.storage.errors import ItemAlreadyExistsError


def test_should_use_token(app, mock_redis_put):
    with app.app_context():
        # Given
        jti_token = str(uuid4())
        expires_at = datetime.now(tz=timezone.utc) + timedelta(seconds=60)

        # When
        use_jti_claim(jti_token, expires_at)

        # Then
        assert mock_redis_put.call_count == 1


def test_should_return_raise_value_error():
    # Given
    token = None
    expires_at = datetime.now(tz=timezone.utc) + timedelta(seconds=60)

    # When
    with pytest.raises(ValueError):
        use_jti_claim(token, expires_at)


def test_should_raise_jti_token_used_when_token_already_exists(app, mock_redis_put):
    with app.app_context():
        # Given
        jti_token = str(uuid4())
        expires_at = datetime.now(tz=timezone.utc) + timedelta(seconds=60)

        # When
        with pytest.raises(JtiTokenUsed) as excinfo:
            mock_redis_put.side_effect = [ItemAlreadyExistsError()]
            use_jti_claim(jti_token, expires_at)

        # Then
        assert str(excinfo.value) == f"jti claim '{jti_token}' has already been used"


def test_should_raise_type_error_invalid_uuid():
    jti_token = "jti_token"
    expires_at = datetime.now(tz=timezone.utc) + timedelta(seconds=60)

    with pytest.raises(TypeError):
        use_jti_claim(jti_token, expires_at)
