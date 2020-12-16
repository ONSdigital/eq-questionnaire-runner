from datetime import datetime, timedelta
from uuid import uuid4

from flask import current_app
from jose import jwt


def get_address_lookup_api_auth_token():
    if current_app.config["ADDRESS_LOOKUP_API_AUTH_ENABLED"]:
        secret = current_app.eq["secret_store"].get_secret_by_name(
            "ADDRESS_LOOKUP_API_AUTH_TOKEN_SECRET"
        )
        session_timeout = current_app.config["EQ_SESSION_TIMEOUT_SECONDS"]
        leeway = current_app.config["ADDRESS_LOOKUP_API_AUTH_TOKEN_LEEWAY_IN_SECONDS"]
        expiry_seconds = session_timeout + leeway

        payload = {
            "exp": datetime.utcnow() + timedelta(seconds=expiry_seconds),
            "jti": str(uuid4()),
            "iss": "eq",
        }

        return jwt.encode(payload, secret, algorithm="HS256")
