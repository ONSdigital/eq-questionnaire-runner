from tests.integration.questionnaire import QuestionnaireTestCase


class TestQuestionnaireRelationships(QuestionnaireTestCase):
    def remove_list_item(self, position):
        self.get("questionnaire/list-collector")
        self.get(self.get_link("remove", position))
        self.post({"remove-confirmation": "Yes"})

    def test_valid_relationship(self):
        self.launchSurvey("test_relationships")
        self.add_person("Marie", "Doe")
        self.add_person("John", "Doe")
        self.post({"anyone-else": "No"})
        self.post({"anyone-else": "No"})

        self.post({"relationship-answer": "Husband or Wife"})
        self.post()
        self.assertInUrl("/questionnaire/sections/")

    def test_resume_should_not_show_last_viewed_guidance(self):
        self.launchSurvey("test_relationships")
        self.add_person("Marie", "Doe")
        self.add_person("John", "Doe")
        self.post({"anyone-else": "No"})
        self.get("/questionnaire/relationships?resume=True")
        self.assertNotInUrl("resume=True")
        self.assertNotInBody("This is the last viewed question in this section")

    def test_last_relationship(self):
        self.launchSurvey("test_relationships")
        first_list_item_id = self.add_person("Marie", "Doe")
        second_list_item_id = self.add_person("John", "Doe")
        self.post({"anyone-else": "No"})
        self.get("/questionnaire/relationships?last=True")
        self.assertInUrl(
            f"/questionnaire/relationships/people/{first_list_item_id}/to/{second_list_item_id}"
        )

    def test_get_relationships_when_not_on_path_raises_404(self):
        self.launchSurvey("test_relationships")
        self.get("/questionnaire/relationships")
        self.assertStatusNotFound()

    def test_invalid_relationship_raises_404(self):
        self.launchSurvey("test_relationships")
        self.get("/questionnaire/relationships/people/fake-id/to/another-fake-id")
        self.assertStatusNotFound()

    def test_go_to_invalid_relationship(self):
        self.launchSurvey("test_relationships")
        self.add_person("Marie", "Doe")
        self.add_person("John", "Doe")
        self.post({"anyone-else": "No"})

        self.get("/questionnaire/relationships/people/fake-id/to/another-fake-id")
        self.assertInUrl("/questionnaire/relationships")

    def test_failed_validation(self):
        self.launchSurvey("test_relationships")
        self.add_person("Marie", "Doe")
        self.add_person("John", "Doe")
        self.post({"anyone-else": "No"})
        self.post()
        self.assertInBody("There is a problem with your answer")

    def test_multiple_relationships(self):
        self.launchSurvey("test_relationships")
        self.add_person("Marie", "Doe")
        self.add_person("John", "Doe")
        self.add_person("Susan", "Doe")
        self.post({"anyone-else": "No"})

        self.post({"relationship-answer": "Husband or Wife"})
        self.post({"relationship-answer": "Husband or Wife"})
        self.post({"relationship-answer": "Husband or Wife"})
        self.post()
        self.assertInUrl("/questionnaire/sections/section/")

    def test_relationships_removed_when_list_item_removed(self):
        self.launchSurvey("test_relationships", roles=["dumper"])
        self.add_person("Marie", "Doe")
        self.add_person("John", "Doe")
        self.add_person("Susan", "Doe")
        list_item_ids = self.get_list_item_ids()
        self.post({"anyone-else": "No"})

        self.post({"relationship-answer": "Husband or Wife"})
        self.post({"relationship-answer": "Husband or Wife"})
        self.post({"relationship-answer": "Husband or Wife"})

        self.remove_list_item(3)

        self.assertNotInBody("Susan Doe")

        relationship_answer = self.dump_debug()["ANSWERS"][-1]
        for relationship in relationship_answer["value"]:
            self.assertNotIn(list_item_ids[-1], relationship.values())

        self.remove_list_item(1)
        relationship_answer = self.dump_debug()["ANSWERS"][-1]
        del list_item_ids[-1]
        for relationship in relationship_answer["value"]:
            self.assertNotIn(list_item_ids[-1], relationship.values())

    def test_relationship_not_altered_when_new_list_item_not_submitted(self):
        self.launchSurvey("test_relationships")
        self.add_person("Marie", "Doe")
        self.add_person("John", "Doe")
        list_item_ids_original = self.get_list_item_ids()
        self.post({"anyone-else": "No"})
        self.post({"relationship-answer": "Husband or Wife"})

        self.get("/questionnaire/list-collector")
        self.add_person("Susan", "Doe")
        self.remove_list_item(3)
        list_item_ids_new = self.get_list_item_ids()
        self.post({"anyone-else": "No"})

        self.assertEqual(list_item_ids_original, list_item_ids_new)

    def test_post_to_relationships_root(self):
        self.launchSurvey("test_relationships")
        self.add_person("Marie", "Doe")
        self.add_person("John", "Doe")
        self.post({"anyone-else": "No"})
        self.post(url="/questionnaire/relationships")
        self.assertStatusOK()

    def test_head_request_on_relationships_url(self):
        self.launchSurvey("test_relationships")
        first_list_item_id = self.add_person("Marie", "Doe")
        second_list_item_id = self.add_person("John", "Doe")
        self.post({"anyone-else": "No"})
        self.head(
            f"/questionnaire/relationships/people/{first_list_item_id}/to/{second_list_item_id}"
        )
        self.assertStatusOK()
