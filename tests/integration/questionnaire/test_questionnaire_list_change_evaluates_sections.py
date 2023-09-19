from tests.integration.questionnaire import QuestionnaireTestCase


class TestQuestionnaireListChangeEvaluatesSections(QuestionnaireTestCase):
    def get_link(self, action, position):
        selector = f"[data-qa='list-item-{action}-{position}-link']"
        selected = self.getHtmlSoup().select(selector)

        filtered = [html for html in selected if position in html.get_text()]

        return filtered[0].get("href")

    def test_without_primary_person(self):
        self.launchSurvey("test_list_change_evaluates_sections")

        self.get("/questionnaire/sections/who-lives-here/")
        self.assertEqualUrl("/questionnaire/primary-person-list-collector/")
        self.post({"you-live-here": "No"})
        self.assertEqualUrl("/questionnaire/list-collector/")

        self.post({"anyone-else": "No"})
        self.post()
        self.assertEqualUrl("/questionnaire/")

        self.get("/questionnaire/sections/accommodation-section/")
        self.assertEqualUrl("/questionnaire/accommodation-type/")

        self.post()
        self.post()
        self.post()
        self.assertEqualUrl("/questionnaire/")

        self.get("questionnaire/people/add-person")
        self.add_person("John", "Doe")
        self.post({"anyone-else": "No"})
        self.assertEqualUrl("/questionnaire/sections/who-lives-here/")
        self.post()
        self.assertEqualUrl("/questionnaire/")

        self.assertInSelector(
            "Partially completed", "[data-qa='hub-row-accommodation-section-state']"
        )

        self.get("questionnaire/sections/accommodation-section/")
        self.assertEqualUrl("/questionnaire/own-or-rent/?resume=True")

    def test_with_primary_person(self):
        self.launchSurvey("test_list_change_evaluates_sections")

        self.get("/questionnaire/sections/accommodation-section/")
        self.post()
        self.post()
        self.assertEqualUrl("/questionnaire/sections/accommodation-section/")
        self.post()

        self.assertInSelector(
            "Completed", "[data-qa='hub-row-accommodation-section-state']"
        )

        self.get("/questionnaire/sections/who-lives-here/")
        self.assertEqualUrl("/questionnaire/primary-person-list-collector/")
        self.post({"you-live-here": "Yes"})
        self.add_person("John", "Doe")
        self.post({"anyone-else": "No"})
        self.post()

        self.assertEqualUrl("/questionnaire/")
        self.assertInSelector(
            "Partially completed", "[data-qa='hub-row-accommodation-section-state']"
        )
