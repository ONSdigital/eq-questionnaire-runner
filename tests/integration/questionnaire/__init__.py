from tests.integration.integration_test_case import IntegrationTestCase


class URL:
    HUB = "/questionnaire/"
    FINAL_SUMMARY = "/questionnaire/summary/"
    FINAL_CONFIRMATION = "/questionnaire/confirmation/"
    THANK_YOU = "/submitted/thank-you/"


class QuestionnaireTestCase(IntegrationTestCase):
    def add_person(self, first_name: str, last_name: str):
        self.post({"anyone-else": "Yes"})
        self.post({"first-name": first_name, "last-name": last_name})
