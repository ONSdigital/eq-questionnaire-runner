from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.questionnaire import HUB_URL_PATH, THANK_YOU_URL_PATH


class TestQuestionnaireHub(IntegrationTestCase):
    def test_navigation_to_hub_route_when_hub_not_enabled(self):
        # Given the hub is not enabled
        self.launchSurvey("test_checkbox")

        # When I navigate to the hub url
        self.get(HUB_URL_PATH)

        # Then I should be redirected to the first incomplete question
        self.assertInBody("Which pizza toppings would you like?")
        self.assertInUrl("mandatory-checkbox")

    def test_redirect_to_hub_when_section_complete(self):
        # Given the hub is enabled
        self.launchSurvey("test_hub_and_spoke")

        # When I complete a section
        self.post()
        self.post({"employment-status-answer": "Working as an employee"})

        # Then I should be redirected to the hub
        self.assertEqualUrl(HUB_URL_PATH)

    def test_hub_section_url_when_hub_not_enabled(self):
        # Given the hub is not enabled
        self.launchSurvey("test_checkbox")

        # When I navigate to the url for a hub's section
        self.get("/questionnaire/sections/default-section/")

        # Then I should be redirected to the correct location for that section
        self.assertEqualUrl("/questionnaire/mandatory-checkbox/")

    def test_section_url_when_hub_enabled_and_section_not_started(self):
        # Given the hub is enabled
        self.launchSurvey("test_hub_and_spoke")

        # When I navigate to a url for a hub's section
        self.get("questionnaire/sections/employment-section/")

        # Then I should be redirected to the first incomplete question in the section
        self.assertEqualUrl("/questionnaire/employment-status/")

    def test_hub_section_url_when_hub_enabled_and_section_in_progress(self):
        # Given the hub is enabled and a section is in-progress
        self.launchSurvey("test_hub_and_spoke")
        self.post()
        self.post({"employment-status-answer-exclusive": "None of these apply"})
        self.get(HUB_URL_PATH)
        self.assertInBody("Partially completed")
        self.assertEqualUrl(HUB_URL_PATH)

        # When I navigate to the url for a hub's section that is in-progress
        self.get("/questionnaire/employment-type/?resume=True")

        # Then I should be redirected to the first incomplete question in the section
        self.assertEqualUrl("/questionnaire/employment-type/?resume=True")

    def test_hub_section_url_when_hub_enabled_and_section_complete(self):
        # Given the hub is enabled and a section is complete
        self.launchSurvey("test_hub_and_spoke")
        self.get("/questionnaire/sections/accommodation-section/")
        self.post()
        self.post()
        self.assertInBody("View answers")
        self.assertEqualUrl(HUB_URL_PATH)

        # When I navigate to the url for a hub's section that is complete
        self.get("/questionnaire/sections/accommodation-section/")

        # Then I should be redirected to the last completed question in the section
        self.assertEqualUrl("/questionnaire/sections/accommodation-section/")

    def test_hub_inaccessible_if_sections_required_and_incomplete(self):
        self.launchSurvey("test_hub_complete_sections")

        self.get(HUB_URL_PATH)

        # Redirected to first question to complete
        self.assertEqualUrl("/questionnaire/employment-status/")

    def test_hub_accessible_if_sections_required_and_complete(self):
        self.launchSurvey("test_hub_complete_sections")

        self.post({"employment-status-answer": "Working as an employee"})
        self.post()

        self.get(HUB_URL_PATH)

        self.assertEqualUrl(HUB_URL_PATH)

    def test_hub_displays_repeating_sections_with_valid_urls(self):
        # Given the hub is enabled and a section is complete
        self.launchSurvey("test_repeating_sections_with_hub_and_spoke")
        # Go to first section
        self.post()

        # Add a primary person
        self.post({"you-live-here": "Yes"})
        self.post({"first-name": "John", "last-name": "Doe"})

        # First list collector
        self.post({"anyone-else": "Yes"})

        self.post({"first-name": "Anna", "last-name": "Doe"})

        # Go to second list collector
        self.post({"anyone-else": "No"})

        # Submit interstitial page
        self.post()

        # Go to visitors
        self.post({"another-anyone-else": "No"})

        # Visitors
        self.post({"visitors-anyone-else": "Yes"})

        self.post({"visitor-first-name": "Joe", "visitor-last-name": "Public"})

        # Go back to hub
        self.post({"visitors-anyone-else": "No"})
        self.post()

        table_title_selector = ".ons-summary__item-title"
        self.assertInSelector("John Doe", table_title_selector)
        self.assertInSelector("Anna Doe", table_title_selector)
        self.assertInSelector("Joe Public", table_title_selector)

        section_urls = self.getHtmlSoup().find_all(
            "a", class_="ons-summary__button", href=True
        )

        # Go to first section
        first_repeating_section_url = section_urls[1].attrs["href"]
        self.get(first_repeating_section_url)
        self.post({"proxy-answer": "Yes"})

        self.assertInBody("What is <em>John Doe’s</em> date of birth?")

        self.get(HUB_URL_PATH)

        # Go to second section
        second_repeating_section_url = section_urls[2].attrs["href"]
        self.get(second_repeating_section_url)
        self.post({"proxy-answer": "Yes"})

        self.assertInBody("What is <em>Anna Doe’s</em> date of birth?")

        # Go to visitors
        visitor_repeating_section_url = section_urls[3].attrs["href"]
        self.get(visitor_repeating_section_url)
        self.assertInBody("What is <em>Joe Public’s</em> date of birth?")

    def test_hub_section_required_but_enabled_false(self):
        # Given the hub is enabled and there are two required sections
        self.launchSurvey("test_hub_section_required_and_enabled")

        # When I answer 'No' to the first section, meaning the second section is not enabled
        self.post({"household-relationships-answer": "No"})

        # Then I should be redirected to the hub and can submit my answers without completing the other section
        self.assertEqualUrl(HUB_URL_PATH)
        self.post()
        self.assertEqualUrl(THANK_YOU_URL_PATH)

    def test_hub_section_required_but_enabled_true(self):
        # Given the hub is enabled and there are two required sections
        self.launchSurvey("test_hub_section_required_and_enabled")

        # When I answer 'Yes' to the first section, meaning the second section is enabled
        self.post({"household-relationships-answer": "Yes"})

        # Then I should be redirected to the second section
        self.assertEqualUrl("/questionnaire/relationships-count/")

    def test_hub_section_enabled_and_accessible_with_repeating_sections(self):
        # Given the hub is enabled and there are two required sections (and one is for a repeat)
        self.launchSurvey("test_hub_section_required_with_repeat")

        # When I answer I complete the first section and the repeating section
        self.post({"you-live-here": "Yes"})
        self.post({"first-name": "John", "last-name": "Doe"})
        self.post({"anyone-else": "No"})
        self.post()
        self.post({"proxy-answer": "Yes"})
        self.post(
            {
                "date-of-birth-answer-day": 1,
                "date-of-birth-answer-month": 2,
                "date-of-birth-answer-year": 1999,
            }
        )
        self.post()

        # Then I should see the hub
        self.assertEqualUrl(HUB_URL_PATH)

    def test_hub_section_is_inaccessible_when_all_repeats_not_complete(self):
        # Given the hub is enabled and there are two required sections (and one is for a repeat)
        self.launchSurvey("test_hub_section_required_with_repeat")

        # When I  complete the first section and the first repeat, but not the second repeat
        self.post({"you-live-here": "Yes"})
        self.post({"first-name": "John", "last-name": "Doe"})
        self.post({"anyone-else": "Yes"})
        self.post({"first-name": "Jane", "last-name": "Doe"})
        self.post({"anyone-else": "No"})
        self.post()
        self.post({"proxy-answer": "Yes"})
        self.post(
            {
                "date-of-birth-answer-day": 1,
                "date-of-birth-answer-month": 2,
                "date-of-birth-answer-year": 1999,
            }
        )
        self.post()

        # Then the hub should not yet be accessible
        self.get(HUB_URL_PATH)
        self.assertInUrl("/proxy")
