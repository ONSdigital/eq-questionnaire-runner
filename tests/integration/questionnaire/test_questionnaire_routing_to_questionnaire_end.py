from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.questionnaire import SUBMIT_URL_PATH


class TestRoutingToQuestionnaireEndBase(IntegrationTestCase):
    def _launch_and_complete_questionnaire(self, schema):
        self.launchSurveyV2(schema_name=schema)
        self.post({"test-answer": "No"})


class TestRoutingToQuestionnaireEndSingleSection(TestRoutingToQuestionnaireEndBase):
    def test_able_to_route_to_questionnaire_end(self):
        # Given I launch a questionnaire with a single section and answer "No" to the first question
        self._launch_and_complete_questionnaire(
            "test_routing_to_questionnaire_end_single_section"
        )

        # Then I should be routed to the end of the questionnaire and be shown the submit page
        self.assertInBody("Would you like to complete question 2?")
        self.assertInUrl(SUBMIT_URL_PATH)


class TestRoutingToQuestionnaireEndMultipleSections(TestRoutingToQuestionnaireEndBase):
    def test_able_to_route_to_questionnaire_end(self):
        # Given I launch a questionnaire with multiple sections
        # When I answer "No" to the first question
        self._launch_and_complete_questionnaire(
            "test_routing_to_questionnaire_end_multiple_sections"
        )

        # Then I should be routed to the end of the questionnaire and be shown the submit page with only 1 section
        self.assertInBody("Would you like to complete section 2?")
        self.assertInBody("Section 1")
        self.assertNotInBody("Section 2")
        self.assertInUrl(SUBMIT_URL_PATH)

    def test_section_is_reenabled_when_changing_answer_after_routing_to_questionnaire_end(
        self,
    ):
        # Given I am able to route to the questionnaire end by completing only section 1
        self._launch_and_complete_questionnaire(
            "test_routing_to_questionnaire_end_multiple_sections"
        )
        self.assertInUrl(SUBMIT_URL_PATH)

        # When I change my answer in section 1
        self.get("questionnaire/test-forced/?return_to=final-summary#test-answer")
        self.post({"test-answer": "Yes"})

        # Then I am able to complete section 2 and view the answers on the submit page
        self.assertInUrl("/test-optional")
        self.post({"test-optional-answer": "I am a completionist"})
        self.assertInUrl(SUBMIT_URL_PATH)

        self.assertInBody("Section 1")
        self.assertInBody("Section 2")
        self.assertInBody("Why did you choose to complete this section?")
