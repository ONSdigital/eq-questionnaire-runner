from tests.integration.integration_test_case import IntegrationTestCase


class TestSchemaThemeThankYou(IntegrationTestCase):
    def test_census_individual(self):
        self.launchSurvey(
            "test_thank_you_census_individual",
            display_address="68 Abingdon Road, Goathill",
        )
        self.post({"individual-confirmation": "Yes"})
        self.post()
        self.assertInBody("Thank you for completing your census")
        self.assertInBody(
            "Your individual census has been submitted for <strong>68 Abingdon Road, Goathill</strong>"
        )
        self.assertInBody(
            'Make sure you <a href="/sign-out">leave this page</a> or close your browser if using a shared device'
        )

    def test_census_household(self):
        self.launchSurvey(
            "test_thank_you_census_household",
            display_address="68 Abingdon Road, Goathill",
        )
        self.post({"household-confirmation": "Yes"})
        self.post()
        self.assertInBody("Thank you for completing the census")
        self.assertInBody(
            "Your census has been submitted for the household at <strong>68 Abingdon Road, Goathill</strong>"
        )

    def test_census_communal_establishment(self):
        self.launchSurvey(
            "test_thank_you_census_communal_establishment",
            display_address="68 Abingdon Road, Goathill",
        )
        self.post({"communal-establishment-confirmation": "Yes"})
        self.post()
        self.assertInBody("Thank you for completing the census")
        self.assertInBody(
            "Your census has been submitted for the accommodation at <strong>68 Abingdon Road, Goathill</strong>"
        )

    def test_census_theme_schema_name_not_mapped_to_census_type(self):
        self.launchSurvey("test_feedback_email_confirmation")
        self.post({"schema-confirmation-answer": "Yes"})
        self.post()
        self.assertInBody("Thank you for completing the survey")
