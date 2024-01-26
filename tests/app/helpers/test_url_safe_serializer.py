from uuid import uuid4

import pytest
from flask import Flask
from flask import session as cookie_session
from itsdangerous import BadSignature

from app.helpers import url_safe_serializer
from app.settings import EQ_SESSION_ID


def test_safe_serializer_deserializes(app: Flask):
    test_string = "test-string"

    with app.test_request_context("/status"):
        cookie_session[EQ_SESSION_ID] = str(uuid4())
        serialized_param = url_safe_serializer().dumps("test-string")
        deserialized_param = url_safe_serializer().loads(serialized_param)
        assert test_string == deserialized_param


def test_safe_serializer_raises_bad_signature_when_salts_differ(app: Flask):
    with app.test_request_context("/status"):
        cookie_session[EQ_SESSION_ID] = str(uuid4())

        serialized_param = url_safe_serializer().dumps("test-string")

        cookie_session[EQ_SESSION_ID] = str(uuid4())

        with pytest.raises(BadSignature):
            url_safe_serializer().loads(serialized_param)


def test_safe_serializer_raises_value_error_when_secret_key_is_none(app: Flask):
    app.secret_key = None
    with app.test_request_context():
        with pytest.raises(ValueError):
            url_safe_serializer()
