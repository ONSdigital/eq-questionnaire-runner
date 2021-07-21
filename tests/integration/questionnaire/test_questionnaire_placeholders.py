from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.questionnaire import SUBMIT_URL_PATH


class TestPlaceholders(IntegrationTestCase):
    def test_title_placeholders_rendered_in_summary(self):
        self.launchSurvey(
            "test_placeholder_full", display_address="68 Abingdon Road, Goathill"
        )
        self.assertInBody("Please enter a name")
        self.post({"first-name": "Kevin", "last-name": "Bacon"})

        self.assertInBody("What is Kevin Bacon’s date of birth?")

        self.post(
            {
                "date-of-birth-answer-day": 1,
                "date-of-birth-answer-month": 2,
                "date-of-birth-answer-year": 1999,
            }
        )

        self.post(
            {"confirm-date-of-birth-answer-proxy": "Yes, {person_name} is {age} old."}
        )

        self.post(
            {"checkbox-answer": ["{household_address}", "7 Evelyn Street, Barry"]}
        )

        self.assertInUrl(SUBMIT_URL_PATH)
        self.assertInBody("What is Kevin Bacon’s date of birth?")
        self.assertInBody("68 Abingdon Road, Goathill")

    def test_placeholders_rendered_in_pages(self):
        self.launchSurvey("test_placeholder_transform")
        self.assertInBody("Please enter the total retail turnover")
        self.post({"total-retail-turnover-answer": 2000})

        self.assertInBody(
            "Of the <em>£2,000.00</em> total retail turnover, what was the value of internet sales?"
        )

        self.post({"total-retail-turnover-internet-sales-answer": 3000})

        self.post({"total-items-answer": 2})

        self.assertInBody("Do you want to add <em>a 3rd</em> item?")

        self.post({"add-item-question": "Yes"})

        self.assertInUrl(SUBMIT_URL_PATH)
        self.assertInBody("Please enter the total retail turnover")
        self.assertInBody("Please enter the value of internet sales")
        self.assertInBody("Please enter the number of items")
        self.assertInBody("Do you want to add a 3rd item?")

    def test_placeholder_address_selector_rendered_in_page(self):
        self.launchSurvey("test_address")

        self.post(
            {
                "address-mandatory-line1": "7 Evelyn Street",
                "address-mandatory-postcode": "CF63 4JG",
            }
        )
        self.post({})

        self.assertInBody(
            "Please confirm the first line of your address is 7 Evelyn Street"
        )
