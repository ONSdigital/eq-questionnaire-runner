from tests.integration.integration_test_case import IntegrationTestCase


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

        # check we're on the thank you page and there's no sign out
        self.assertInUrl("thank-you")
        self.assertNotInBody("Sign out")

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
