from uuid import uuid4

from flask import session as cookie_session
from itsdangerous import BadSignature

from app.helpers import url_safe_serializer
from app.settings import EQ_SESSION_ID
from tests.app.app_context_test_case import AppContextTestCase


class TestUrlSafeSerializer(AppContextTestCase):
    def test_safe_serializer_deserializes(self):
        test_string = "test-string"

        with self.app_request_context("/status"):
            cookie_session[EQ_SESSION_ID] = str(uuid4())

            serialized_param = url_safe_serializer().dumps("test-string")
            deserialized_param = url_safe_serializer().loads(serialized_param)

            self.assertEqual(test_string, deserialized_param)

    def test_safe_serializer_raises_bad_signature_when_salts_differ(self):
        with self.app_request_context("/status"):
            cookie_session[EQ_SESSION_ID] = str(uuid4())

            serialized_param = url_safe_serializer().dumps("test-string")

            cookie_session[EQ_SESSION_ID] = str(uuid4())

            with self.assertRaises(BadSignature):
                url_safe_serializer().loads(serialized_param)
