from tests.integration.integration_test_case import IntegrationTestCase


class TestEmailConfirmation(IntegrationTestCase):
    def test_thank_you_page_get_not_allowed(self):
        # Given I launch the test_confirmation_email questionnaire
        self.launchSurvey("test_confirmation_email")

        # When I try to view the thank you page without completing the questionnaire
        self.get("/submitted/thank-you/")

        # Then I get shown a 404 error
        self.assertStatusNotFound()

    def test_thank_you_page_post_not_allowed(self):
        # Given I launch the test_confirmation_email questionnaire
        self.launchSurvey("test_confirmation_email")

        # When I try to POST to the thank you page without completing the questionnaire
        self.post(url="/submitted/thank-you/")

        # Then I get shown a 404 error
        self.assertStatusNotFound()

    def test_email_confirmation_page_get_not_allowed(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()

        # When I try to view the confirmation email sent page without sending an email
        self.get("/submitted/confirmation-email/sent")

        # Then I get shown a 404 error
        self.assertStatusNotFound()

    def test_confirmation_email_page_get_not_allowed(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()

        # When I try to view the confirmation email page without sending an email from the thank you page first
        self.get("/submitted/confirmation-email/send")

        # Then I get shown a 404 error
        self.assertStatusNotFound()

    def test_confirmation_email_page_post_not_allowed(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()

        # When I try to POST to the confirmation email page without sending an email from the thank you page first
        self.post(url="/submitted/confirmation-email/send/")

        # Then I get shown a 404 error
        self.assertStatusNotFound()

    def test_census_themed_schema_with_confirmation_email_true(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()

        # When I am on the thank you page, Then there is an confirmation email form
        self.assertInUrl("/submitted/thank-you/")
        self.assertInBody("Get confirmation email")
        self.assertEqualPageTitle(
            "Thank you - Census 2021 - Confirmation email test schema"
        )

    def test_census_themed_schema_with_confirmation_email_not_set(self):
        # Given I launch the test_thank_you_census_individual questionnaire, which doesn't have email confirmation set in the schema
        self.launchSurvey("test_thank_you_census_individual")

        # When I complete the questionnaire
        self.post()
        self.post()

        # Then on the thank you page I don't get a confirmation email form
        self.assertInUrl("/submitted/thank-you/")
        self.assertNotInBody("Get confirmation email")

    def test_default_themed_schema_with_confirmation_email_not_set(self):
        # Given I launch the test_checkbox questionnaire, which doesn't have email confirmation set in the schema
        self.launchSurvey("test_checkbox")

        # When I complete the questionnaire
        self.post({"mandatory-checkbox-answer": "Tuna"})
        self.post({"non-mandatory-checkbox-answer": "Pineapple"})
        self.post({"single-checkbox-answer": "Estimate"})
        self.post()

        # Then on the thank you page I don't get a confirmation email form
        self.assertInUrl("/submitted/thank-you/")
        self.assertNotInBody("Get confirmation email")

    def test_thank_you_page_confirmation_email(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()

        # When I enter a valid email and submit
        self.post({"email": "email@example.com"})

        # Then I get confirmation that the email has been sent
        self.assertInUrl("confirmation-email/sent")
        self.assertInBody("A confirmation email has been sent")

    def test_thank_you_missing_email(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()

        # When I fail to enter an email and submit
        self.post()

        # Then I get an error message on the thank you page
        self.assertInUrl("/submitted/thank-you/")
        self.assertInBody("There is a problem with this page")
        self.assertInBody("Enter an email address")
        self.assertEqualPageTitle(
            "Error: Thank you - Census 2021 - Confirmation email test schema"
        )

    def test_thank_you_incorrect_email_format(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()

        # When I fail to enter an email in the correct format and submit
        self.post({"email": "incorrect-format"})

        # Then I get an error message on the thank you page
        self.assertInUrl("thank-you")
        self.assertInBody("There is a problem with this page")
        self.assertInBody(
            "Enter an email in a valid format, for example name@example.com"
        )

        self.assertEqualPageTitle(
            "Error: Thank you - Census 2021 - Confirmation email test schema"
        )

    def test_confirmation_email_page_accessible_after_email_sent_from_thank_you(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()

        # When I enter a valid email and submit
        self.post({"email": "email@example.com"})

        # Then I can access the email confirmation page
        self.get("/submitted/confirmation-email/send")
        self.assertInBody("Send another confirmation email")
        self.assertEqualPageTitle(
            "Confirmation email - Census 2021 - Confirmation email test schema"
        )

    def test_confirmation_email_page_missing_email(self):
        # Given I launch and complete the test_confirmation_email questionnaire and submit with a valid email from the thank you page
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})

        # When I go to the confirmation email page and submit, but fail to enter an email
        self.get("/submitted/confirmation-email/send/")
        self.post()

        # Then I get an error message on the confirmation email page
        self.assertInUrl("/submitted/confirmation-email/send/")
        self.assertInBody("There is a problem with this page")
        self.assertInBody("Enter an email address")
        self.assertEqualPageTitle(
            "Error: Confirmation email - Census 2021 - Confirmation email test schema"
        )

    def test_confirmation_email_page_incorrect_email_format(self):
        # Given I launch and complete the test_confirmation_email questionnaire and submit with a valid email from the thank you page
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})

        # When I go to the confirmation email page and submit, but fail to enter an email in the correct format
        self.get("/submitted/confirmation-email/send/")
        self.post({"email": "invalid-format"})

        # Then I get an error message on the confirmation email page
        self.assertInUrl("/submitted/confirmation-email/send/")
        self.assertInBody("There is a problem with this page")
        self.assertInBody(
            "Enter an email in a valid format, for example name@example.com"
        )
        self.assertEqualPageTitle(
            "Error: Confirmation email - Census 2021 - Confirmation email test schema"
        )

    def test_confirmation_email_page(self):
        # Given I launch and complete the test_confirmation_email questionnaire and submit with a valid email from the thank you page
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})

        # When I go to the confirmation email page and submit with a valid email
        self.get("/submitted/confirmation-email/send/")
        self.post({"email": "email@example.com"})

        # Then I get confirmation that the email has been sent
        self.assertInUrl("confirmation-email/sent")
        self.assertInBody("A confirmation email has been sent to email@example.com")

    def _launch_and_complete_questionnaire(self):
        self.launchSurvey("test_confirmation_email")
        self.post({"answer_id": "Yes"})
        self.post()
