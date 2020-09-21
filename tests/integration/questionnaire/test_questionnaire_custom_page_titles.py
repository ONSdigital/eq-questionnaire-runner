from . import QuestionnaireTestCase


class TestQuestionnaireCustomPageTitles(QuestionnaireTestCase):
    def test_custom_page_titles(self):
        self.launchSurvey("test_custom_page_titles")
        self.post()
        self.assertEqualPageTitle("Custom page title - Census 2021")

        self.post({"anyone-else": "Yes"})
        self.assertEqualPageTitle("Add person 1 - Census 2021")

        self.post({"first-name": "Marie", "last-name": "Doe"})
        self.post({"anyone-else": "Yes"})
        self.assertEqualPageTitle("Add person 2 - Census 2021")

        self.post({"first-name": "John", "last-name": "Doe"})
        self.add_person("Susan", "Doe")
        self.post({"anyone-else": "No"})

        self.assertEqualPageTitle("How Person 1 is related to Person 2 - Census 2021")
        self.post({"relationship-answer": "Husband or Wife"})

        self.assertEqualPageTitle("How Person 1 is related to Person 3 - Census 2021")
        self.post({"relationship-answer": "Husband or Wife"})

        self.assertEqualPageTitle("How Person 2 is related to Person 3 - Census 2021")
        self.post({"relationship-answer": "Husband or Wife"})

        self.assertEqualPageTitle("Custom section summary page title - Census 2021")

        self.post()
        self.post()
        self.assertEqualPageTitle("Person 1 individual interstitial - Census 2021")

        self.post()
        self.assertEqualPageTitle("Person 1 proxy question - Census 2021")

        self.post()
        self.post()
        self.post()
        self.post()
        self.assertEqualPageTitle("Person 2 individual interstitial - Census 2021")

        self.post()
        self.assertEqualPageTitle("Person 2 proxy question - Census 2021")
        self.post()
        self.assertEqualPageTitle("Custom question page title - Census 2021")
