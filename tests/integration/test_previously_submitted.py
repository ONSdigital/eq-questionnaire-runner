from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.questionnaire import THANK_YOU_URL_PATH


class TestPreviouslySubmitted(IntegrationTestCase):
    def test_previously_submitted(self):
        # Given I complete the questionnaire and submit
        self.launchSurveyV2(schema_name="test_textfield")
        self.post()
        self.post()
        self.assertInUrl(THANK_YOU_URL_PATH)

        # When I try to return to a page in the questionnaire
        self.get("/questionnaire/submit/")

        # Then I should receive a 401 unauthorised code and be redirected to the submission complete page
        self.assertStatusUnauthorised()
        self.assertEqualPageTitle("Submission Complete - Other input fields")
        self.assertInBody("This page is no longer available")
        self.assertInBody("Your survey has been submitted")
        self.assertInBody(f'<a href="{THANK_YOU_URL_PATH}">Return to previous page</a>')
