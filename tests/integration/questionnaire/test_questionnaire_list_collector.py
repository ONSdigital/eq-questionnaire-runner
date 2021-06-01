from . import SUBMIT_URL_PATH, QuestionnaireTestCase


class TestQuestionnaireListCollector(QuestionnaireTestCase):
    def get_add_someone_link(self):
        selector = f"[data-qa='add-item-link']"
        selected = self.getHtmlSoup().select(selector)
        return selected[0].get("href")

    def test_invalid_add_block_url(self):
        self.launchSurvey("test_list_collector")

        self.get("/questionnaire/people/123/add-person")

        self.assertStatusNotFound()

    def test_invalid_list_name(self):
        self.launchSurvey("test_list_collector")

        self.get("/questionnaire/invalid-list-name/add-person/")

        self.assertStatusNotFound()

    def test_invalid_list_item_id_for_edit_block(self):
        self.launchSurvey("test_list_collector")

        self.get("/questionnaire/people/123/edit-person")

        self.assertStatusNotFound()

    def test_happy_path(self):
        self.launchSurvey("test_list_collector")

        self.assertInBody("Does anyone else live here?")

        self.post({"anyone-else": "Yes"})

        self.add_person("Marie Claire", "Doe")

        self.assertInSelector("Marie Claire Doe", "[data-qa='list-item-1-label']")

        self.add_person("John", "Doe")

        self.assertInSelector("John Doe", "[data-qa='list-item-2-label']")

        self.add_person("A", "Mistake")

        self.assertInSelector("A Mistake", "[data-qa='list-item-3-label']")

        self.add_person("Johnny", "Doe")

        self.assertInSelector("Johnny Doe", "[data-qa='list-item-4-label']")

        # Make another mistake

        mistake_change_link = self.get_link("change", 3)

        self.get(mistake_change_link)

        self.post({"first-name": "Another", "last-name": "Mistake"})

        self.assertInSelector("Another Mistake", "[data-qa='list-item-3-label']")

        # Get rid of the mistake

        mistake_remove_link = self.get_link("remove", 3)

        self.get(mistake_remove_link)

        self.assertInBody("Are you sure you want to remove this person?")

        # Cancel

        self.post({"remove-confirmation": "No"})

        self.assertEqualUrl("/questionnaire/list-collector/")

        # Remove again

        self.get(mistake_remove_link)

        self.post({"remove-confirmation": "Yes"})

        # Make sure Johnny has moved up the list
        self.assertInSelector("Johnny Doe", "[data-qa='list-item-3-label']")

        # Test the previous links
        john_change_link = self.get_link("change", 2)
        john_remove_link = self.get_link("remove", 2)

        self.get(john_change_link)

        self.previous()

        self.assertEqualUrl("/questionnaire/list-collector/")

        self.get(john_remove_link)

        self.assertInUrl("remove")

        self.previous()

        self.assertEqualUrl("/questionnaire/list-collector/")

    def test_list_collector_submission(self):
        self.launchSurvey("test_list_collector")

        self.post(action="start_questionnaire")

        self.assertInBody("Does anyone else live here?")

        self.post({"anyone-else": "Yes"})

        self.add_person("Marie Claire", "Doe")

        self.assertInSelector("Marie Claire Doe", "[data-qa='list-item-1-label']")

        self.add_person("John", "Doe")

        self.assertInSelector("John Doe", "[data-qa='list-item-2-label']")

        self.post({"anyone-else": "No"})

        self.post()

        self.post({"another-anyone-else": "No"})

        self.assertInBody("List Collector Summary")

        self.assertInBody("Household members")

        john_remove_link = self.get_link("remove", 2)

        mary_remove_link = self.get_link("remove", 1)

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

        self.assertInUrl(SUBMIT_URL_PATH)

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

        change_link = self.get_link("change", 1)

        self.get(change_link)

        self.assertInBody("Don’t need to change anything?")

    def test_warning_text_displayed_on_remove_block_if_exists(self):
        self.launchSurvey("test_list_collector")

        self.post(action="start_questionnaire")

        self.post({"anyone-else": "Yes"})

        self.add_person("Someone", "Else")

        remove_link = self.get_link("remove", 1)

        self.get(remove_link)

        self.assertIsNotNone(
            self.getHtmlSoup().select("#question-warning-remove-question")
        )

        self.assertInBody("All of the information about this person will be deleted")

    def test_list_collector_return_to_when_section_summary_cant_be_displayed(self):
        # Given I have completed a section and returned to a list_collector from the section summary
        self.launchSurvey("test_relationships", roles=["dumper"])

        self.add_person("Marie", "Doe")

        self.post({"anyone-else": "No"})

        self.assertInUrl("/sections/section/")

        add_someone_link = self.get_add_someone_link()

        self.get(add_someone_link)

        # When I update the list collector, which changes the section status to in-progress
        self.add_person("John", "Doe")

        # Then my next location is the parent list collector without last updated guidance being shown
        self.assertInBody("Does anyone else live at 1 Pleasant Lane?")
        self.assertNotInBody("This is the last viewed question in this section")

    def test_adding_person_using_second_list_collector_when_no_people(
        self,
    ):
        self.launchSurvey("test_list_collector_two_list_collectors")

        self.assertInBody("Does anyone live at your address?")

        self.post({"anyone-usually-live-at-answer": "No"})

        self.assertInBody("Does anyone else live here?")

        self.post({"anyone-else": "No"})

        self.assertInBody("Does anyone else live at your address?")

        self.post({"another-anyone-usually-live-at-answer": "Yes"})

        self.assertInBody("What is the name of the person?")

        self.post({"first-name": "Marie", "last-name": "Day"})

        self.post({"another-anyone-else": "No"})

        self.assertInUrl("/questionnaire/sections/section/")

        first_person_change_link = self.get_link("change", 1)

        self.get(first_person_change_link)

        self.assertInBody("Change details for Marie Day")

        self.post({"first-name": "James", "last-name": "May"})

        self.assertInUrl("/questionnaire/sections/section/")

        first_person_remove_link = self.get_link("remove", 1)

        self.get(first_person_remove_link)

        self.assertInBody("Are you sure you want to remove this person?")
