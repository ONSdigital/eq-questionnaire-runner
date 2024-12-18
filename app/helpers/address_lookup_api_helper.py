from datetime import datetime, timezone
from uuid import uuid4

from flask import current_app
from jwcrypto import jwk, jwt
from jwcrypto.common import base64url_encode


def get_jwk_from_secret(secret: str) -> jwk.JWK:
    return jwk.JWK(kty="oct", k=base64url_encode(secret.encode("utf-8")))


def get_address_lookup_api_auth_token() -> str | None:
    if current_app.config["ADDRESS_LOOKUP_API_AUTH_ENABLED"]:
        secret = current_app.eq["secret_store"].get_secret_by_name(  # type: ignore
            "ADDRESS_LOOKUP_API_AUTH_TOKEN_SECRET"
        )
        session_timeout = current_app.config["EQ_SESSION_TIMEOUT_SECONDS"]
        leeway = current_app.config["ADDRESS_LOOKUP_API_AUTH_TOKEN_LEEWAY_IN_SECONDS"]
        expiry_time = (
            int(datetime.now(timezone.utc).timestamp()) + session_timeout + leeway
        )

        token = jwt.JWT(
            header={"alg": "HS256"},
            claims={
                "exp": expiry_time,
                "jti": str(uuid4()),
                "iss": "eq",
            },
        )
        key = get_jwk_from_secret(secret)
        token.make_signed_token(key)
        serialised_token: str = token.serialize()

        return serialised_token
