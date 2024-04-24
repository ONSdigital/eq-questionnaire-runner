from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireRadioVoluntary(IntegrationTestCase):
    BASE_URL = "/questionnaire/"

    def test_radio_voluntary(self):
        self.launchSurveyV2(schema_name="test_radio_voluntary")
        self.post({"radio-voluntary-true-answer": "Coffee"})
        self.previous()
        self.post(action="clear_radios")
        self.post()
        self.assertNotInBody("Coffee")


class TestQuestionnaireRepeatingSectionRadioVoluntary(IntegrationTestCase):
    BASE_URL = "/questionnaire/"

    def test_clear_radios(self):
        self.launchSurveyV2(schema_name="test_radio_voluntary_with_repeating_sections")
        self.post()
        self.post({"anyone-lives-here": "Yes"})
        self.post({"first-name": "James", "last-name": "May"})
        self.post({"anyone-lives-here": "No"})
        self.post()
        self.post({"radio-voluntary-answer": "Coffee"})

        self.assertInUrl("personal-details-section")
        self.assertInBody("Coffee")

        self.previous()
        self.post(action="clear_radios")
        self.post()

        self.assertInUrl("personal-details-section")
        self.assertNotInBody("Coffee")
