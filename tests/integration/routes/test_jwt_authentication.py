import logging
import random
import string
import time
import unittest
import uuid

from sdc.crypto.encrypter import encrypt
from sdc.crypto.key_store import KeyStore

from app.keys import KEY_PURPOSE_AUTHENTICATION
from tests.app.authentication import (
    TEST_DO_NOT_USE_SR_PUBLIC_KEY,
    TEST_DO_NOT_USE_UPSTREAM_PRIVATE_KEY,
)
from tests.app.parser.conftest import get_response_expires_at
from tests.integration.app_context_test_case import AppContextTestCase
from tests.integration.integration_test_case import (
    EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_KID,
    SR_USER_AUTHENTICATION_PUBLIC_KEY_KID,
)


class FlaskClientAuthenticationTestCase(AppContextTestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

        super().setUp()
        self.client = self._app.test_client(use_cookies=False)

    def test_no_token(self):
        response = self.client.get("/session")
        self.assertEqual(401, response.status_code)

    def test_invalid_token(self):
        token = "invalid"

        response = self.client.get("/session?token=" + token)
        self.assertEqual(403, response.status_code)

    def test_fully_encrypted(self):
        key_store = KeyStore(
            {
                "keys": {
                    SR_USER_AUTHENTICATION_PUBLIC_KEY_KID: {
                        "purpose": KEY_PURPOSE_AUTHENTICATION,
                        "type": "public",
                        "value": TEST_DO_NOT_USE_SR_PUBLIC_KEY,
                    },
                    EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_KID: {
                        "purpose": KEY_PURPOSE_AUTHENTICATION,
                        "type": "private",
                        "value": TEST_DO_NOT_USE_UPSTREAM_PRIVATE_KEY,
                    },
                }
            }
        )

        payload = self.create_payload()

        encrypted_token = encrypt(payload, key_store, KEY_PURPOSE_AUTHENTICATION)

        response = self.client.get("/session?token=" + encrypted_token)
        self.assertEqual(302, response.status_code)

    @staticmethod
    def create_payload():
        iat = time.time()
        exp = time.time() + (5 * 60)
        response_id = "".join(random.choices(string.digits, k=16))
        return {
            "tx_id": str(uuid.uuid4()),
            "jti": str(uuid.uuid4()),
            "case_id": str(uuid.uuid4()),
            "iat": int(iat),
            "exp": int(exp),
            "survey_metadata": {
                "data": {
                    "period_str": "2016-01-01",
                    "period_id": "12",
                    "ref_p_start_date": "2016-01-01",
                    "ref_p_end_date": "2016-09-01",
                    "ru_ref": "12345678901A",
                    "ru_name": "Test",
                    "return_by": "2016-09-09",
                    "user_id": "jimmy",
                }
            },
            "schema_name": "test_default",
            "collection_exercise_sid": "sid",
            "response_id": response_id,
            "account_service_url": "http://upstream.url/",
            "response_expires_at": get_response_expires_at(),
            "version": "v2",
        }


if __name__ == "__main__":
    unittest.main()
