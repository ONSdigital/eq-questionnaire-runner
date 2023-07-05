import time
from datetime import datetime, timedelta, timezone

import responses
from freezegun import freeze_time
from mock.mock import patch
from sdc.crypto.key_store import KeyStore

from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.services.supplementary_data import SupplementaryDataRequestFailed
from app.settings import ACCOUNT_SERVICE_BASE_URL, ACCOUNT_SERVICE_BASE_URL_SOCIAL
from app.utilities.json import json_loads
from tests.app.services.test_request_supplementary_data import TEST_SDS_URL
from tests.integration.integration_test_case import IntegrationTestCase

TIME_TO_FREEZE = datetime(2020, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
EQ_SESSION_TIMEOUT_SECONDS = 45 * 60
BUSINESS_URL = ACCOUNT_SERVICE_BASE_URL
SOCIAL_URL = ACCOUNT_SERVICE_BASE_URL_SOCIAL
TEST_SDS_URL = "http://localhost:5003/v1/unit_data"

mock_supplementary_data_payload_missing_encryption_key_id_and_data = {
    "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
    "survey_id": "123",
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
        self.launchSurvey(exp=time.time() - float(60))
        self.assertStatusUnauthorised()

    def test_head_request_on_session_expired(self):
        self.head("/session-expired")
        self.assertStatusOK()

    def test_head_request_on_session_signed_out(self):
        self.launchSurvey("test_introduction")
        self.get("/signed-out")
        self.assertStatusOK()

    @freeze_time(TIME_TO_FREEZE)
    def test_get_session_expiry_doesnt_extend_session(self):
        self.launchSurvey()
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
        self.launchSurvey()
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

    @patch("app.routes.session.get_supplementary_data")
    @patch(
        "app.data_models.questionnaire_store.QuestionnaireStore.set_supplementary_data"
    )
    def test_supplementary_data_is_loaded_when_new_sds_dataset_id_in_metadata(
        self,
        mock_set,
        mock_get,
    ):
        self.launchSupplementaryDataSurvey()
        self.assertStatusOK()
        mock_get.assert_called_once()
        mock_set.assert_called_once()

    @patch("app.routes.session.get_supplementary_data")
    @patch(
        "app.data_models.questionnaire_store.QuestionnaireStore.set_supplementary_data"
    )
    def test_supplementary_data_is_reloaded_when_changed_sds_dataset_id_in_metadata(
        self,
        mock_set,
        mock_get,
    ):
        self.launchSupplementaryDataSurvey(response_id="1", sds_dataset_id="first")
        self.assertStatusOK()
        mock_set.assert_called_once()
        mock_get.assert_called_once()
        self.launchSupplementaryDataSurvey(response_id="1", sds_dataset_id="second")
        self.assertStatusOK()
        self.assertEqual(mock_get.call_count, 2)
        self.assertEqual(mock_set.call_count, 2)

    @patch("app.routes.session.get_supplementary_data")
    @patch(
        "app.data_models.questionnaire_store.QuestionnaireStore.set_supplementary_data"
    )
    def test_supplementary_data_is_not_reloaded_when_same_sds_dataset_id_in_metadata(
        self,
        mock_set,
        mock_get,
    ):
        self.launchSupplementaryDataSurvey(response_id="1", sds_dataset_id="same")
        self.assertStatusOK()
        mock_set.assert_called_once()
        mock_get.assert_called_once()
        self.launchSupplementaryDataSurvey(response_id="1", sds_dataset_id="same")
        self.assertStatusOK()
        mock_get.assert_called_once()
        mock_set.assert_called_once()

    def test_supplementary_data_raises_500_error_on_exception(self):
        with patch(
            "app.routes.session.get_supplementary_data",
            side_effect=SupplementaryDataRequestFailed,
        ):
            self.assert_supplementary_data_500_page()

    @responses.activate
    def test_supplementary_data_raises_500_error_when_supplementary_data_invalid(self):
        responses.add(
            responses.GET,
            TEST_SDS_URL,
            json=mock_supplementary_data_payload_missing_encryption_key_id_and_data,
            status=200,
        )
        self.assert_supplementary_data_500_page()

    def test_supplementary_data_raises_500_error_when_missing_supplementary_data_key(
        self,
    ):
        with patch(
            "app.services.supplementary_data.get_key_store",
            return_value=KeyStore({"keys": {}}),
        ):
            self.assert_supplementary_data_500_page()


class TestCensusSession(IntegrationTestCase):
    def setUp(self):
        # Cache for requests
        self.last_url = None
        self.last_response = None
        self.last_csrf_token = None
        self.redirect_url = None

        # Perform setup steps
        self._set_up_app(setting_overrides={"SURVEY_TYPE": "census"})

    def test_session_signed_out_no_cookie_session_census_config(self):
        self.launchSurvey(schema_name="test_individual_response")
        self.assertInBody("Save and sign out")

        self.deleteCookie()
        self.get("/sign-out", follow_redirects=False)

        self.assertInRedirect("census.gov.uk")
