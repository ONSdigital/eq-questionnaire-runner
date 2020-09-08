import json
import uuid
from datetime import datetime, timedelta
from unittest import mock

import fakeredis
from dateutil.tz import tzutc

from app.data_models.app_models import EQSession, UsedJtiClaim
from app.storage.errors import ItemAlreadyExistsError
from app.storage.redis import Redis
from app.storage.storage import StorageModel
from tests.app.app_context_test_case import AppContextTestCase

EXPIRES_AT = datetime.now(tz=tzutc()).replace(microsecond=0) + timedelta(minutes=1)


class TestRedis(AppContextTestCase):
    def setUp(self):
        super().setUp()

        self.mock_client = fakeredis.FakeStrictRedis()

        self.redis = Redis(self.mock_client)

    def test_put_jti_stores_empty_value(self):
        used_at = datetime.now()
        expires_at = used_at + timedelta(seconds=60)

        jti = UsedJtiClaim(str(uuid.uuid4()), expires_at)

        self.redis.put(jti, overwrite=False)

        stored_data = self.mock_client.get(jti.jti_claim)

        self.assertEqual(b"", stored_data)

    def test_duplicate_put_jti_fails(self):
        used_at = datetime.now()
        expires_at = used_at + timedelta(seconds=60)

        jti = UsedJtiClaim(str(uuid.uuid4()), expires_at)

        self.redis.put(jti, overwrite=False)

        with self.assertRaises(ItemAlreadyExistsError):
            self.redis.put(jti, overwrite=False)

    def test_put_session(self):
        # given
        eq_session = EQSession(
            eq_session_id="sessionid",
            user_id="someuser",
            session_data="somedata",
            expires_at=EXPIRES_AT,
        )
        stored_data = self.redis.get(EQSession, eq_session.eq_session_id)
        self.assertIsNone(stored_data)

        # when
        self.redis.put(eq_session)

        # Then
        stored_data = self.redis.get(EQSession, eq_session.eq_session_id)
        self.assertIsNotNone(stored_data)

    def test_get_session(self):
        # Given
        eq_session = EQSession(
            eq_session_id="sessionid",
            user_id="someuser",
            session_data="somedata",
            expires_at=EXPIRES_AT,
        )
        stored_data = self.redis.get(EQSession, eq_session.eq_session_id)
        self.assertIsNone(stored_data)
        self.redis.put(eq_session)

        # When
        stored_data = self.redis.get(EQSession, eq_session.eq_session_id)

        # Then
        for k, v in eq_session.__dict__.items():
            parsed_value = getattr(stored_data, k)
            if isinstance(v, datetime):
                self.assertGreaterEqual(v, parsed_value)
            else:
                self.assertEqual(v, parsed_value)

    def test_delete_session(self):
        # Given
        eq_session = EQSession(
            eq_session_id="sessionid",
            user_id="someuser",
            session_data="somedata",
            expires_at=EXPIRES_AT,
        )
        self.redis.put(eq_session)
        session = self.redis.get(EQSession, "sessionid")
        self.assertEqual(session.eq_session_id, eq_session.eq_session_id)

        # When
        self.redis.delete(eq_session)

        # Then
        self.assertIsNone(self.redis.get(EQSession, "sessionid"))

    def test_redis_does_not_store_key_field_in_value(self):
        # Given
        eq_session = EQSession(
            eq_session_id="sessionid",
            user_id="someuser",
            session_data="somedata",
            expires_at=EXPIRES_AT,
        )
        stored_data = self.redis.get(EQSession, eq_session.eq_session_id)
        self.assertIsNone(stored_data)
        self.redis.put(eq_session)

        # When
        stored_data = self.mock_client.get(eq_session.eq_session_id)

        storage_model = StorageModel(model_type=EQSession)

        assert storage_model.key_field not in json.loads(stored_data)

    def test_get_redis_expiry_when_expiry_set(self):
        # Given
        eq_session = EQSession(
            eq_session_id="sessionid",
            user_id="someuser",
            session_data="somedata",
            expires_at=EXPIRES_AT,
        )
        # When
        self.redis.put(eq_session)

        # Then
        expires_in = self.mock_client.ttl(eq_session.eq_session_id)
        assert expires_in > 0

    def test_get_redis_expiry_when_expiry_not_set(self):
        # Given
        eq_session = EQSession(
            eq_session_id="sessionid",
            user_id="someuser",
            session_data="somedata",
            expires_at=EXPIRES_AT,
        )

        # When
        with mock.patch(
            "app.storage.storage.StorageModel.expiry_field",
            new_callable=mock.PropertyMock,
        ) as mock_expiry_field:
            mock_expiry_field.return_value = None
            self.redis.put(eq_session)

        # Then
        expires_in = self.mock_client.ttl(eq_session.eq_session_id)
        assert expires_in == -1
