from unittest.mock import MagicMock

from app import settings
from app.cloud_tasks.exceptions import CloudTaskCreationFailed
from tests.integration.integration_test_case import IntegrationTestCase


class TestEmailConfirmation(IntegrationTestCase):
    def setUp(self):
        settings.CONFIRMATION_EMAIL_LIMIT = 2
        super().setUp()

    def _launch_and_complete_questionnaire(self):
        self.launchSurvey("test_confirmation_email")
        self.post({"answer_id": "Yes"})
        self.post()

    def test_bad_signature_confirmation_email_sent(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})

        # When I try to view the sent page with an incorrect email hash
        self.get("/submitted/confirmation-email/sent?email=bad-signature")

        # Then a BadRequest error is returned
        self.assertBadRequest()
        self.assertEqualPageTitle(
            "An error has occurred - Confirmation email test schema"
        )

    def test_missing_email_param_confirmation_email_sent(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})

        # When I try to view the sent page with no email param
        self.get("/submitted/confirmation-email/sent")

        # Then a BadRequest error is returned
        self.assertBadRequest()

    def test_bad_signature_confirm_email(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})

        # When I try to view the confirm email page with an incorrect email hash
        self.get("/submitted/confirmation-email/confirm?email=bad-signature")

        # Then a BadRequest error is returned
        self.assertBadRequest()
        self.assertEqualPageTitle(
            "An error has occurred - Confirmation email test schema"
        )

    def test_missing_email_param_confirm_email(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})

        # When I try to view the confirm email page with no email param
        self.get("/submitted/confirmation-email/confirm")

        # Then a BadRequest error is returned
        self.assertBadRequest()

    def test_confirm_email_with_confirmation_email_not_set(self):
        # Given I launch the test_thank_you_census_individual questionnaire, which doesn't have email confirmation set in the schema
        self.launchSurvey("test_thank_you_census_individual")
        self.post()
        self.post()

        # When I try to view the confirm email page
        self.get("/submitted/confirmation-email/confirm?email=email-hash")

        # Then I get routed to the thank you page
        self.assertInUrl("/submitted/thank-you/")
        self.assertNotInBody("Is this email address correct?")

    def test_confirmation_email_send_with_confirmation_email_not_set(self):
        # Given I launch the test_thank_you_census_individual questionnaire, which doesn't have email confirmation set in the schema
        self.launchSurvey("test_thank_you_census_individual")
        self.post()
        self.post()

        # When I try to view the confirmation email send page
        self.get("/submitted/confirmation-email/send")

        # Then I get routed to the thank you page
        self.assertInUrl("/submitted/thank-you/")
        self.assertNotInBody("Send a confirmation email")

    def test_bad_signature_confirmation_email_send(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()

        # When I try to view the confirm email page with an incorrect email hash
        self.get("/submitted/confirmation-email/send?email=bad-signature")

        # Then a BadRequest error is returned
        self.assertBadRequest()
        self.assertEqualPageTitle(
            "An error has occurred - Confirmation email test schema"
        )

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

    def test_census_themed_schema_with_confirmation_email_true(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()

        # When I am on the thank you page, Then there is an confirmation email form
        self.assertInUrl("/submitted/thank-you/")
        self.assertInBody("Get confirmation email")
        self.assertEqualPageTitle(
            "Thank you for completing the census - Confirmation email test schema"
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

    def test_confirm_email_missing_answer(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()

        # When I enter a valid email but don't provide an answer on the confirm email page
        self.post({"email": "email@example.com"})
        self.post()

        # Then I get an error on the confirm email page
        self.assertEqualPageTitle(
            "Error: Confirm your email address - Confirmation email test schema"
        )
        self.assertInBody("There is a problem with your answer")
        self.assertInBody("Select an answer")

    def test_confirm_email_no(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()

        # When I enter a valid email but answer no on the confirm email page
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "No, I need to change it"})

        # Then I get redirect to the confirmation email send page with the email pre-filled
        self.assertInUrl("/submitted/confirmation-email/send")
        self.assertInBody("Send a confirmation email")
        self.assertInBody("email@example.com")

    def test_confirm_email_yes(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()

        # When I enter a valid email submit and answer yes on the confirm email page
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})

        # Then I get confirmation that the email has been sent
        self.assertInUrl("confirmation-email/sent")
        self.assertInBody(
            'Make sure you <a href="/sign-out">leave this page</a> or close your browser if using a shared device'
        )

    def test_confirm_email_confirmation_email_limit_reached(
        self,
    ):
        # Given I launch and complete the test_confirmation_email questionnaire and reach the email confirmation limit
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})
        self.last_url
        self.post({"confirm-email": "Yes, send the confirmation email"})
        self.get("/submitted/confirmation-email/send/")
        self.post({"email": "email@example.com"})
        confirm_email_url = self.last_url
        self.post({"confirm-email": "Yes, send the confirmation email"})

        # When I try to access the confirm email page
        self.get(confirm_email_url)

        # Then I get routed to the thank you page
        self.assertInUrl("/submitted/thank-you/")

    def test_thank_you_page_confirmation_email_white_space(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()

        # When I enter a valid email which has leading and trailing whitespace
        self.post({"email": " email@example.com "})
        self.post({"confirm-email": "Yes, send the confirmation email"})

        # Then I get confirmation that the email has been sent
        self.assertInUrl("confirmation-email/sent")
        self.assertInBody("A confirmation email has been sent to email@example.com")

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
            "Error: Thank you for completing the census - Confirmation email test schema"
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
            "Enter an email address in a valid format, for example name@example.com"
        )

        self.assertEqualPageTitle(
            "Error: Thank you for completing the census - Confirmation email test schema"
        )

    def test_thank_you_email_invalid_tld(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()

        # When I enter an email with an invalid TLD and submit
        self.post({"email": "a@a.a"})

        # Then I get an error message on the thank you page
        self.assertInUrl("thank-you")
        self.assertInBody("There is a problem with this page")
        self.assertInBody(
            "Enter an email address in a valid format, for example name@example.com"
        )

    def test_thank_you_email_invalid_and_invalid_tld(self):
        # Given I launch and complete the test_confirmation_email questionnaire
        self._launch_and_complete_questionnaire()

        # When I enter an invalid email with an invalid TLD and submit
        self.post({"email": "a@@a.a"})

        # Then I get a single error message on the thank you page
        self.assertInUrl("thank-you")
        self.assertInBody("There is a problem with this page")
        self.assertInBody(
            "Enter an email address in a valid format, for example name@example.com"
        )
        self.assertNotInBody('data-qa="error-link-2"')

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
            "Error: Confirmation email - Confirmation email test schema"
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
            "Enter an email address in a valid format, for example name@example.com"
        )
        self.assertEqualPageTitle(
            "Error: Confirmation email - Confirmation email test schema"
        )

    def test_confirmation_email_page(self):
        # Given I launch and complete the test_confirmation_email questionnaire and submit with a valid email from the thank you page
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})

        # When I go to the confirmation email page and submit with a valid email
        self.get("/submitted/confirmation-email/send/")
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})

        # Then I get confirmation that the email has been sent
        self.assertInUrl("confirmation-email/sent")
        self.assertInBody("A confirmation email has been sent to email@example.com")

    def test_confirmation_email_page_white_space(self):
        # Given I launch and complete the test_confirmation_email questionnaire and submit with a valid email from the thank you page
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})

        # When I go to the confirmation email page and submit with a valid email which has leading and trailing whitespace
        self.get("/submitted/confirmation-email/send/")
        self.post({"email": " email@example.com "})
        self.post({"confirm-email": "Yes, send the confirmation email"})

        # Then I get confirmation that the email has been sent
        self.assertInUrl("confirmation-email/sent")
        self.assertInBody("A confirmation email has been sent to email@example.com")

    def test_send_another_email_link_is_not_present_on_thank_you_page_when_confirmation_limit_hit(
        self,
    ):
        # Given I launch and complete the test_confirmation_email questionnaire and submit with a valid email from the thank you page
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})

        # When I reach the limit of the number of confirmation emails able to be sent
        self.get("/submitted/thank-you/")
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})

        # Then I no longer see the option to send a confirmation email
        self.get("/submitted/thank-you/")
        self.assertInUrl("/submitted/thank-you/")
        self.assertNotInBody("Get confirmation email")

    def test_send_another_email_link_is_not_present_on_confirmation_sent_page_when_confirmation_limit_hit(
        self,
    ):
        # Given I launch and complete the test_confirmation_email questionnaire and submit with a valid email from the thank you page
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})

        # When I reach the limit of the number of confirmation emails able to be sent
        self.get("/submitted/confirmation-email/send/")
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})

        # Then I no longer see the option to send another confirmation email
        self.assertInUrl("confirmation-email/sent")
        self.assertNotInBody("send another confirmation email.")

    def test_visiting_send_another_email_page_redirects_to_thank_you_page_when_limit_exceeded(
        self,
    ):
        # Given I launch and complete the test_confirmation_email questionnaire and have reached the email limit
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})
        self.get("/submitted/confirmation-email/send/")
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})

        # When I try to access the send another email page
        self.get("/submitted/confirmation-email/send/")

        # Then I should be redirected to the thank you page
        self.assertInUrl("/submitted/thank-you/")
        self.assertNotInBody("Get confirmation email")

    def test_submitting_email_on_thank_you_page_reloads_the_page_when_limit_exceeded(
        self,
    ):
        # Given I launch and complete the test_confirmation_email questionnaire and have reached the email limit
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})
        self.assertInUrl("confirmation-email/sent")

        # Load the thank you page with the email form
        self.get("/submitted/thank-you/")
        # Set the new email limit so the limit will be reached on the next request
        self._application.config["CONFIRMATION_EMAIL_LIMIT"] = 1

        # When I try to submit another email
        self.post({"email": "email@example.com"})

        # Then the thank you page should be reloaded without the email form
        self.assertInUrl("/submitted/thank-you/")
        self.assertNotInBody("Get confirmation email")

    def test_submitting_email_on_send_another_email_page_redirect_to_thank_you_when_limit_exceeded(
        self,
    ):
        # Given I launch and complete the test_confirmation_email questionnaire and have reached the email limit
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})
        self.assertInUrl("confirmation-email/sent")

        # Load the send another email page with the email form
        self.get("/submitted/confirmation-email/send/")
        # Set the new email limit so the limit will be reached on the next request
        self._application.config["CONFIRMATION_EMAIL_LIMIT"] = 1

        # When I try to submit another email
        self.post({"email": "email@example.com"})

        # I should be redirected to the thank you page
        self.assertInUrl("/submitted/thank-you/")
        self.assertNotInBody("Get confirmation email")

    def test_500_publish_failed(self):
        publisher = self._application.eq["cloud_tasks"]
        publisher.create_task = MagicMock(side_effect=CloudTaskCreationFailed)

        # Given I launch and complete the test_confirmation_email questionnaire and submit with a valid email from the thank you page
        self._launch_and_complete_questionnaire()

        # When the email fulfilment request fails to publish
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})

        # Then an error page is shown
        self.assertEqualPageTitle(
            "Sorry, there was a problem sending the confirmation email - Confirmation email test schema"
        )
        self.assertInSelector(self.last_url, "p[data-qa=retry]")

    def test_attempting_to_deserialize_email_hash_from_different_session_fails(self):
        # Given I request a confirmation to my email address
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})

        # When I use the email hash in a different session
        query_params = self.last_url.split("?")[-1]
        self.exit()
        self._launch_and_complete_questionnaire()
        self.post({"email": "new-email@new-example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})
        self.get(f"/submitted/confirmation-email/sent?{query_params}")

        # Then a BadRequest error is returned
        self.assertBadRequest()
        self.assertEqualPageTitle(
            "An error has occurred - Confirmation email test schema"
        )

    def test_head_request_on_email_confirmation(self):
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})
        self.head(self.last_url)
        self.assertStatusOK()

    def test_head_request_on_email_send(self):
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "No, I need to change it"})
        self.head(self.last_url)
        self.assertStatusOK()

    def test_head_request_on_email_sent(self):
        self._launch_and_complete_questionnaire()
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})
        self.head(self.last_url)
        self.assertStatusOK()
