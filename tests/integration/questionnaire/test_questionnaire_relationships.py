from . import QuestionnaireTestCase


class TestQuestionnaireRelationships(QuestionnaireTestCase):
    def remove_list_item(self, rowIndex):
        self.get("questionnaire/list-collector")
        selector = f"[data-qa='list-item-remove-{rowIndex}-link']"
        selected = self.getHtmlSoup().select(selector)
        self.get(list(selected)[0].get("href"))
        self.post({"remove-confirmation": "Yes"})

    def test_valid_relationship(self):
        self.launchSurvey("test_relationships")
        self.add_person("Marie", "Doe")
        self.add_person("John", "Doe")
        self.post({"anyone-else": "No"})

        self.post({"relationship-answer": "Husband or Wife"})
        self.post()
        self.assertInUrl("/questionnaire/sections/")

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
        self.post({"anyone-else": "No"})

        self.post({"relationship-answer": "Husband or Wife"})
        self.post({"relationship-answer": "Husband or Wife"})
        self.post({"relationship-answer": "Husband or Wife"})

        list_item_ids = self.dump_debug()["LISTS"][0]["items"]
        self.remove_list_item("3")

        self.assertNotInBody("Susan Doe")

        relationship_answer = self.dump_debug()["ANSWERS"][-1]
        for relationship in relationship_answer["value"]:
            self.assertNotIn(list_item_ids[-1], relationship.values())

        self.remove_list_item("1")
        relationship_answer = self.dump_debug()["ANSWERS"][-1]
        del list_item_ids[-1]
        for relationship in relationship_answer["value"]:
            self.assertNotIn(list_item_ids[-1], relationship.values())

    def test_relationship_not_altered_when_new_list_item_not_submitted(self):
        self.launchSurvey("test_relationships", roles=["dumper"])
        self.add_person("Marie", "Doe")
        self.add_person("John", "Doe")
        self.post({"anyone-else": "No"})
        self.post({"relationship-answer": "Husband or Wife"})

        list_item_ids_original = self.dump_debug()["LISTS"][0]["items"]

        self.get("/questionnaire/list-collector")
        self.add_person("Susan", "Doe")
        self.remove_list_item("3")
        self.post({"anyone-else": "No"})

        list_item_ids_new = self.dump_debug()["LISTS"][0]["items"]

        self.assertEqual(list_item_ids_original, list_item_ids_new)
