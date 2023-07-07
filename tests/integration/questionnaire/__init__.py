from tests.integration.integration_test_case import IntegrationTestCase

HUB_URL_PATH = "/questionnaire/"
THANK_YOU_URL_PATH = "/submitted/thank-you/"
SUBMIT_URL_PATH = "/questionnaire/submit/"


class QuestionnaireTestCase(IntegrationTestCase):
    def add_person(self, first_name: str, last_name: str):
        self.post({"anyone-else": "Yes"})
        self.post({"first-name": first_name, "last-name": last_name})
        number_of_people = self.number_of_people()
        return self.get_list_item_ids()[number_of_people - 1]

    def number_of_people(self):
        return len(self.get_list_item_ids())

    def get_list_item_ids(self):
        return [
            list_item.attrs["data-list-item-id"]
            for list_item in self.getHtmlSoup().find_all(
                attrs={"data-list-item-id": True}
            )
        ]

    def get_link(self, action, position):
        selector = f"[data-qa='list-item-{action}-{position}-link']"
        selected = self.getHtmlSoup().select(selector)
        return selected[0].get("href")
