import time
from uuid import uuid4

from sdc.crypto.encrypter import encrypt

from app.authentication.auth_payload_version import AuthPayloadVersion
from app.keys import KEY_PURPOSE_AUTHENTICATION
from tests.app.parser.conftest import get_response_expires_at

ACCOUNT_SERVICE_URL = "http://upstream.url"

PAYLOAD = {
    "user_id": "integration-test",
    "period_str": "April 2016",
    "period_id": "201604",
    "collection_exercise_sid": "789",
    "ru_ref": "123456789012A",
    "response_id": "1234567890123456",
    "ru_name": "Integration Testing",
    "ref_p_start_date": "2016-04-01",
    "ref_p_end_date": "2016-04-30",
    "return_by": "2016-05-06",
    "trad_as": "Integration Tests",
    "employment_date": "1983-06-02",
    "language_code": "en",
    "roles": [],
    "account_service_url": ACCOUNT_SERVICE_URL,
    "display_address": "68 Abingdon Road, Goathill",
}

PAYLOAD_V2_BUSINESS = {
    "version": AuthPayloadVersion.V2.value,
    "survey_metadata": {
        "data": {
            "user_id": "integration-test",
            "period_str": "April 2016",
            "period_id": "201604",
            "ru_ref": "123456789012A",
            "ru_name": "Integration Testing",
            "ref_p_start_date": "2016-04-01",
            "ref_p_end_date": "2016-04-30",
            "trad_as": "Integration Tests",
            "employment_date": "1983-06-02",
            "display_address": "68 Abingdon Road, Goathill",
        }
    },
    "collection_exercise_sid": "789",
    "response_id": "1234567890123456",
    "language_code": "en",
    "roles": [],
    "account_service_url": ACCOUNT_SERVICE_URL,
}

PAYLOAD_V2_SOCIAL = {
    "version": AuthPayloadVersion.V2.value,
    "survey_metadata": {
        "data": {
            "case_ref": "1000000000000001",
            "qid": str(uuid4()),
        },
        "receipting_keys": ["qid"],
    },
    "collection_exercise_sid": "789",
    "response_id": "1234567890123456",
    "language_code": "en",
    "roles": [],
    "account_service_url": ACCOUNT_SERVICE_URL,
}


class TokenGenerator:
    def __init__(self, key_store, upstream_kid, sr_public_kid):
        self._key_store = key_store
        self._upstream_kid = upstream_kid
        self._sr_public_kid = sr_public_kid

    @staticmethod
    def _get_payload_with_params(
        schema_name=None, schema_url=None, payload=PAYLOAD, **extra_payload
    ):  # pylint: disable=dangerous-default-value
        payload_vars = payload.copy()
        payload_vars["tx_id"] = str(uuid4())
        if schema_name:
            payload_vars["schema_name"] = schema_name
        if schema_url:
            payload_vars["schema_url"] = schema_url

        payload_vars["iat"] = time.time()
        payload_vars["exp"] = payload_vars["iat"] + float(3600)  # one hour from now
        payload_vars["jti"] = str(uuid4())
        payload_vars["case_id"] = str(uuid4())
        payload_vars["response_expires_at"] = get_response_expires_at()

        for key, value in extra_payload.items():
            payload_vars[key] = value

        return payload_vars

    def create_token(self, schema_name, **extra_payload):
        payload_vars = self._get_payload_with_params(
            schema_name=schema_name, schema_url=None, **extra_payload
        )

        return self.generate_token(payload_vars)

    def create_token_v2(self, schema_name, theme="default", **extra_payload):
        payload_for_theme = (
            PAYLOAD_V2_SOCIAL if theme == "social" else PAYLOAD_V2_BUSINESS
        )
        payload = self._get_payload_with_params(
            schema_name=schema_name, payload=payload_for_theme, **extra_payload
        )

        return self.generate_token(payload)

    def create_token_invalid_version(self, schema_name, **extra_payload):
        payload = self._get_payload_with_params(
            schema_name=schema_name, payload=PAYLOAD_V2_BUSINESS, **extra_payload
        )

        payload["version"] = "v3"

        return self.generate_token(payload)

    def create_token_without_jti(self, schema_name, **extra_payload):
        payload_vars = self._get_payload_with_params(
            schema_name=schema_name, schema_url=None, **extra_payload
        )
        del payload_vars["jti"]

        return self.generate_token(payload_vars)

    def create_token_without_case_id(self, schema_name, **extra_payload):
        payload_vars = self._get_payload_with_params(
            schema_name=schema_name, schema_url=None, **extra_payload
        )
        del payload_vars["case_id"]

        return self.generate_token(payload_vars)

    def create_token_without_trad_as(self, schema_name, **extra_payload):
        payload_vars = self._get_payload_with_params(
            schema_name=schema_name, schema_url=None, **extra_payload
        )
        del payload_vars["trad_as"]

        return self.generate_token(payload_vars)

    def create_token_v2_social_token_invalid_receipting_key(
        self, schema_name, **extra_payload
    ):
        payload_vars = self._get_payload_with_params(
            schema_name=schema_name, payload=PAYLOAD_V2_SOCIAL, **extra_payload
        )
        del payload_vars["survey_metadata"]["data"]["qid"]

        return self.generate_token(payload_vars)

    def create_token_with_schema_url(self, schema_name, schema_url, **extra_payload):
        payload_vars = self._get_payload_with_params(
            schema_name=schema_name, schema_url=schema_url, **extra_payload
        )

        return self.generate_token(payload_vars)

    def generate_token(self, payload):
        return encrypt(payload, self._key_store, KEY_PURPOSE_AUTHENTICATION)
