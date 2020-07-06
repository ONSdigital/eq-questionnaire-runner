from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireListCollector(IntegrationTestCase):
    def add_person(self, first_name, last_name):
        self.post({"anyone-else": "Yes"})

        self.post({"first-name": first_name, "last-name": last_name})

    def get_link(self, rowIndex, text):
        selector = f"[data-qa='{text}-item-link-{rowIndex}']"
        selected = self.getHtmlSoup().select(selector)

        filtered = [html for html in selected if text in html.get_text()]

        return filtered[0].get("href")

    def get_previous_link(self):
        selector = "#top-previous"
        selected = self.getHtmlSoup().select(selector)
        return selected[0].get("href")

    def test_invalid_list_collector(self):
        self.launchSurvey("test_list_collector")

        self.get("/questionnaire/invalid/some-list-id/edit-person")

        self.assertInUrl("/questionnaire/list-collector")

    def test_invalid_list_item_id_on_add_block(self):
        self.launchSurvey("test_list_collector")

        self.get("/questionnaire/people/123/add-person")

        self.assertInUrl("/questionnaire/list-collector")

    def test_invalid_block(self):
        self.launchSurvey("test_list_collector")

        self.get("/questionnaire/bad-block")

        self.assertInUrl("list-collector")

    def test_invalid_list_item_id(self):
        self.launchSurvey("test_list_collector")

        self.get("/questionnaire/people/123/edit-person")

        self.assertInUrl("list-collector")

    def test_happy_path(self):
        self.launchSurvey("test_list_collector")

        self.assertInBody("Does anyone else live here?")

        self.post({"anyone-else": "Yes"})

        self.add_person("Marie Claire", "Doe")

        self.assertInSelector("Marie Claire Doe", "[data-qa='list-item-label-0']")

        self.add_person("John", "Doe")

        self.assertInSelector("John Doe", "[data-qa='list-item-label-1']")

        self.add_person("A", "Mistake")

        self.assertInSelector("A Mistake", "[data-qa='list-item-label-2']")

        self.add_person("Johnny", "Doe")

        self.assertInSelector("Johnny Doe", "[data-qa='list-item-label-3']")

        # Make another mistake

        mistake_change_link = self.get_link("2", "Change")

        self.get(mistake_change_link)

        self.post({"first-name": "Another", "last-name": "Mistake"})

        self.assertInSelector("Another Mistake", "[data-qa='list-item-label-2']")

        # Get rid of the mistake

        mistake_remove_link = self.get_link("2", "Remove")

        self.get(mistake_remove_link)

        self.assertInBody("Are you sure you want to remove this person?")

        # Cancel

        self.post({"remove-confirmation": "No"})

        self.assertEqualUrl("/questionnaire/list-collector/")

        # Remove again

        self.get(mistake_remove_link)

        self.post({"remove-confirmation": "Yes"})

        # Make sure Johnny has moved up the list
        self.assertInSelector("Johnny Doe", "[data-qa='list-item-label-2']")

        # Test the previous links
        john_change_link = self.get_link("1", "Change")
        john_remove_link = self.get_link("1", "Remove")

        self.get(john_change_link)

        self.get(self.get_previous_link())

        self.assertEqualUrl("/questionnaire/list-collector/")

        self.get(john_remove_link)

        self.assertInUrl("remove")

        self.get(self.get_previous_link())

        self.assertEqualUrl("/questionnaire/list-collector/")

    def test_list_collector_submission(self):
        self.launchSurvey("test_list_collector")

        self.post(action="start_questionnaire")

        self.assertInBody("Does anyone else live here?")

        self.post({"anyone-else": "Yes"})

        self.add_person("Marie Claire", "Doe")

        self.assertInSelector("Marie Claire Doe", "[data-qa='list-item-label-0']")

        self.add_person("John", "Doe")

        self.assertInSelector("John Doe", "[data-qa='list-item-label-1']")

        self.post({"anyone-else": "No"})

        self.post()

        self.post({"another-anyone-else": "No"})

        self.assertInBody("List Collector Summary")

        self.assertInBody("Household members")

        john_remove_link = self.get_link("1", "Remove")

        mary_remove_link = self.get_link("0", "Remove")

        self.get(john_remove_link)

        self.post({"remove-confirmation": "Yes"})

        self.get(mary_remove_link)

        self.post({"remove-confirmation": "Yes"})

        self.assertInBody("There are no householders")

        self.post()

        self.post()

        self.assertInUrl("thank-you")

    def test_optional_list_collector_submission(self):
        self.launchSurvey("test_list_collector")

        self.post(action="start_questionnaire")

        self.assertInBody("Does anyone else live here?")

        self.post({"anyone-else": "No"})

        self.post()

        self.post({"another-anyone-else": "No"})

        self.assertInBody("List Collector Summary")

        self.post()

        self.assertInUrl("confirmation")

    def test_list_summary_on_question(self):
        self.launchSurvey("test_list_summary_on_question")

        self.post(action="start_questionnaire")

        self.post({"anyone-else": "Yes"})

        self.add_person("Marie Claire", "Doe")

        self.post({"anyone-else": "No"})

        self.post()

        self.post({"another-anyone-else": "No"})

        self.assertInBody("Are any of these people related to one another?")

        self.assertInBody("Marie Claire Doe")

        self.post({"radio-mandatory-answer": "No, all household members are unrelated"})

        self.assertInUrl("/sections/section/")

        self.assertInBody("Marie Claire Doe")

    def test_questionnaire_summary_with_custom_section_summary(self):
        self.launchSurvey("test_list_summary_on_question")

        self.post(action="start_questionnaire")

        self.post({"anyone-else": "Yes"})

        self.add_person("Marie Claire", "Doe")

        self.post({"anyone-else": "No"})

        self.post()

        self.post({"another-anyone-else": "No"})

        self.post({"radio-mandatory-answer": "No, all household members are unrelated"})

        self.post()

        self.assertInBody("Check your answers and submit")

        self.assertNotInBody("No, all household members are unrelated")

    def test_cancel_text_displayed_on_add_block_if_exists(self):
        self.launchSurvey("test_list_collector")

        self.post(action="start_questionnaire")

        self.post({"anyone-else": "Yes"})

        self.assertInBody("Don’t need to add anyone else?")

    def test_cancel_text_displayed_on_edit_block_if_exists(self):
        self.launchSurvey("test_list_collector")

        self.post(action="start_questionnaire")

        self.post({"anyone-else": "Yes"})

        self.add_person("Someone", "Else")

        change_link = self.get_link("0", "Change")

        self.get(change_link)

        self.assertInBody("Don’t need to change anything?")

    def test_warning_text_displayed_on_remove_block_if_exists(self):
        self.launchSurvey("test_list_collector")
        self.post(action="start_questionnaire")
        self.post({"anyone-else": "Yes"})
        self.add_person("Someone", "Else")
        remove_link = self.get_link("0", "Remove")
        self.get(remove_link)
        self.assertIsNotNone(
            self.getHtmlSoup().select("#question-warning-remove-question")
        )
        self.assertInBody("All of the information about this person will be deleted")
