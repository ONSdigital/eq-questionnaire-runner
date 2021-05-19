from tests.integration.integration_test_case import IntegrationTestCase

SECTION_SUMMARY_URL_PATH = "/questionnaire/sections/{section_id}/"


class TestRoutingToSectionEnd(IntegrationTestCase):
    def test_section_summary_not_available_if_any_question_in_section_incomplete(self):
        # Given I launch questionnaire and have not answered questions for a section
        self.launchSurvey("test_routing_to_section_end")

        # When I try access the section summary
        self.get(SECTION_SUMMARY_URL_PATH.format(section_id="test-routing-section"))

        # Then I am redirected to the first incomplete question in the section
        self.assertInUrl("/test-routing-forced")

    def test_section_summary_available_after_completing_section(self):
        # Given I launch questionnaire and have completed a section
        self.launchSurvey("test_routing_to_section_end")
        self.post({"test-routing-answer": "No"})
        self.assertInBody("Were you forced to complete section 1?")
        self.assertInUrl(
            SECTION_SUMMARY_URL_PATH.format(section_id="test-routing-section")
        )

    def test_section_summary_not_available_after_invalidating_section(self):
        # Given I launch questionnaire and have completed a section
        self.launchSurvey("test_routing_to_section_end")
        self.post({"test-routing-answer": "No"})
        self.assertInBody("Were you forced to complete section 1?")
        self.assertInUrl(
            SECTION_SUMMARY_URL_PATH.format(section_id="test-routing-section")
        )
        self.post()

        # When I invalidate any block in the section and try access its section summary
        self.get("questionnaire/test-routing-forced#test-routing-answer")
        self.post({"test-routing-answer": "Yes"})

        self.get(SECTION_SUMMARY_URL_PATH.format(section_id="test-routing-section"))

        # Then I am redirected to the first incomplete question in the section
        self.assertInUrl("/test-routing-optional")
