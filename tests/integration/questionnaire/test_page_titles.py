from tests.integration.integration_test_case import IntegrationTestCase


class TestPageTitles(IntegrationTestCase):
    def test_should_have_error_in_page_title_when_fail_validation(self):
        # Given
        self.launchSurvey("test_checkbox")
        # When
        self.post()
        # Then
        self.assertEqualPageTitle(
            "Error: Which pizza toppings would you like? - Other input fields"
        )
