import time
from datetime import datetime, timedelta, timezone

import responses
from freezegun import freeze_time
from marshmallow import ValidationError
from mock.mock import patch
from sdc.crypto.key_store import KeyStore

from app.helpers.metadata_helpers import get_ru_ref_without_check_letter
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.services.supplementary_data import SupplementaryDataRequestFailed
from app.settings import ACCOUNT_SERVICE_BASE_URL, ACCOUNT_SERVICE_BASE_URL_SOCIAL
from app.utilities.json import json_loads
from tests.app.services.test_request_supplementary_data import TEST_SDS_URL
from tests.integration.create_token import PAYLOAD_V2_SUPPLEMENTARY_DATA
from tests.integration.integration_test_case import (
    EQ_SUBMISSION_SDX_PRIVATE_KEY,
    EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY,
    EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_KID,
    KEYS_DICT,
    SR_USER_AUTHENTICATION_PUBLIC_KEY_KID,
    IntegrationTestCase,
)

TIME_TO_FREEZE = datetime(2020, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
EQ_SESSION_TIMEOUT_SECONDS = 45 * 60
BUSINESS_URL = ACCOUNT_SERVICE_BASE_URL
SOCIAL_URL = ACCOUNT_SERVICE_BASE_URL_SOCIAL
TEST_SDS_URL = "http://localhost:5003/v1/unit_data"

mock_supplementary_data_payload_missing_data = {
    "dataset_id": "203b2f9d-c500-8175-98db-86ffcfdccfa3",
    "survey_id": "123",
}

mock_supplementary_data_payload_invalid_kid_in_data = {
    "dataset_id": "203b2f9d-c500-8175-98db-86ffcfdccfa3",
    "survey_id": "123",
    # pylint: disable-next=line-too-long
    "data": "eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00iLCJraWQiOiJkZjg4ZmRhZDI2MTJhZTFlODA1NzExMjBlNmM2MzcxZjU1ODk2Njk3In0.lssJXsMUE3dhWtQRUt7DTaZJvx4DpNdLW98cu8g4NijYX9TFpJiOFyzPxUlpFZb-fMa4zW9q6qZofQeQTbl_Ae3QAwGhuWF7v9NMdWM1aH377byyJJyJpdqlU4t-P03evRWZqAG2HtsNE2Zn1ORXn80Dc9IRkzutgrziLI8OBIZeO6-XEgbVCapsQApWkyux7QRdFH95wfda75nVvGqTbBOYvQiMTKd8KzpH2Vl200IOqEpmrcjUCE-yqdTupzcr88hwNI2ZYdv-pTNowJw1FPODZ7V_sE4Ac-JYv3yBTDcXdz3I5-rX8i2HXqz-g3VhveZiAl9q0AgklPkaO_oNWJzjrCb7DZGL4DjiGYuOcw8OSdOpKLXwkExMlado-wigxy1IWoCzFu2E5tWpmLc0WWcjKuBgD7-4tcn059F7GcwhX2uMRESCmc39pblvseM2UnmmQnwr8GvD7gqWdFwtBsECyXQ5UXAxWLJor_MtU8lAFZxiorRcrXZJwAivroPO9iEB-1Mvt2zZFWI_vMgpJCAIpETscotDKMVCG0UMfkKckJqLnmQpvF4oYTr77w1COBX5bi-AV8UrLJ7sVVktSXOBc_KCGRpoImA5cE67hW7mFUdJi1EHA39qt0tTqZD7izpu8sSLxsiuCkfsqrd4uAedcDdQm4QGxXOPD4pxois.wfWsetB3M0x9qfw5.43Wns86lGlbHj63b0ZxE2bxBQVus6FIqelb9LfSbvopLn5oR8FM4vDEnDp_rIyvjmV9YAZJ6HAHaYaWoNyIO0EorgamrB4R3-LqInANoe9c8xLZ9wl_QpE9aWnxsmFGZUWLO3q2fVTPnwBtA_LxK8FD0vjdLL9eHGYEmPVCGVX0BJX04TVW9aoemsx9Yn3ZtfvmQHuROiB-GcA5wOSb-GvhzfplY09GQr7g7221MiYCHYimmEJyxLV5clWPXu6izzVLDyG9l2ewCifiuBLD0O1U_fPlahHTmidwHKJEAEn39biNw5E_dr8WyZ3xBvJa9dP50m0xeyN4COR-xlYcEbuDcKoqN6BnY0bMNDxQYlBO--QcPLQ6h48uTJszwzsmNIwHoi0xy5dQah7c9Nt2lpMuNt1Wix-O8JWYCqaiCKxjwt9G8kabMbzhp1n3LetWweoyV7qJTbiB13Byv6SZwMO9M.8j8wtvwBAHzqRhv5Ii9jjQ",
}


class TestSession(IntegrationTestCase):
    def setUp(self):
        # Cache for requests
        self.last_url = None
        self.last_response = None
        self.last_csrf_token = None
        self.redirect_url = None

        # Perform setup steps
        self._set_up_app(
            setting_overrides={
                "SURVEY_TYPE": "default",
                "EQ_SESSION_TIMEOUT_SECONDS": EQ_SESSION_TIMEOUT_SECONDS,
            }
        )

    def assert_supplementary_data_500_page(self):
        self.launchSupplementaryDataSurvey()
        self.assertStatusCode(500)
        self.assertInBody("Sorry, there is a problem with this service")

    def test_session_expired(self):
        self.get("/session-expired")
        self.assertInBody("Sorry, you need to sign in again")
        self.assertInBody(
            f'<p>If you are completing a business survey, you need to sign back in to <a href="{BUSINESS_URL}/sign-in/logout">your account</a>.</p>'
        )
        self.assertInBody(
            f'<p>If you started your survey using an access code, you need to <a href="{SOCIAL_URL}/{DEFAULT_LANGUAGE_CODE}/start/">re-enter your code</a>.</p>'
        )

    def test_session_jti_token_expired(self):
        self.launchSurveyV2(exp=time.time() - float(60))
        self.assertStatusUnauthorised()

    def test_head_request_on_session_expired(self):
        self.head("/session-expired")
        self.assertStatusOK()

    def test_head_request_on_session_signed_out(self):
        self.launchSurveyV2(schema_name="test_introduction")
        self.get("/signed-out")
        self.assertStatusOK()

    @freeze_time(TIME_TO_FREEZE)
    def test_get_session_expiry_doesnt_extend_session(self):
        self.launchSurveyV2()
        # Advance time by 20 mins...
        with freeze_time(TIME_TO_FREEZE + timedelta(minutes=20)):
            self.get("/session-expiry")
            response = self.getResponseData()
            parsed_json = json_loads(response)
            # ... check that the session expiry time is not affected by
            # the request, and is still 45mins from the start time
            expected_expires_at = (
                TIME_TO_FREEZE + timedelta(seconds=EQ_SESSION_TIMEOUT_SECONDS)
            ).isoformat()

            self.assertIn("expires_at", parsed_json)
            self.assertEqual(parsed_json["expires_at"], expected_expires_at)

    @freeze_time(TIME_TO_FREEZE)
    def test_patch_session_expiry_extends_session(self):
        self.launchSurveyV2()
        # Advance time by 20 mins...
        request_time = TIME_TO_FREEZE + timedelta(minutes=20)
        with freeze_time(request_time):
            self.patch(None, "/session-expiry")
            response = self.getResponseData()
            parsed_json = json_loads(response)
            # ... check that the session expiry time is reset by the request
            # and is now 45 mins from the request time
            expected_expires_at = (
                request_time + timedelta(seconds=EQ_SESSION_TIMEOUT_SECONDS)
            ).isoformat()

            self.assertIn("expires_at", parsed_json)
            self.assertEqual(parsed_json["expires_at"], expected_expires_at)

    @patch("app.routes.session.get_supplementary_data_v1")
    @patch("app.routes.session._validate_supplementary_data_lists")
    @patch(
        "app.questionnaire.questionnaire_store_updater.QuestionnaireStoreUpdaterBase.set_supplementary_data",
    )
    def test_supplementary_data_is_loaded_with_correct_identifier_when_new_sds_dataset_id_in_metadata(
        self,
        mock_set,
        mock_validate,
        mock_get,
    ):
        self.launchSupplementaryDataSurvey()
        self.assertStatusOK()
        mock_get.assert_called_once()
        mock_set.assert_called_once()
        mock_validate.assert_called_once()

        used_identifier = mock_get.call_args.kwargs["identifier"]
        ru_ref = PAYLOAD_V2_SUPPLEMENTARY_DATA["survey_metadata"]["data"]["ru_ref"]
        assert used_identifier == get_ru_ref_without_check_letter(ru_ref)
        assert used_identifier != ru_ref

    @patch("app.routes.session.get_supplementary_data_v1")
    @patch("app.routes.session._validate_supplementary_data_lists")
    @patch(
        "app.questionnaire.questionnaire_store_updater.QuestionnaireStoreUpdaterBase.set_supplementary_data",
    )
    def test_supplementary_data_is_reloaded_when_changed_sds_dataset_id_in_metadata(
        self,
        mock_set,
        mock_validate,
        mock_get,
    ):
        self.launchSupplementaryDataSurvey(response_id="1", sds_dataset_id="first")
        self.assertStatusOK()
        mock_set.assert_called_once()
        mock_get.assert_called_once()
        mock_validate.assert_called_once()
        self.launchSupplementaryDataSurvey(response_id="1", sds_dataset_id="second")
        self.assertStatusOK()
        self.assertEqual(mock_get.call_count, 2)
        self.assertEqual(mock_set.call_count, 2)
        self.assertEqual(mock_validate.call_count, 2)

    @patch("app.routes.session.get_supplementary_data_v1")
    @patch("app.routes.session._validate_supplementary_data_lists")
    @patch(
        "app.questionnaire.questionnaire_store_updater.QuestionnaireStoreUpdaterBase.set_supplementary_data",
    )
    def test_supplementary_data_is_not_reloaded_when_same_sds_dataset_id_in_metadata(
        self,
        mock_set,
        mock_validate,
        mock_get,
    ):
        self.launchSupplementaryDataSurvey(response_id="1", sds_dataset_id="same")
        self.assertStatusOK()
        mock_set.assert_called_once()
        mock_get.assert_called_once()
        mock_validate.assert_called_once()
        self.launchSupplementaryDataSurvey(response_id="1", sds_dataset_id="same")
        self.assertStatusOK()
        mock_get.assert_called_once()
        mock_set.assert_called_once()
        # validation should happen twice regardless
        self.assertEqual(mock_validate.call_count, 2)

    def test_supplementary_data_raises_500_error_when_sds_api_request_fails(self):
        with patch(
            "app.routes.session.get_supplementary_data_v1",
            side_effect=SupplementaryDataRequestFailed,
        ):
            self.assert_supplementary_data_500_page()

    @responses.activate
    def test_supplementary_data_raises_500_error_when_supplementary_data_invalid(self):
        responses.add(
            responses.GET,
            TEST_SDS_URL,
            json=mock_supplementary_data_payload_invalid_kid_in_data,
            status=200,
        )
        self.assert_supplementary_data_500_page()

    @responses.activate
    def test_supplementary_data_raises_500_error_when_supplementary_data_missing_data(
        self,
    ):
        responses.add(
            responses.GET,
            TEST_SDS_URL,
            json=mock_supplementary_data_payload_missing_data,
            status=200,
        )
        self.assert_supplementary_data_500_page()

    def test_supplementary_data_raises_500_error_when_missing_supplementary_data_key(
        self,
    ):
        self.key_store = KeyStore(
            {
                "keys": {
                    k: KEYS_DICT["keys"][k]
                    for k in (
                        EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_KID,
                        SR_USER_AUTHENTICATION_PUBLIC_KEY_KID,
                        EQ_SUBMISSION_SDX_PRIVATE_KEY,
                        EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY,
                    )
                }
            }
        )

        self.assert_supplementary_data_500_page()

    @patch("app.routes.session.get_supplementary_data_v1")
    @patch(
        "app.questionnaire.questionnaire_store_updater.QuestionnaireStoreUpdaterBase.set_supplementary_data",
    )
    def test_supplementary_data_raises_500_error_when_missing_required_lists(
        self, mock_set, mock_get
    ):
        """Tests that if the supplementary data being loaded does not cover all the dependent lists for the schema
        that a validation error is raised"""
        mock_get.return_value = {"data": {"items": {"products": []}}}
        self.launchSupplementaryDataSurvey(schema_name="test_supplementary_data")
        self.assertStatusCode(500)
        mock_set.assert_not_called()

    @patch("app.routes.session.get_supplementary_data_v1")
    @patch(
        "app.questionnaire.questionnaire_store_updater.QuestionnaireStoreUpdaterBase.set_supplementary_data",
    )
    def test_supplementary_data_is_loaded_when_all_required_lists_present(
        self, mock_set, mock_get
    ):
        mock_get.return_value = {"data": {"items": {"employees": [], "products": []}}}
        self.launchSupplementaryDataSurvey(schema_name="test_supplementary_data")
        self.assertStatusOK()
        mock_set.assert_called_once()

    @patch("app.routes.session.get_supplementary_data_v1")
    @patch(
        "app.routes.session._validate_supplementary_data_lists",
        side_effect=[
            None,
            ValidationError(
                "Supplementary data does not include the following lists required for the schema: missing"
            ),
        ],
    )
    @patch(
        "app.questionnaire.questionnaire_store_updater.QuestionnaireStoreUpdaterBase.set_supplementary_data",
    )
    def test_supplementary_data_raises_500_error_when_survey_becomes_invalid_for_same_dataset(
        self,
        mock_set,
        mock_validate,
        mock_get,
    ):
        """
        This checks the edge case in which a survey changes to have different lists, but the supplementary dataset id
        remains the same, so the supplementary data is not fetched again, but is no longer valid for the survey
        """
        self.launchSupplementaryDataSurvey(response_id="1", sds_dataset_id="same")
        self.assertStatusOK()
        mock_set.assert_called_once()
        mock_get.assert_called_once()
        mock_validate.assert_called_once()
        self.launchSupplementaryDataSurvey(response_id="1", sds_dataset_id="same")
        self.assertStatusCode(500)
        self.assertEqual(mock_validate.call_count, 2)
