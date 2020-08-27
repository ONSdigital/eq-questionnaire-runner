from tests.integration.integration_test_case import IntegrationTestCase


class TestRenderDropdownWidget(IntegrationTestCase):
    def setUp(self):
        super().setUp()
        # Given
        self.launchSurvey("test_address")

    def test_address_line_1_is_mandatory(self):
        # When
        self.post({})

        # Then
        self.assertInBody("Enter an address to continue")

    def test_empty_address_field_are_not_displayed_on_summary(self):
        # When
        self.post({"address-line1": "7 Evelyn Street", "address-postcode": "CF63 4JG"})

        # Then
        self.assertInBody("7 Evelyn Street<br/>CF63 4JG")

    def test_address_fields_are_filled_in_when_revisting_the_page(self):
        # Given
        self.post({"address-line1": "7 Evelyn Street", "address-postcode": "CF63 4JG"})
        self.assertInUrl("/summary")

        # When
        self.get("questionnaire/address-block/")

        # Then
        self.assertInBody("7 Evelyn Street")
        self.assertInBody("CF63 4JG")
