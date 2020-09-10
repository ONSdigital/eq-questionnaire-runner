from tests.integration.integration_test_case import IntegrationTestCase


class QuestionnaireTestCase(IntegrationTestCase):
    def add_person(self, first_name: str, last_name: str):
        self.post({"anyone-else": "Yes"})
        self.post({"first-name": first_name, "last-name": last_name})
