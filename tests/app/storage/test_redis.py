import uuid
from datetime import datetime, timedelta, timezone

import pytest
from redis.exceptions import ConnectionError as RedisConnectionError

from app.data_models.app_models import EQSession, UsedJtiClaim
from app.storage.errors import ItemAlreadyExistsError
from app.storage.storage import StorageModel
from app.utilities.json import json_loads

EXPIRES_AT = datetime.now(tz=timezone.utc).replace(microsecond=0) + timedelta(minutes=1)


def test_put_jti_stores_empty_value(redis, redis_client):
    used_at = datetime.now(tz=timezone.utc)
    expires_at = used_at + timedelta(seconds=60)

    jti = UsedJtiClaim(str(uuid.uuid4()), expires_at)

    redis.put(jti, overwrite=False)

    stored_data = redis_client.get(jti.jti_claim)

    assert b"" == stored_data


def test_duplicate_put_jti_fails(redis):
    used_at = datetime.now(tz=timezone.utc)
    expires_at = used_at + timedelta(seconds=60)

    jti = UsedJtiClaim(str(uuid.uuid4()), expires_at)

    redis.put(jti, overwrite=False)

    with pytest.raises(ItemAlreadyExistsError):
        redis.put(jti, overwrite=False)


def test_put_session(redis):
    # given
    eq_session = EQSession(
        eq_session_id="sessionid",
        user_id="someuser",
        session_data="somedata",
        expires_at=EXPIRES_AT,
    )
    stored_data = redis.get(EQSession, eq_session.eq_session_id)
    assert stored_data is None

    # when
    redis.put(eq_session)

    # Then
    stored_data = redis.get(EQSession, eq_session.eq_session_id)
    assert stored_data is not None


def test_get_session(redis):
    # Given
    eq_session = EQSession(
        eq_session_id="sessionid",
        user_id="someuser",
        session_data="somedata",
        expires_at=EXPIRES_AT,
    )
    stored_data = redis.get(EQSession, eq_session.eq_session_id)
    assert stored_data is None
    redis.put(eq_session)

    # When
    stored_data = redis.get(EQSession, eq_session.eq_session_id)

    # Then
    for k, v in eq_session.__dict__.items():
        parsed_value = getattr(stored_data, k)
        if isinstance(v, datetime):
            assert v >= parsed_value
        else:
            assert v == parsed_value


def test_delete_session(redis):
    # Given
    eq_session = EQSession(
        eq_session_id="sessionid",
        user_id="someuser",
        session_data="somedata",
        expires_at=EXPIRES_AT,
    )
    redis.put(eq_session)
    session = redis.get(EQSession, "sessionid")
    assert session.eq_session_id == eq_session.eq_session_id

    # When
    redis.delete(eq_session)

    # Then
    assert redis.get(EQSession, "sessionid") is None


def test_redis_does_not_store_key_field_in_value(redis, redis_client):
    # Given
    eq_session = EQSession(
        eq_session_id="sessionid",
        user_id="someuser",
        session_data="somedata",
        expires_at=EXPIRES_AT,
    )
    stored_data = redis.get(EQSession, eq_session.eq_session_id)
    assert stored_data is None
    redis.put(eq_session)

    # When
    stored_data = redis_client.get(eq_session.eq_session_id)

    storage_model = StorageModel(model_type=EQSession)

    assert storage_model.key_field not in json_loads(stored_data)


def test_get_redis_expiry_when_expiry_set(redis, redis_client):
    # Given
    eq_session = EQSession(
        eq_session_id="sessionid",
        user_id="someuser",
        session_data="somedata",
        expires_at=EXPIRES_AT,
    )
    # When
    redis.put(eq_session)

    # Then
    expires_in = redis_client.ttl(eq_session.eq_session_id)
    assert expires_in > 0


# @pytest.mark.usefixtures("app")
def test_get_redis_expiry_when_expiry_not_set(redis, redis_client, mocker):
    # Given
    eq_session = EQSession(
        eq_session_id="sessionid",
        user_id="someuser",
        session_data="somedata",
        expires_at=EXPIRES_AT,
    )

    # When
    mock_expiry_field = mocker.patch(
        "app.storage.storage.StorageModel.expiry_field",
        new_callable=mocker.PropertyMock,
    )
    mock_expiry_field.return_value = None
    redis.put(eq_session)

    # Then
    expires_in = redis_client.ttl(eq_session.eq_session_id)
    assert expires_in == -1


def test_put_handles_connection_error_once(redis, mocker):
    # Given
    used_at = datetime.now(tz=timezone.utc)
    expires_at = used_at + timedelta(seconds=60)
    jti = UsedJtiClaim(str(uuid.uuid4()), expires_at)

    redis.client.set = mocker.Mock(
        side_effect=[RedisConnectionError, RedisConnectionError]
    )

    # When
    with pytest.raises(RedisConnectionError):
        redis.put(jti, overwrite=False)

    # Then
    assert redis.client.set.call_count == 2


def test_get_handles_connection_error_once(redis, mocker):
    # Given
    redis.client.get = mocker.Mock(
        side_effect=[RedisConnectionError, RedisConnectionError]
    )

    # When
    with pytest.raises(RedisConnectionError):
        redis.get(EQSession, "test")

    # Then
    assert redis.client.get.call_count == 2


def test_delete_handles_connection_error_once(redis, mocker):
    # Given
    used_at = datetime.now(tz=timezone.utc)
    expires_at = used_at + timedelta(seconds=60)
    jti = UsedJtiClaim(str(uuid.uuid4()), expires_at)

    redis.client.delete = mocker.Mock(
        side_effect=[RedisConnectionError, RedisConnectionError]
    )

    # When
    with pytest.raises(RedisConnectionError):
        redis.delete(jti)

    # Then
    assert redis.client.delete.call_count == 2
