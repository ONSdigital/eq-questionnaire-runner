from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.questionnaire import SUBMIT_URL_PATH, THANK_YOU_URL_PATH


class TestQuestionnaireInterstitial(IntegrationTestCase):
    BASE_URL = "/questionnaire/"

    def test_interstitial_page_button_text_is_continue(self):
        self.launchSurveyV2(schema_name="test_interstitial_page")
        self.post(action="start_questionnaire")
        self.post({"favourite-breakfast": "Cereal"})
        self.assertInBody("Continue")

    def test_interstitial_can_continue_and_submit(self):
        self.launchSurveyV2(schema_name="test_interstitial_page")
        self.post(action="start_questionnaire")
        self.post({"favourite-breakfast": "Cereal"})
        self.post()
        self.assertInUrl("lunch-block")
        self.post({"favourite-lunch": "Pizza"})
        self.assertInUrl(SUBMIT_URL_PATH)
        self.post()
        self.assertInUrl(THANK_YOU_URL_PATH)

    def test_interstitial_definition(self):
        self.launchSurveyV2(schema_name="test_interstitial_definition")
        self.assertInBody("Successfully")
        self.assertInBody("In a way that accomplishes a desired aim or result")

    def test_interstitial_content_variant_definition(self):
        self.launchSurveyV2(schema_name="test_interstitial_definition")
        self.post()
        self.post({"content-variant-definition-answer": "Answer"})

        self.assertInBody("Answer")
        self.assertInBody("A spoken or written reply or response to a question")
