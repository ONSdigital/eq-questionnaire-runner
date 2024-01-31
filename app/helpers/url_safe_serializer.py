from flask import current_app
from flask import session as cookie_session
from itsdangerous import URLSafeSerializer

from app.settings import EQ_SESSION_ID


def url_safe_serializer() -> URLSafeSerializer:
    # Type Ignore: Changing secret key at this point would be too late.
    return URLSafeSerializer(current_app.secret_key, salt=cookie_session[EQ_SESSION_ID]) # type: ignore
