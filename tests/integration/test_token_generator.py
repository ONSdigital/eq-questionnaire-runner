from sdc.crypto.exceptions import InvalidTokenException
from sdc.crypto.key_store import KeyStore

from app.authentication.authenticator import decrypt_token
from app.routes.session import get_questionnaire_claims
from profile_application import app
from tests.integration.create_token import TokenGenerator
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


class TestTokenGenerator(IntegrationTestCase):
    def get_claims(self, decrypted_token):
        result = get_questionnaire_claims(
            decrypted_token,
            [
                {"name": "user_id", "type": "string"},
                {"name": "period_id", "type": "string"},
                {"name": "flag_1", "type": "boolean"},
                {"name": "ru_name", "type": "string"},
            ],
        )
        return result

    def test_integer_value_for_boolean_type_fails_validation_with_create_token(self):
        token = self.token_generator.create_token("test_metadata_routing", flag_1=123)
        with app.app_context():
            decrypted_token = decrypt_token(token)
            with self.assertRaises(InvalidTokenException) as ex:
                self.get_claims(decrypted_token)
                assert "Invalid questionnaire claims" in str(ex.exception)

    def test_boolean_value_passes_validation_with_create_token(self):
        token = self.token_generator.create_token("test_metadata_routing", flag_1=True)
        with app.app_context():
            decrypted_token = decrypt_token(token)
            result = self.get_claims(decrypted_token)

            assert result == {
                "flag_1": True,
                "period_id": "201604",
                "ru_name": "Integration Testing",
                "user_id": "integration-test",
            }

    def test_flag_1_exists_in_metadata_with_create_token(self):
        token = self.token_generator.create_token("test_metadata_routing", flag_1=True)
        with app.app_context():
            decrypted_token = decrypt_token(token)
            assert "flag_1" in decrypted_token

    def test_integer_value_for_boolean_type_fails_validation_with_create_token_v2(self):
        token = self.token_generator.create_token_v2(
            "test_metadata_routing", flag_1=123
        )
        with app.app_context():
            decrypted_token = decrypt_token(token)
            with self.assertRaises(InvalidTokenException) as ex:
                self.get_claims(decrypted_token)
                assert "Invalid questionnaire claims" in str(ex.exception)

    def test_boolean_value_passes_validation_with_create_token_v2(self):
        token = self.token_generator.create_token_v2(
            "test_metadata_routing", flag_1=True
        )
        with app.app_context():
            decrypted_token = decrypt_token(token)
            # Returns values within "survey_metadata"
            result = self.get_claims(decrypted_token)

            assert result == {
                "display_address": "68 Abingdon Road, Goathill",
                "employment_date": "1983-06-02",
                "flag_1": True,
                "period_id": "201604",
                "period_str": "April 2016",
                "ref_p_end_date": "2016-04-30",
                "ref_p_start_date": "2016-04-01",
                "ru_name": "Integration Testing",
                "ru_ref": "12345678901A",
                "trad_as": "Integration Tests",
                "user_id": "integration-test",
            }

    def test_flag_1_exists_in_survey_metadata_with_create_token_v2(self):
        token = self.token_generator.create_token_v2(
            "test_metadata_routing", flag_1=True
        )
        with app.app_context():
            decrypted_token = decrypt_token(token)
            assert "flag_1" in decrypted_token["survey_metadata"]["data"]
