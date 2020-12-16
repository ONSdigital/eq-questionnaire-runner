from datetime import datetime, timedelta, timezone

from freezegun import freeze_time
from jose import jwt

from app.helpers import get_address_lookup_api_auth_token
from app.helpers.uuid_helper import is_valid_uuid
from tests.app.app_context_test_case import AppContextTestCase


class TestAddressLookupApiAuthToken(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self.test_app.config["ADDRESS_LOOKUP_API_AUTH_ENABLED"] = True

    time_to_freeze = datetime.now(timezone.utc).replace(second=0, microsecond=0)

    @freeze_time(time_to_freeze)
    def test_get_address_lookup_api_auth_token(self):
        with self.app_request_context("/status"):
            secret = self.test_app.eq["secret_store"].get_secret_by_name(
                "ADDRESS_LOOKUP_API_AUTH_TOKEN_SECRET"
            )
            session_timeout = self.test_app.config["EQ_SESSION_TIMEOUT_SECONDS"]
            leeway = self.test_app.config[
                "ADDRESS_LOOKUP_API_AUTH_TOKEN_LEEWAY_IN_SECONDS"
            ]

            expiry_seconds = session_timeout + leeway
            expiry_time = datetime.utcnow() + timedelta(seconds=expiry_seconds)

            token = get_address_lookup_api_auth_token()
            decoded_token = jwt.decode(token, secret, algorithms="HS256")

            assert len(decoded_token) == 3
            assert decoded_token["iss"] == "eq"
            assert decoded_token["exp"] == expiry_time.timestamp()
            assert is_valid_uuid(decoded_token["jti"])
