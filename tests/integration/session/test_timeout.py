import time

from app import settings
from tests.integration.integration_test_case import IntegrationTestCase


class TestTimeout(IntegrationTestCase):
    def setUp(self):
        settings.EQ_SESSION_TIMEOUT_SECONDS = 4
        settings.SURVEY_TYPE = "default"
        super().setUp()

    def tearDown(self):
        settings.EQ_SESSION_TIMEOUT_SECONDS = 45 * 60
        super().tearDown()

    def test_timeout_continue_valid_session_returns_200(self):
        self.launchSurveyV2(schema_name="test_timeout")
        self.get(self.last_url)
        self.assertStatusOK()

    def test_when_session_times_out_server_side_401_is_returned(self):
        self.launchSurveyV2(schema_name="test_timeout")
        time.sleep(5)
        self.get(self.last_url)
        self.assertStatusUnauthorised()
        self.assertInBody("Sorry, you need to sign in again")

    def test_alternate_401_page_is_displayed_when_no_cookie(self):
        self.get("/session")
        self.assertStatusUnauthorised()
        self.assertInBody("followed a link to a page you are not signed in to")
        self.assertEqualPageTitle("Page is not available - ONS Surveys")

    def test_schema_defined_timeout_cant_be_higher_than_server(self):
        self.launchSurveyV2(schema_name="test_timeout")
        time.sleep(4)
        self.get(self.last_url)
        self.assertStatusUnauthorised()
        self.assertInBody(
            "been inactive for 45 minutes and your session has timed out to protect your information"
        )
        self.assertEqualPageTitle("Page is not available - Timeout test")

    def test_submission_complete_timeout(self):
        self.launchSurveyV2(schema_name="test_timeout")
        self.post()
        self.post()
        time.sleep(4)
        self.get(self.last_url)
        self.assertStatusUnauthorised()
        self.assertInBody("Sorry, you need to sign in again")
        self.assertEqualPageTitle("Page is not available - Timeout test")
