from tests.integration.integration_test_case import IntegrationTestCase


class TestEmailConfirmation(IntegrationTestCase):


    def test_email_confirmation_from_thank_you(self):
        self.launchSurvey("test_email_confirmation")
        self.post({"answer_id": "Yes"})
        self.post()
        self.assertInBody("Get confirmation email")
        self.post({"email": "email@example.com"})
        self.assertInBody("A confirmation email has been sent to")

    def test_thank_you_missing_email(self):
        self.launchSurvey("test_email_confirmation")
        self.post({"answer_id": "Yes"})
        self.post()
        self.assertInBody("Get confirmation email")
        self.post({"email": "email@example.com"})
        self.assertInBody("There is a problem with your answer")
        self.assertInBody("Enter an email address to continue")

    def test_thank_you_incorrect_email_format(self):
        self.launchSurvey("test_email_confirmation")
        self.post({"answer_id": "Yes"})
        self.post()
        self.assertInBody("Get confirmation email")
        self.post({"email": "email@example.com"})
        self.assertInBody("There is a problem with your answer")
        self.assertInBody("Enter an email in a valid format, for example name@example.com")


    def test_thank_you_page_post_not_allowed(self):
        self.post(url="/submitted/thank-you/")
        self.assertStatusCode(405)

    def test_email_confirmation_page_post_not_allowed(self):
        self.post(url="/submitted/email-confirmation/")
        self.assertStatusCode(405)

    def test_email_confirmation_page_get_not_allowed(self):
        self.get(url="/submitted/email-confirmation/")
        self.assertStatusCode(405)

    def test_email_confirmation_sent_page_get_not_allowed(self):
        self.post(url="/submitted/email-confirmation-sent/")
        self.assertStatusCode(405)
