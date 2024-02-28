from unittest import mock

from app.authentication.authenticator import decrypt_token
from tests.integration.app_context_test_case import AppContextTestCase
from tests.integration.create_token import (
    PAYLOAD_V2_BUSINESS,
    PAYLOAD_V2_SOCIAL,
    PAYLOAD_V2_SUPPLEMENTARY_DATA,
)
from tests.integration.integration_test_case import IntegrationTestCase

EXPECTED_TOKEN_BUSINESS = {
    "account_service_url": "http://upstream.url",
    "case_id": "1001",
    "collection_exercise_sid": "789",
    "exp": 1709058195.091798,
    "iat": 1709054595.091798,
    "jti": "1001",
    "language_code": "en",
    "response_expires_at": "2024-02-28T09:59:43.109276+00:00",
    "response_id": "1234567890123456",
    "roles": [],
    "schema_name": "test_metadata_routing.json",
    "survey_metadata": {
        "data": {
            "display_address": "68 Abingdon Road, Goathill",
            "employment_date": "1983-06-02",
            "flag_1": 123,
            "link": "https://example.com",
            "period_id": "202402",
            "period_str": "April 2016",
            "ref_p_end_date": "2016-04-30",
            "ref_p_start_date": "2016-04-01",
            "ru_name": "Integration Testing",
            "ru_ref": "12345678901A",
            "trad_as": "Integration Tests",
            "user_id": "integration-test",
        }
    },
    "tx_id": "1001",
    "version": "v2",
}
EXPECTED_TOKEN_SOCIAL = {
    "account_service_url": "http://upstream.url",
    "case_id": "1001",
    "collection_exercise_sid": "789",
    "exp": 1709058195.091798,
    "iat": 1709054595.091798,
    "jti": "1001",
    "language_code": "en",
    "response_expires_at": "2024-02-28T09:59:43.109276+00:00",
    "response_id": "1234567890123456",
    "roles": [],
    "schema_name": "social_demo.json",
    "survey_metadata": {
        "data": {
            "case_ref": "1000000000000001",
            "date": "2016-05-12",
            "flag_1": True,
            "qid": PAYLOAD_V2_SOCIAL["survey_metadata"]["data"]["qid"],
            "user_id": "64389274239",
        },
        "receipting_keys": ["qid"],
    },
    "tx_id": "1001",
    "version": "v2",
}


class TestCreateToken(IntegrationTestCase, AppContextTestCase):
    """
    The purpose of this test class is to test the creation of a token (from create_token.py) to ensure
    metadata in a decrypted token is nested/found in the correct level.
    """

    # Patches are used since the values "uuid4", "time" and "get_response_expires_at" return are dynamic
    @mock.patch("tests.integration.create_token.uuid4")
    @mock.patch(
        "tests.integration.create_token.time",
    )
    @mock.patch(
        "tests.integration.create_token.get_response_expires_at",
    )
    def test_payload_content_and_structure_from_token(
        self, mock_response_expiry_time, mock_time, mock_uuid
    ):
        mock_uuid.return_value = 1001
        mock_time.return_value = 1709054595.091798
        mock_response_expiry_time.return_value = "2024-02-28T09:59:43.109276+00:00"
        test_parameters = [
            {
                "schema": "test_metadata_routing.json",
                "theme": "default",
                "additional_payload": {
                    "flag_1": 123,
                    "period_id": "202402",
                    "link": "https://example.com",
                },
                "payload": PAYLOAD_V2_BUSINESS,
                "expected_token": EXPECTED_TOKEN_BUSINESS,
            },
            {
                "schema": "social_demo.json",
                "theme": "social",
                "additional_payload": {
                    "flag_1": True,
                    "user_id": "64389274239",
                    "date": "2016-05-12",
                },
                "payload": PAYLOAD_V2_SOCIAL,
                "expected_token": EXPECTED_TOKEN_SOCIAL,
            },
        ]
        for value in test_parameters:
            with self.subTest():
                additional_payload = value["additional_payload"]
                token = self.token_generator.create_token_v2(
                    schema_name=value["schema"],
                    theme=value["theme"],
                    **additional_payload,
                )

                with self.test_app.app_context():
                    decrypted_token = decrypt_token(token)
                    self.assertEqual(value["expected_token"], decrypted_token)

    def test_uuid_consistent_after_decryption(self):
        token = self.token_generator.create_token_v2(
            "test_checkbox.json", theme="social", value="Dummy Text"
        )
        with self.test_app.app_context():
            decrypted_token = decrypt_token(token)
            assert decrypted_token["survey_metadata"] == {
                "data": {
                    "case_ref": "1000000000000001",
                    "qid": PAYLOAD_V2_SOCIAL["survey_metadata"]["data"]["qid"],
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
            assert decrypted_token["survey_metadata"] == {
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
                    decrypted_token = decrypt_token(values["token"])
                    self.assertNotIn(values["removed_metadata"], decrypted_token)
