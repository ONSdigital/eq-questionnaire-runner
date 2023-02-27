from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireInstructions(IntegrationTestCase):
    BASE_URL = "/questionnaire/"

    def test_preview_not_enabled_results_in_500(self):
        self.launchSurvey("test_checkbox")
        self.post(action="start_questionnaire")
        self.get(f"{self.BASE_URL}/preview/")
        self.assertStatusCode(500)
