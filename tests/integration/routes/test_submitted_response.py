import time

from app import settings
from tests.integration.integration_test_case import IntegrationTestCase


class TestSubmissionResponse(IntegrationTestCase):
    def _launch_and_complete_questionnaire(self):
        self.launchSurvey("test_view_submitted_response")
        self.post({"name-answer": "John Smith"})
        self.post()

    def test_enabled(self):
        # Given I launch and complete a questionnaire that has view-submitted-response enabled
        self._launch_and_complete_questionnaire()

        # When I try to get the view-response page
        self.get("/submitted/view-response")

        # Then the page is displayed correctly
        self.assertEqualPageTitle("Submitted Response - Test View Submitted Response")
        self.assertInBody(
            "Your answers were submitted for <span>Integration Testing</span>"
        )
        self.assertInBody("Submitted on:")
        self.assertInBody("Submission reference:")
        self.assertInBody("What is your name?")
        self.assertInBody("John Smith")

    def test_not_enabled(self):
        # Given I launch and complete a questionnaire that does not have view-submitted-response enabled
        self.launchSurvey("test_confirmation_email")
        self.post()
        self.post()

        # When I try to get the view-response page
        self.get("/submitted/view-response")

        # Then I get shown a 404 error
        self.assertStatusNotFound()

    def test_expired(self):
        settings.SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS = 1
        super().setUp()
        # Given I launch and complete a questionnaire that has view-submitted-response enabled but has expired
        self._launch_and_complete_questionnaire()
        time.sleep(2)

        # When I try to get the view-response page
        self.get("/submitted/view-response")

        # Then I get shown a 404 error
        self.assertStatusNotFound()
