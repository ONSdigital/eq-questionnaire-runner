import random
import re
import string

from tests.integration.questionnaire import QuestionnaireTestCase


class TestQuestionnaireListCollector(QuestionnaireTestCase):
    def test_invalid_list_on_primary_person_collector(self):
        self.launchSurveyV2(schema_name="test_list_collector_primary_person")

        self.get("/questionnaire/invalid/123423/add-or-edit-person/")

        self.assertStatusNotFound()

    def test_invalid_list_item_id_for_primary_person_add_block(self):
        self.launchSurveyV2(schema_name="test_list_collector_primary_person")
        self.post({"you-live-here": "Yes"})

        self.assertInUrl("add-or-edit-primary-person/")

        self.get("/questionnaire/people/abcdef/add-or-edit-primary-person/")

        self.assertStatusNotFound()

    def test_non_primary_person_list_item_id_for_primary_person_add_block(self):
        self.launchSurveyV2(schema_name="test_list_collector_primary_person")

        # Add a non-primary person
        self.post({"you-live-here": "No"})
        self.post({"anyone-usually-live-at-answer": "Yes"})
        self.post({"first-name": "John", "last-name": "Doe"})

        first_person_change_link = self.get_link("change", 1)

        self.get(first_person_change_link)

        # Get the non-primary list item id
        non_primary_person_list_item_id = re.search(
            r"people\/([a-zA-Z]*)\/edit-person", self.last_url
        ).group(1)

        # Add primary person
        self.get("/questionnaire/primary-person-list-collector/")
        self.post({"you-live-here": "Yes"})

        # Use the non-primary person list item id in the URL
        self.get(
            f"/questionnaire/people/{non_primary_person_list_item_id}/add-or-edit-primary-person/"
        )

        self.assertStatusNotFound()

    def test_adding_then_removing_primary_person(self):
        self.launchSurveyV2(schema_name="test_list_collector_primary_person")

        self.post({"you-live-here": "Yes"})

        self.assertInBody("What is your name")

        self.post({"first-name": "Marie", "last-name": "Day"})

        self.assertInBody("Does anyone else live here?")

        self.assertInBody("Marie Day")

        self.post({"anyone-else": "Yes"})

        self.assertInBody("What is the name of the person")

        self.post({"first-name": "James", "last-name": "May"})

        self.assertInBody("James May")

        self.get("/questionnaire/primary-person-list-collector")

        self.post({"you-live-here": "No"})

        self.assertInUrl("anyone-usually-live-at")

        self.post({"anyone-usually-live-at-answer": "Yes"})

        self.assertInBody("James May")

    def test_cannot_remove_primary_person_from_list_collector(self):
        self.launchSurveyV2(schema_name="test_list_collector_primary_person")

        self.post({"you-live-here": "Yes"})

        primary_person_list_item_id = re.search(
            r"people\/([a-zA-Z]*)\/add-or-edit-primary-person", self.last_url
        ).group(1)

        self.post({"first-name": "Marie", "last-name": "Day"})

        self.post({"anyone-else": "Yes"})

        self.post({"first-name": "James", "last-name": "May"})

        self.get(f"questionnaire/people/{primary_person_list_item_id}/remove-person/")

        self.assertStatusNotFound()

        self.get("questionnaire/list-collector/")

        self.assertInBody("James May")
        self.assertInBody("Marie Day")

    def test_changing_answer_from_no_to_yes_on_primary_person_list_collector_resumes_in_right_location(
        self,
    ):
        response_id = random.choices(string.digits, k=16)

        # Given I initially answer 'No' to the primary person list collector
        self.launchSurveyV2(
            schema_name="test_list_collector_primary_person", reponse_id=response_id
        )
        self.post({"you-live-here": "No"})

        # When I change my answer to 'Yes' and sign out
        self.get("questionnaire/primary-person-list-collector/")
        self.post({"you-live-here": "Yes"})
        self.signOut()

        # Then on resuming, I am returned to the primary-person-list-collector
        self.launchSurveyV2(
            schema_name="test_list_collector_primary_person", reponse_id=response_id
        )
        self.assertInUrl("/questionnaire/primary-person-list-collector/")

    def test_section_summary_with_primary_no_driving_question_on_path(
        self,
    ):
        self.launchSurveyV2(
            schema_name="test_list_collector_primary_and_collector_with_driving_question"
        )

        self.assertInBody("Start section")

        self.post()

        self.assertInBody("Do you live here?")

        self.post({"you-live-here": "Yes"})

        self.post({"first-name": "James", "last-name": "May"})

        self.assertInUrl("/questionnaire/anyone-else-usually-live-at/")

        self.assertInBody("Does anyone else usually live at")

        self.post({"anyone-else-usually-live-at-answer": "No"})

        self.assertInUrl("/questionnaire/sections/section/")

        first_person_change_link = self.get_link("change", 1)

        self.get(first_person_change_link)

        self.assertInBody("What is your name")
