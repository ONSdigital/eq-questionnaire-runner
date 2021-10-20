import time

from tests.integration.integration_test_case import IntegrationTestCase


class TestSession(IntegrationTestCase):
    def setUp(self):
        # Cache for requests
        self.last_url = None
        self.last_response = None
        self.last_csrf_token = None
        self.redirect_url = None

        # Perform setup steps
        self._set_up_app(setting_overrides={"SURVEY_TYPE": "default"})

    def test_session_expired(self):
        self.get("/session-expired")
        self.assertInBody("Sorry, you need to sign in again")

    def test_session_signed_out(self):
        self.launchSurvey(account_service_log_out_url="https://localhost/logout")
        self.assertInBody("Save and sign out")

        self.get("/sign-out")

        self.assertInUrl("/logout")

    def test_session_signed_out_no_account_service_log_out_url(self):
        self.launchSurvey()
        self.assertInBody("Save and sign out")

        self.get("/sign-out")

        self.assertInUrl("/signed-out")

    def test_session_signed_out_no_cookie_session_default_config(self):
        self.launchSurvey()
        self.assertInBody("Save and sign out")

        self.deleteCookie()
        self.get("/sign-out", follow_redirects=False)

        self.assertInRedirect("surveys.ons.gov.uk")

    def test_session_jti_token_expired(self):
        self.launchSurvey(exp=time.time() - float(60))
        self.assertStatusUnauthorised()

    def test_head_request_on_session_expired(self):
        self.head("/session-expired")
        self.assertStatusOK()

    def test_head_request_on_session_signed_out(self):
        self.head("/signed-out")
        self.assertStatusOK()


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
