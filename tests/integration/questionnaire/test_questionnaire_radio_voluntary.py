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


class TestQuestionnaireRepeatingSectionRadioVoluntary(IntegrationTestCase):

    BASE_URL = "/questionnaire/"

    def test_radio_voluntary_on_repeating_section(self):
        self.launchSurvey("test_repeating_section_with_radio_voluntary")
        self.post()
        self.post({"you-live-here": "Yes"})
        self.post({"first-name": "James", "last-name": "May"})
        self.post({"anyone-else": "No"})
        self.post()
        self.post({"radio-voluntary-true-answer": "Coffee"})
        self.previous()
        self.post(action="clear_radios")
        self.post()
        self.post({"radio-voluntary-false-answer": "Hamburger"})
        self.assertInUrl("personal-details-section")
        self.assertNotInBody("Coffee")
