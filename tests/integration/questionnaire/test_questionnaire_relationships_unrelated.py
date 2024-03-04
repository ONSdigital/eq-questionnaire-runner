from tests.integration.questionnaire import QuestionnaireTestCase


class TestQuestionnaireRelationshipsUnrelated(QuestionnaireTestCase):
    def launch_survey_and_add_people(self):
        self.launchSurvey("test_relationships_unrelated", roles=["dumper"])
        self.add_person("Andrew", "Austin")
        self.add_person("Betty", "Burns")
        self.add_person("Carla", "Clark")
        self.add_person("Daniel", "Davis")
        self.add_person("Eve", "Elliot")
        self.add_person("Fred", "Francis")

    def get_selected_relationship(self):
        for option in self.getHtmlSoup().find_all(
            "input", {"name": "relationship-answer"}
        ):
            if option.has_attr("checked"):
                return option.attrs["value"]
        return None

    def get_relationship_answer_from_answer_store(self):
        answers = self.dump_debug()["ANSWERS"]
        for answer in answers:
            if answer["answer_id"] == "relationship-answer":
                return answer["value"]

    def test_is_accessible_when_list_name_and_list_item_valid(
        self,
    ):
        self.launch_survey_and_add_people()
        self.post({"anyone-else": "No"})
        self.post({"relationship-answer": "Unrelated"})
        self.post({"relationship-answer": "Unrelated"})

        self.assertInBody("Are any of these people related to you?")

    def test_is_not_accessible_when_invalid_list_item(self):
        self.launchSurvey("test_relationships_unrelated")
        self.get(
            "/questionnaire/relationships/people/invalid-id/related-to-anyone-else"
        )
        self.assertStatusNotFound()

    def test_is_not_accessible_when_invalid_list_name(self):
        self.launch_survey_and_add_people()
        first_list_item = self.get_list_item_ids()[0]
        self.post({"anyone-else": "No"})

        self.get(
            f"/questionnaire/relationships/invalid-list-name/{first_list_item}/related-to-anyone-else"
        )
        self.assertStatusNotFound()

    def test_is_not_accessible_when_invalid_block_id(self):
        self.launch_survey_and_add_people()
        first_list_item = self.get_list_item_ids()[0]
        self.post({"anyone-else": "No"})

        self.get(
            f"/questionnaire/relationships/people/{first_list_item}/invalid-block-id"
        )
        self.assertStatusNotFound()

    def test_list_summary(self):
        self.launch_survey_and_add_people()
        self.post({"anyone-else": "No"})
        self.post({"relationship-answer": "Unrelated"})
        self.post({"relationship-answer": "Unrelated"})

        self.assertNotInBody("Andrew Austin")
        self.assertNotInBody("Betty Burns")
        self.assertNotInBody("Carla Clark")
        self.assertInBody("Daniel Davis")
        self.assertInBody("Eve Elliot")
        self.assertInBody("Fred Francis")

    def test_list_summary_for_second_person(self):
        self.launch_survey_and_add_people()
        self.post({"anyone-else": "No"})
        self.post({"relationship-answer": "Unrelated"})
        self.post({"relationship-answer": "Unrelated"})
        self.post(
            {
                "related-to-anyone-else-answer": "No, none of these people are related to me"
            }
        )
        self.post({"relationship-answer": "Unrelated"})
        self.post({"relationship-answer": "Unrelated"})

        self.assertNotInBody("Andrew Austin")
        self.assertNotInBody("Carla Clark")
        self.assertNotInBody("Daniel Davis")
        self.assertInBody("Eve Elliot")
        self.assertInBody("Fred Francis")

    def test_change_answer_changes_routing_path(self):
        self.launch_survey_and_add_people()
        self.post({"anyone-else": "No"})
        self.post({"relationship-answer": "Unrelated"})
        self.post({"relationship-answer": "Unrelated"})
        self.assertInBody("Are any of these people related to you?")
        self.previous()
        self.post({"relationship-answer": "Husband or Wife"})
        self.assertNotInBody("Are any of these people related to you?")

    def test_returning_to_list_summary_displays_the_correct_list(self):
        self.launch_survey_and_add_people()
        self.post({"anyone-else": "No"})
        self.post({"relationship-answer": "Unrelated"})
        self.post({"relationship-answer": "Unrelated"})
        self.assertInBody("Are any of these people related to you?")
        self.post(
            {
                "related-to-anyone-else-answer": "No, none of these people are related to me"
            }
        )
        self.previous()
        self.assertNotInBody("Andrew Austin")
        self.assertNotInBody("Betty Burns")
        self.assertNotInBody("Carla Clark")
        self.assertInBody("Daniel Davis")
        self.assertInBody("Eve Elliot")
        self.assertInBody("Fred Francis")

    def test_variants(self):
        self.launch_survey_and_add_people()
        self.post({"anyone-else": "No"})
        self.post({"relationship-answer": "Unrelated"})
        self.post({"relationship-answer": "Unrelated"})
        self.post(
            {
                "related-to-anyone-else-answer": "No, none of these people are related to me"
            }
        )
        self.post({"relationship-answer": "Unrelated"})
        self.post({"relationship-answer": "Unrelated"})
        self.assertInBody(
            'Are any of these people related to <strong>Betty Burns</strong>?'
        )

    def test_variant_no_answer_routes_to_next_person(self):
        self.launch_survey_and_add_people()
        self.post({"anyone-else": "No"})
        self.post({"relationship-answer": "Unrelated"})
        self.post({"relationship-answer": "Unrelated"})
        self.post(
            {
                "related-to-anyone-else-answer": "No, none of these people are related to me"
            }
        )
        self.post({"relationship-answer": "Unrelated"})
        self.post({"relationship-answer": "Unrelated"})
        self.post(
            {
                "related-to-anyone-else-answer": "No, none of these people are related to {person_name}"
            }
        )
        self.assertInBody("Thinking about Carla Clark, Daniel Davis is their")

    def test_yes_answer_clears_unrelated_relationships(self):
        self.launch_survey_and_add_people()
        self.post({"anyone-else": "No"})
        self.post({"relationship-answer": "Unrelated"})
        self.post({"relationship-answer": "Unrelated"})
        self.post({"related-to-anyone-else-answer": "Yes"})
        self.post({"relationship-answer": "Unrelated"})
        self.previous()
        self.previous()
        self.post({"related-to-anyone-else-answer": "Yes"})
        assert not self.get_selected_relationship()

    def test_yes_answer_doesnt_clear_related_relationships(self):
        self.launch_survey_and_add_people()
        self.post({"anyone-else": "No"})
        self.post({"relationship-answer": "Unrelated"})
        self.post({"relationship-answer": "Unrelated"})
        self.post({"related-to-anyone-else-answer": "Yes"})
        self.post({"relationship-answer": "Husband or Wife"})
        self.previous()
        self.previous()
        self.post({"related-to-anyone-else-answer": "Yes"})
        assert self.get_selected_relationship() == "Husband or Wife"

    def test_no_answer_populates_unrelated_relationships(self):
        self.launch_survey_and_add_people()
        self.post({"anyone-else": "No"})
        self.post({"relationship-answer": "Unrelated"})
        self.post({"relationship-answer": "Unrelated"})
        self.post(
            {
                "related-to-anyone-else-answer": "No, none of these people are related to me"
            }
        )
        relationship_answers = self.get_relationship_answer_from_answer_store()
        relationships = [
            relationship_answer["relationship"]
            for relationship_answer in relationship_answers
        ]
        assert len(relationship_answers) == 5
        assert len(set(relationships)) == 1
