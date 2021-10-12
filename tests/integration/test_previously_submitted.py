from mock import patch

from tests.integration.integration_test_case import IntegrationTestCase


class TestPreviouslySubmitted(IntegrationTestCase):
    def test_previously_submitted(self):
        # Given
        self.launchSurvey("test_view_submitted_response")
        self.post()
        self.post()
        self.post()

        self.get("/questionnaire/submit/")
        self.assertStatusUnauthorised()
        self.assertEqualPageTitle("Submission Complete - Test View Submitted Response")
        self.assertInBody("This page is no longer available")
        self.assertInBody("Your survey has been submitted")
        self.assertInBody('<a href="/submitted/thank-you/">Return to previous page</a>')
