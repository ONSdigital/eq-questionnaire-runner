from tests.integration.integration_test_case import IntegrationTestCase


class TestCaseSensitiveRouting(IntegrationTestCase):
    """
    Test that routing on checkbox list of answers is case insensitive.
    """

    def test_routing_equals_case_sensitive_tuple(self):
        # Given I launch routing rules schema that has case sensitive tuple to compare
        self.launchSurvey("test_new_routing_checkbox_contains_any")

        # When I submit "India" and "Malta" as an answer
        self.post({"country-checkbox-answer": ["India", "Malta"]})

        # Then I should see the correct text
        self.assertInBody("You chose India or Malta (or both).")
