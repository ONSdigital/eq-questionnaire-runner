from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.questionnaire import SUBMIT_URL_PATH, THANK_YOU_URL_PATH


class TestResume(IntegrationTestCase):
    def test_navigating_backwards(self):
        # Given I submit the first page
        self.launchSurveyV2(schema_name="test_textfield")
        self.post({"name-answer": "Joe Bloggs"})

        # When I go back to the first page, sign out and then resume
        self.get("/questionnaire/name-block")
        self.signOut()
        self.launchSurveyV2(schema_name="test_textfield")

        # Then I should resume on the first incomplete location
        self.assertEqual(SUBMIT_URL_PATH, self.last_url)

    def test_sign_out_on_section_summary(self):
        # Given I complete the first section
        self.launchSurveyV2(
            schema_name="test_section_summary", display_address="test address"
        )
        self.post({"insurance-type-answer": "Both"})
        self.post({"insurance-address-answer": "Address"})
        self.post({"listed-answer": "No"})

        # When I sign out and then resume
        self.signOut()
        self.launchSurveyV2(
            schema_name="test_section_summary", display_address="test address"
        )

        # Then I should resume on the start of the next section
        self.assertInUrl("/questionnaire/house-type/")

    def test_after_submission(self):
        # Given I complete the questionnaire and submit
        self.launchSurveyV2(schema_name="test_textfield")
        self.post({"name-answer": "Joe Bloggs"})
        self.post()

        # When I resume
        self.launchSurveyV2(schema_name="test_textfield")

        # Then I should resume on the thank you page
        self.assertInUrl(THANK_YOU_URL_PATH)
