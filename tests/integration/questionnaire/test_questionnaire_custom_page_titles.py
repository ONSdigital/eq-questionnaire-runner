from . import QuestionnaireTestCase


class TestQuestionnaireCustomPageTitles(QuestionnaireTestCase):
    def test_custom_page_titles(self):
        self.launchSurvey("test_custom_page_titles")
        self.post()
        self.assertEqualPageTitle("Custom page title - Test Custom Page Titles")

        self.post({"anyone-else": "Yes"})
        self.assertEqualPageTitle("Add person 1 - Test Custom Page Titles")

        self.post({"first-name": "Marie", "last-name": "Doe"})
        self.post({"anyone-else": "Yes"})
        self.assertEqualPageTitle("Add person 2 - Test Custom Page Titles")

        self.post({"first-name": "John", "last-name": "Doe"})
        self.add_person("Susan", "Doe")
        self.post({"anyone-else": "No"})

        self.assertEqualPageTitle(
            "How Person 1 is related to Person 2 - Test Custom Page Titles"
        )
        self.post({"relationship-answer": "Husband or Wife"})

        self.assertEqualPageTitle(
            "How Person 1 is related to Person 3 - Test Custom Page Titles"
        )
        self.post({"relationship-answer": "Husband or Wife"})

        self.assertEqualPageTitle(
            "How Person 2 is related to Person 3 - Test Custom Page Titles"
        )
        self.post({"relationship-answer": "Husband or Wife"})

        self.assertEqualPageTitle(
            "Custom section summary page title - Test Custom Page Titles"
        )

    def test_custom_repeating_page_titles(self):
        self.launchSurvey("test_custom_page_titles")
        self.post()
        self.post({"anyone-else": "Yes"})
        self.post({"first-name": "Marie", "last-name": "Doe"})
        self.add_person("John", "Doe")
        self.post({"anyone-else": "No"})
        self.post({"relationship-answer": "Husband or Wife"})
        self.post()
        self.post()
        self.assertEqualPageTitle(
            "Individual interstitial: Person 1 - Test Custom Page Titles"
        )

        self.post()
        self.assertEqualPageTitle("Proxy question: Person 1 - Test Custom Page Titles")

        self.post()
        self.assertEqualPageTitle(
            "What is your date of birth?: Person 1 - Test Custom Page Titles"
        )

        self.post()
        self.assertEqualPageTitle("Summary: Person 1 - Test Custom Page Titles")

        self.post()
        self.post()
        self.assertEqualPageTitle(
            "Individual interstitial: Person 2 - Test Custom Page Titles"
        )

        self.post()
        self.assertEqualPageTitle("Proxy question: Person 2 - Test Custom Page Titles")

        self.post()
        self.assertEqualPageTitle(
            "What is your date of birth?: Person 2 - Test Custom Page Titles"
        )

        self.post()
        self.assertEqualPageTitle("Summary: Person 2 - Test Custom Page Titles")
