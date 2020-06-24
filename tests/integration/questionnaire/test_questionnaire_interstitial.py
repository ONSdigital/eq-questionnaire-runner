from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireInterstitial(IntegrationTestCase):

    BASE_URL = "/questionnaire/"

    def test_interstitial_page_button_text_is_continue(self):
        self.launchSurvey("test_interstitial_page")
        self.post(action="start_questionnaire")
        self.post({"favourite-breakfast": "Cereal"})
        self.assertInBody("Continue")

    def test_interstitial_can_continue_and_submit(self):
        self.launchSurvey("test_interstitial_page")
        self.post(action="start_questionnaire")
        self.post({"favourite-breakfast": "Cereal"})
        self.post()
        self.assertInUrl("lunch-block")
        self.post({"favourite-lunch": "Pizza"})
        self.assertInUrl("confirmation")
        self.post()
        self.assertInBody("Submission successful")

    def test_interstitial_instruction(self):
        self.launchSurvey("test_interstitial_instruction")
        self.post(action="start_questionnaire")
        self.assertInBody("Just pause for a second")
