from datetime import datetime, timezone

from freezegun import freeze_time
from jwcrypto import jwt

from app.helpers import get_address_lookup_api_auth_token
from app.helpers.address_lookup_api_helper import get_jwk_from_secret
from app.helpers.uuid_helper import is_valid_uuid
from app.utilities.json import json_loads
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
            expiry_time = (
                int(datetime.now(timezone.utc).timestamp()) + session_timeout + leeway
            )

            token = get_address_lookup_api_auth_token()
            key = get_jwk_from_secret(secret)
            decoded_token = jwt.JWT(key=key, jwt=token)
            claims = json_loads(decoded_token.claims)

            assert claims["iss"] == "eq"
            assert claims["exp"] == expiry_time
            assert is_valid_uuid(claims["jti"])
