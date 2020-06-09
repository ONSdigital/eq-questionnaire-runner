from tests.integration.integration_test_case import IntegrationTestCase


class TestSignOut(IntegrationTestCase):
    def test_sign_out_not_signed_in_redirects_to_signed_out_page(self):
        self.get("/sign-out")
        self.assertInUrl("/signed-out")

    def test_sign_out_without_log_out_url_redirects_to_signed_out_page(self):
        self.launchSurvey("test_textfield")
        self.get("/sign-out")
        self.assertInUrl("/signed-out")

    def test_sign_out_with_log_out_url_redirects_to_log_out_url(self):
        self.launchSurvey(
            "test_textfield", account_service_log_out_url="https://localhost/logout"
        )
        self.get("/sign-out")
        self.assertInUrl("/logout")

    def test_sign_out_after_navigating_backwards(self):
        # If a user completes a block, then goes back and signs out, on re-authentication
        # they should resume on the first incomplete location
        self.launchSurvey("test_textfield")
        self.post({"name-answer": "Joe Bloggs"})

        # Go back to the first page
        self.get("/questionnaire/name-block")

        self.get("/sign-out")
        self.launchSurvey("test_textfield")

        # Check we are on the second page
        self.assertEqual("/questionnaire/summary/", self.last_url)

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
