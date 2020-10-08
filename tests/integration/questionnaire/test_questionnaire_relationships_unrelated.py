from . import QuestionnaireTestCase


class TestQuestionnaireRelationshipsUnrelated(QuestionnaireTestCase):
    def launch_survey_and_add_people(self):
        self.launchSurvey("test_relationships_unrelated", roles=["dumper"])
        self.add_person("Marie", "Doe")
        self.add_person("John", "Doe")
        self.post({"anyone-else": "No"})

    def test_relationship_unrelated_is_accessible_when_list_name_and_list_item_valid(
        self,
    ):
        self.launch_survey_and_add_people()

        first_list_item = self.dump_debug()["LISTS"][0]["items"][0]
        self.get(
            f"/questionnaire/relationships/people/{first_list_item}/related-to-anyone-else"
        )
        self.assertInBody("Are any of these people related to you?")
        self.assertInBody("Marie Doe")
        self.assertInBody("John Doe")

    def test_unrelated_relationship_is_not_accessible_when_invalid_list_item(self):
        self.launchSurvey("test_relationships_unrelated")
        self.get(
            f"/questionnaire/relationships/people/invalid-id/related-to-anyone-else"
        )
        self.assertStatusNotFound()

    def test_relationship_unrelated_is_not_accessible_when_invalid_list_name(self):
        self.launch_survey_and_add_people()

        first_list_item = self.dump_debug()["LISTS"][0]["items"][0]
        self.get(
            f"/questionnaire/relationships/invalid-list-name/{first_list_item}/related-to-anyone-else"
        )
        self.assertStatusNotFound()

    def test_unrelated_relationship_is_not_accessible_when_invalid_block_id(self):
        self.launch_survey_and_add_people()

        first_list_item = self.dump_debug()["LISTS"][0]["items"][0]
        self.get(
            f"/questionnaire/relationships/people/{first_list_item}/invalid-block-id"
        )
        self.assertStatusNotFound()
