from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireRadioVoluntary(IntegrationTestCase):

    BASE_URL = "/questionnaire/"

    def test_radio_voluntary(self):
        self.launchSurvey("test_radio_voluntary")
        self.post({"radio-voluntary-true-answer": "Coffee"})
        self.previous()
        self.post(action="clear_radios")
        self.post()
        self.assertNotInBody("Coffee")
