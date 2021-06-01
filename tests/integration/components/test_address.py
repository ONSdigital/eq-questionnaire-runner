from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.questionnaire import SUBMIT_URL_PATH


class TestAddressFields(IntegrationTestCase):
    def setUp(self):
        super().setUp()
        # Given
        self.launchSurvey("test_address")

    def test_mandatory_address_line_1_is_mandatory(self):
        # When
        self.post({})

        # Then
        self.assertInBody("Enter an address")

    def test_empty_address_field_are_not_displayed_on_summary(self):
        # When
        self.post(
            {
                "address-mandatory-line1": "7 Evelyn Street",
                "address-mandatory-postcode": "CF63 4JG",
            }
        )
        self.post({})
        self.post({})

        # Then
        self.assertInBody("7 Evelyn Street<br/>CF63 4JG")

    def test_address_fields_are_filled_in_when_revisiting_the_page(self):
        # Given
        self.post(
            {
                "address-mandatory-line1": "7 Evelyn Street",
                "address-mandatory-postcode": "CF63 4JG",
            }
        )
        self.post({})
        self.post({})
        self.assertInUrl(SUBMIT_URL_PATH)

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
        self.post({})

        # Then
        self.assertInBody("No answer provided")


class TestLookupAddressFields(IntegrationTestCase):
    # As these are integration tests, we are testing the behaviour of
    # address lookups without Javascript
    def setUp(self):
        super().setUp()
        # Given
        self.launchSurvey("test_address_lookups")

    def test_address_fields_exist(self):
        # Then
        self.assertInBody("Address line 1")

    def test_address_line_1_is_mandatory(self):
        # When
        self.post({})

        # Then
        self.assertInBody("Enter an address")

    def test_address_fields_are_populated_in_when_revisiting_the_page(self):
        # Given
        self.post(
            {
                "address-mandatory-line1": "7 Evelyn Street",
                "address-mandatory-postcode": "CF63 4JG",
                "address-mandatory-uprn": "123456789",
            }
        )
        self.post({})
        self.assertInUrl(SUBMIT_URL_PATH)

        # When
        self.get("questionnaire/address-block-mandatory/")

        # Then
        self.assertInBody("7 Evelyn Street")
        self.assertInBody("CF63 4JG")
        self.assertInBody("123456789")

    def test_uprn_field_not_displayed_on_summary(self):
        # When
        self.post(
            {
                "address-mandatory-line1": "first address",
                "address-mandatory-uprn": "123456789",
            }
        )

        self.post({})

        # Then
        self.assertNotInBody("123456789")

    def test_auth_token_not_in_page(self):
        self.assertNotInBody("data-authorization-token")

    def test_auth_token_in_page(self):
        self.test_app.config["ADDRESS_LOOKUP_API_URL"] = "https://address-lookup-api"
        self.test_app.config["ADDRESS_LOOKUP_API_AUTH_ENABLED"] = True
        # When
        self.get("questionnaire/address-block-mandatory/")
        # Then
        auth_token = (
            self.getHtmlSoup()
            .select(f"#address-mandatory-autosuggest-container")[0]
            .get("data-authorization-token")
        )
        assert auth_token
        assert len(auth_token.split(".")) == 3
