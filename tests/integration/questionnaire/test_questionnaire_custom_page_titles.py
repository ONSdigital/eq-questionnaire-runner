from . import QuestionnaireTestCase


class TestQuestionnaireCustomPageTitles(QuestionnaireTestCase):
    def test_custom_page_titles(self):
        self.launchSurvey("test_custom_page_titles")
        self.post()
        self.assertEqualPageTitle("Custom page title")

        self.post({"anyone-else": "Yes"})
        self.assertEqualPageTitle("Add person 1")

        self.post({"first-name": "Marie", "last-name": "Doe"})
        self.post({"anyone-else": "Yes"})
        self.assertEqualPageTitle("Add person 2")

        self.post({"first-name": "John", "last-name": "Doe"})
        self.add_person("Susan", "Doe")
        self.post({"anyone-else": "No"})

        self.assertEqualPageTitle("How Person 1 is related to Person 2")
        self.post({"relationship-answer": "Husband or Wife"})

        self.assertEqualPageTitle("How Person 1 is related to Person 3")
        self.post({"relationship-answer": "Husband or Wife"})

        self.assertEqualPageTitle("How Person 2 is related to Person 3")
        self.post({"relationship-answer": "Husband or Wife"})

        self.assertEqualPageTitle("Custom section summary page title")

        self.post()
        self.post()
        self.assertEqualPageTitle("Person 1 individual interstitial")

        self.post()
        self.assertEqualPageTitle("Person 1 proxy question")

        self.post()
        self.post()
        self.post()
        self.post()
        self.assertEqualPageTitle("Person 2 individual interstitial")

        self.post()
        self.assertEqualPageTitle("Person 2 proxy question")
        self.post()
        self.assertEqualPageTitle("Custom question page title")
