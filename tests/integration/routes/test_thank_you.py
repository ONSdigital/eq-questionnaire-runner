from tests.integration.integration_test_case import IntegrationTestCase
import pytest
ACCOUNT_SERVICE_TODO_PATH = "/surveys/todo"


class TestThankYou(IntegrationTestCase):
    def test_thank_you_page_no_sign_out(self):
        self.launchSurvey("test_currency")

        # We fill in our answers
        form_data = {
            "answer": "12",
            "answer-usd": "345",
            "answer-eur": "67.89",
            "answer-jpy": "0",
        }

        # We submit the form
        self.post(form_data)

        # Submit answers
        self.post()

        # check we're on the thank you page and there's no sign out button
        self.assertInUrl("thank-you")
        self.assertIsNone(self.getSignOutButton())

    def test_can_switch_language_on_thank_you_page(self):
        self.launchSurvey("test_language")
        self.post()
        # We fill in our answers
        self.post({"first-name": "Kevin", "last-name": "Bacon"})
        self.post(
            {
                "date-of-birth-answer-day": 1,
                "date-of-birth-answer-month": 2,
                "date-of-birth-answer-year": 1999,
            }
        )
        self.post({"number-of-people-answer": 0})
        self.post({"confirm-count": "Yes"})

        # Submit answers
        self.post()

        # Ensure we're on the thank you page
        self.assertInUrl("thank-you")

        # Ensure translation is as expected using language toggle links
        # Toggle link text displays 'English' when in Welsh, and 'Cymraeg' when in English
        self.assertNotInBody("English")
        self.assertInBody("Cymraeg")

        # Switch language to Welsh
        self.get(f"{self.last_url}?language_code=cy")
        self.assertInUrl("?language_code=cy")

        # Ensure translation is now in Welsh
        self.assertInBody("English")
        self.assertNotInBody("Cymraeg")

    def test_head_request_on_thank_you(self):
        self.launchSurvey("test_confirmation_email")
        self.post()
        self.post()
        self.head("/submitted/thank-you")
        self.assertStatusOK()

    def test_options_request_post_submission_before_request(self):
        self.launchSurvey("test_confirmation_email")
        self.post()
        self.post()

        with self.assertLogs() as logs:
            self.options("/submitted/thank-you")
            self.assertStatusOK()

        for output in logs.output:
            self.assertNotIn("questionnaire request", output)

    @pytest.mark.xfail(reason="DS changes pending")
    def test_default_guidance(self):
        self.launchSurvey("test_textfield")
        self.post({"name-answer": "Adam"})
        self.post()

        self.assertInUrl("thank-you")
        self.assertInBody("Your answers will be processed in the next few weeks.")

    @pytest.mark.xfail(reason="DS changes pending")
    def test_custom_guidance(self):
        self.launchSurvey("test_thank_you")
        self.post({"answer": "Yes"})
        self.post()

        self.assertInUrl("thank-you")
        self.assertInBody("This survey was important.")
        self.assertInBody('<a href="">Important link</a>')

    @pytest.mark.xfail(reason="DS changes pending")
    def test_back_to_surveys_link_on_thank_you(self):
        self.launchSurvey("test_thank_you")
        self.post({"answer": "Yes"})
        self.post()

        self.assertInUrl("thank-you")
        self.assertInBody("Back to surveys")
        self.assertInBody(ACCOUNT_SERVICE_TODO_PATH)
