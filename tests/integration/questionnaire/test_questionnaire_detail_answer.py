from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireDetailAnswer(IntegrationTestCase):
    BASE_URL = "/questionnaire/"

    def test_detail_answer(self):
        self.launchSurveyV2(schema_name="test_checkbox_detail_answer_multiple")
        self.post(
            {
                "mandatory-checkbox-answer": ["Ham", "Pineapple", "Your choice"],
                "your-choice-answer-mandatory": "Chicken",
            }
        )
        self.assertInBody("Ham")
        self.assertInBody("Pineapple")
        self.assertInBody("Your choice")
        self.assertInBody("Chicken")
