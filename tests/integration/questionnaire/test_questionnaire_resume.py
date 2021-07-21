from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.questionnaire import SUBMIT_URL_PATH


class TestResume(IntegrationTestCase):
    def test_navigating_backwards(self):
        # If a user completes a block, then goes back and signs out, on re-authentication
        # they should resume on the first incomplete location
        self.launchSurvey("test_textfield")
        self.post({"name-answer": "Joe Bloggs"})

        # Go back to the first page
        self.get("/questionnaire/name-block")

        self.get("/sign-out")
        self.launchSurvey("test_textfield")

        # Check we are on the second page
        self.assertEqual(SUBMIT_URL_PATH, self.last_url)

    def test_sign_out_on_section_summary(self):
        # If a user completes a section and signs out on the section summary,
        # on re-authentication they should resume at the start of the next section
        self.launchSurvey("test_section_summary", display_address="test address")
        self.post({"insurance-type-answer": "Both"})
        self.post({"insurance-address-answer": "Address"})

        self.get("/sign-out")
        self.launchSurvey("test_section_summary", display_address="test address")

        # Check we are at the start of the next section
        self.assertInUrl("/questionnaire/house-type/")
