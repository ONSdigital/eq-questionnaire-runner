from datetime import datetime, timedelta
from uuid import uuid4
import uuid

from dateutil.tz import tzutc
from flask import session as cookie_session
from itsdangerous import BadSignature

from app.data_models.session_data import SessionData
from app.data_models.session_store import SessionStore
from app.helpers import url_safe_serializer
from app.settings import EQ_SESSION_ID
from tests.app.app_context_test_case import AppContextTestCase


class TestUrlSafeSerializer(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self.session_data = SessionData(
            tx_id="tx_id",
            schema_name="some_schema_name",
            response_id="response_id",
            period_str="period_str",
            language_code=None,
            launch_language_code=None,
            survey_url=None,
            ru_name="ru_name",
            ru_ref="ru_ref",
            case_id="case_id",
            questionnaire_id="questionnaire_id",
        )
        self.session_store = SessionStore("user_ik", "pepper", "eq_session_id")
        self.expires_at = datetime.now(tzutc()) + timedelta(seconds=5)

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
