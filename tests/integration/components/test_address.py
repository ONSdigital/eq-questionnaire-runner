from tests.integration.integration_test_case import IntegrationTestCase


class TestRenderDropdownWidget(IntegrationTestCase):
    def setUp(self):
        super().setUp()
        # Given
        self.launchSurvey("test_address")

    def test_mandatory_address_line_1_is_mandatory(self):
        # When
        self.post({})

        # Then
        self.assertInBody("Enter an address to continue")

    def test_empty_address_field_are_not_displayed_on_summary(self):
        # When
        self.post(
            {
                "address-mandatory-line1": "7 Evelyn Street",
                "address-mandatory-postcode": "CF63 4JG",
            }
        )
        self.post({})

        # Then
        self.assertInBody("7 Evelyn Street<br/>CF63 4JG")

    def test_address_fields_are_filled_in_when_revisting_the_page(self):
        # Given
        self.post(
            {
                "address-mandatory-line1": "7 Evelyn Street",
                "address-mandatory-postcode": "CF63 4JG",
            }
        )
        self.post({})
        self.assertInUrl("/summary")

        # When
        self.get("questionnaire/address-block-mandatory/")

        # Then
        self.assertInBody("7 Evelyn Street")
        self.assertInBody("CF63 4JG")

    def test_optional_address_displays_no_answer_provided_on_summary_when_not_provided(
        self,
    ):
        # When
        self.post({"address-mandatory-line1": "first address"})
        self.post({})

        # Then
        self.assertInBody("No answer provided")
