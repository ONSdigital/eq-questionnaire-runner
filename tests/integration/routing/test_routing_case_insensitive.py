from tests.integration.integration_test_case import IntegrationTestCase


class TestCaseInsensitiveRouting(IntegrationTestCase):
    """
    Test that routing on text field answers is case insensitive.
    """

    def test_routing_equals_any_case_insensitive(self):
        self.launchSurveyV2(schema_name="test_routing_case_insensitive_text_field")

        # Given I launch the case insensiitive routing rules schema
        self.post(action="start_questionnaire")

        # When I submit "india" as an answer
        self.post({"country-text-field-answer": "india"})

        # Then I should see the correct text
        self.assertInBody("You submitted India or Azerbaijan.")

    def test_routing_equals_case_insensitive(self):
        self.launchSurveyV2(schema_name="test_routing_case_insensitive_text_field")

        # Given I launch the case insensiitive routing rules schema
        self.post(action="start_questionnaire")

        # When I submit "india" as an answer
        self.post({"country-text-field-answer": "georgia"})

        # Then I should see the correct text
        self.assertInBody("You submitted Georgia.")
