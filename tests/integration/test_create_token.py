from app.authentication.authenticator import decrypt_token
from tests.integration.app_context_test_case import AppContextTestCase
from tests.integration.create_token import (
    PAYLOAD_V2_BUSINESS,
    PAYLOAD_V2_SOCIAL,
    PAYLOAD_V2_SUPPLEMENTARY_DATA,
)
from tests.integration.integration_test_case import IntegrationTestCase

test_parameters = [
    {
        "schema": "test_metadata_routing.json",
        "theme": "default",
        "additional_payload": {
            "flag_1": 123,
            "period_id": "abc",
            "link": "https://example.com",
        },
        "payload": PAYLOAD_V2_BUSINESS,
    },
    {
        "schema": "social_demo.json",
        "theme": "social",
        "additional_payload": {
            "flag_1": True,
            "user_id": "abc",
            "date": "2016-05-12",
        },
        "payload": PAYLOAD_V2_SOCIAL,
    },
]


class TestCreateToken(IntegrationTestCase, AppContextTestCase):
    """
    The purpose of this test class is to test the creation of a token (from create_token.py) to ensure
    metadata in a decrypted token is nested/found in the correct level.
    """

    def test_payload_from_token(self):
        for value in test_parameters:
            with self.subTest():
                additional_payload = value.get("additional_payload")
                token = self.token_generator.create_token_v2(
                    schema_name=value.get("schema"),
                    theme=value.get("theme"),
                    **additional_payload,
                )
                with self.test_app.app_context():
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
            "test_checkbox.json", theme="social", value="Dummy Text"
        )
        with self.test_app.app_context():
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

    def test_sds_metadata_included_in_token(self):
        token = self.token_generator.create_supplementary_data_token(
            "test_checkbox.json"
        )
        with self.test_app.app_context():
            decrypted_token = decrypt_token(token)
            self.assertEqual(
                decrypted_token, PAYLOAD_V2_SUPPLEMENTARY_DATA | decrypted_token
            )

    def test_additional_payload_added_in_token(self):
        token = self.token_generator.create_supplementary_data_token(
            "test_checkbox.json", flag_1=True
        )
        with self.test_app.app_context():
            decrypted_token = decrypt_token(token)
            assert decrypted_token.get("survey_metadata") == {
                "data": {
                    "display_address": "68 Abingdon Road, Goathill",
                    "employment_date": "1983-06-02",
                    "flag_1": True,
                    "period_id": "201604",
                    "period_str": "April 2016",
                    "ref_p_end_date": "2016-04-30",
                    "ref_p_start_date": "2016-04-01",
                    "ru_name": "Integration Testing",
                    "ru_ref": "12345678901A",
                    "sds_dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
                    "survey_id": "123",
                    "trad_as": "Integration Tests",
                    "user_id": "integration-test",
                }
            }

    def test_metadata_is_removed_from_token(self):
        metadata_tokens = [
            {
                "token": self.token_generator.create_token_without_jti(
                    "test_number.json"
                ),
                "removed_metadata": "jti",
            },
            {
                "token": self.token_generator.create_token_without_case_id(
                    "test_numbers.json"
                ),
                "removed_metadata": "case_id",
            },
            {
                "token": self.token_generator.create_token_without_trad_as(
                    "test_numbers.json"
                ),
                "removed_metadata": "trad_as",
            },
        ]
        for values in metadata_tokens:
            with self.subTest():
                with self.test_app.app_context():
                    decrypted_token = decrypt_token(values.get("token"))
                    self.assertNotIn(values.get("removed_metadata"), decrypted_token)
