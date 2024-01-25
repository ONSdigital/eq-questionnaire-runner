import uuid

from sdc.crypto.key_store import KeyStore

from app.authentication.auth_payload_versions import AuthPayloadVersion
from app.authentication.authenticator import decrypt_token
from profile_application import app
from tests.integration.create_token import (
    ACCOUNT_SERVICE_URL,
    PAYLOAD_V2_SOCIAL,
    PAYLOAD_V2_SUPPLEMENTARY_DATA,
    TokenGenerator,
)
from tests.integration.integration_test_case import (
    EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_KID,
    KEYS_DICT,
    SR_USER_AUTHENTICATION_PUBLIC_KEY_KID,
    IntegrationTestCase,
)

key_store = KeyStore(KEYS_DICT)

token_generator = TokenGenerator(
    key_store,
    EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_KID,
    SR_USER_AUTHENTICATION_PUBLIC_KEY_KID,
)

test_parameters = [
    {
        "schema": "test_metadata_routing.json",
        "theme": "default",
        "additional_payload": {
            "flag_1": 123,
            "period_id": "abc",
            "link": "https://example.com",
        },
        "payload": {
            "version": AuthPayloadVersion.V2.value,
            "survey_metadata": {
                "data": {
                    "user_id": "integration-test",
                    "period_str": "April 2016",
                    "period_id": "201604",
                    "ru_ref": "12345678901A",
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
        },
    },
    {
        "schema": "social_demo.json",
        "theme": "social",
        "additional_payload": {
            "flag_1": True,
            "user_id": "abc",
            "date": "2016-05-12",
        },
        "payload": {
            "version": AuthPayloadVersion.V2.value,
            "survey_metadata": {
                "data": {
                    "case_ref": "1000000000000001",
                    "qid": str(uuid.uuid4()),
                },
                "receipting_keys": ["qid"],
            },
            "collection_exercise_sid": "789",
            "response_id": "1234567890123456",
            "language_code": "en",
            "roles": [],
            "account_service_url": ACCOUNT_SERVICE_URL,
        },
    },
]


class TestCreateToken(IntegrationTestCase):
    def test_payload_from_token(self):
        for value in test_parameters:
            with self.subTest():
                additional_payload = value.get("additional_payload")
                token = token_generator.create_token_v2(
                    schema_name=value.get("schema"),
                    theme=value.get("theme"),
                    **additional_payload,
                )
                with app.app_context():
                    decrypted_token = decrypt_token(token)
                    self.assertEqual(
                        decrypted_token, value.get("payload") | decrypted_token
                    )
                    assert (
                        additional_payload.items()
                        <= decrypted_token.get("survey_metadata").get("data").items()
                    )

    def test_uuid_consistent_after_decryption(self):
        token = self.token_generator.create_token_v2(
            "social_demo.json", theme="social", value="Dummy Text"
        )
        with app.app_context():
            decrypted_token = decrypt_token(token)
            assert decrypted_token.get("survey_metadata") == {
                "data": {
                    "case_ref": "1000000000000001",
                    "qid": PAYLOAD_V2_SOCIAL.get("survey_metadata")
                    .get("data")
                    .get("qid"),
                    "value": "Dummy Text",
                },
                "receipting_keys": ["qid"],
            }

    def test_supplementary_data_included_in_token(self):
        token = self.token_generator.create_supplementary_data_token(
            "test_checkbox.json", flag_1=True
        )
        with app.app_context():
            decrypted_token = decrypt_token(token)
            self.assertEqual(
                decrypted_token, PAYLOAD_V2_SUPPLEMENTARY_DATA | decrypted_token
            )
            assert ({"flag_1": True}).items() <= decrypted_token.get(
                "survey_metadata"
            ).get("data").items()

    def test_metadata_is_removed_from_token(self):
        for value in [
            [token_generator.create_token_without_jti, "jti"],
            [token_generator.create_token_without_case_id, "case_id"],
            [token_generator.create_token_without_trad_as, "trad_as"],
        ]:
            with self.subTest():
                token = value[0]("test_numbers.json")
                with app.app_context():
                    decrypted_token = decrypt_token(token)
                    self.assertNotIn(value[1], decrypted_token)
