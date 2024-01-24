from flask import current_app
from flask import session as cookie_session
from itsdangerous import URLSafeSerializer

from app.settings import EQ_SESSION_ID


def url_safe_serializer() -> URLSafeSerializer:
    secret_key = current_app.secret_key
    if secret_key is None:
        raise ValueError("Flask application secret key is not set.")
    return URLSafeSerializer(secret_key, salt=cookie_session[EQ_SESSION_ID])
