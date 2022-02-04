from datetime import datetime, timezone

from flask import Flask
from freezegun import freeze_time
from jwcrypto import jwt

from app.helpers import get_address_lookup_api_auth_token
from app.helpers.address_lookup_api_helper import get_jwk_from_secret
from app.helpers.uuid_helper import is_valid_uuid
from app.utilities.json import json_loads

time_to_freeze = datetime.now(timezone.utc).replace(second=0, microsecond=0)


@freeze_time(time_to_freeze)
def test_get_address_lookup_api_auth_token(app: Flask):
    with app.test_request_context("/status"):
        app.config["ADDRESS_LOOKUP_API_AUTH_ENABLED"] = True
        secret = app.eq["secret_store"].get_secret_by_name(
            "ADDRESS_LOOKUP_API_AUTH_TOKEN_SECRET"
        )
        session_timeout = app.config["EQ_SESSION_TIMEOUT_SECONDS"]
        leeway = app.config["ADDRESS_LOOKUP_API_AUTH_TOKEN_LEEWAY_IN_SECONDS"]
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
