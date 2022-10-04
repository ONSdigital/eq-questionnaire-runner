import time
from datetime import datetime, timedelta, timezone

from freezegun import freeze_time

from app.utilities.json import json_loads
from tests.integration.integration_test_case import IntegrationTestCase

TIME_TO_FREEZE = datetime(2020, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
EQ_SESSION_TIMEOUT_SECONDS = 45 * 60


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

    def test_session_expired(self):
        self.get("/session-expired")
        self.assertInBody("Sorry, you need to sign in again")
        self.assertInBody(
            '<p>If you are completing a business survey, you need to sign back in to <a href="https://surveys.ons.gov.uk/sign-in/logout">your account</a>.</p>'
        )
        self.assertInBody(
            '<p>If you started your survey using an access code, you need to <a href="https://start.surveys.ons.gov.uk/sign-in/logout">re-enter your code</a>.'
            "</p>"
        )

    def test_session_jti_token_expired(self):
        self.launchSurvey(exp=time.time() - float(60))
        self.assertStatusUnauthorised()

    def test_head_request_on_session_expired(self):
        self.head("/session-expired")
        self.assertStatusOK()

    def test_head_request_on_session_signed_out(self):
        self.head("/signed-out")
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
