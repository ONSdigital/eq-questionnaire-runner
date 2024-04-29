from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireInstructions(IntegrationTestCase):
    BASE_URL = "/questionnaire/"

    def test_interstitial_instruction(self):
        self.launchSurveyV2(schema_name="test_instructions")
        self.post(action="start_questionnaire")
        self.assertInBody("Just pause for a second")

    def test_question_instruction(self):
        self.launchSurveyV2(schema_name="test_instructions")
        self.post(action="start_questionnaire")
        self.post()
        self.assertInBody("Tell us about what you eat")
