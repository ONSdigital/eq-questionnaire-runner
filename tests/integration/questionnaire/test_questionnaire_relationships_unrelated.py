from . import QuestionnaireTestCase


class TestQuestionnaireRelationshipsUnrelated(QuestionnaireTestCase):
    def test_relationship_unrelated_is_accessible_when_list_not_empty(self):
        self.launchSurvey("test_relationships_unrelated", roles=["dumper"])
        self.add_person("Marie", "Doe")
        self.add_person("John", "Doe")
        self.post({"anyone-else": "No"})

        first_list_item = self.dump_debug()["LISTS"][0]["items"][0]
        self.get(
            f"/questionnaire/relationships/people/{first_list_item}/related-to-anyone-else"
        )
        self.assertInBody("Are any of these people related to you?")
        self.assertInBody("Marie Doe")
        self.assertInBody("John Doe")

    def test_unrelated_relationship_is_not_accessible_invalid_list_item(self):
        self.launchSurvey("test_relationships_unrelated")
        self.get(
            f"/questionnaire/relationships/people/invalid-id/related-to-anyone-else"
        )
        self.assertStatusNotFound()
