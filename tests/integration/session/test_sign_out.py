from tests.integration.integration_test_case import IntegrationTestCase


class TestSignOut(IntegrationTestCase):
    def test_not_signed_in_redirects_to_signed_out_page(self):
        self.get("/sign-out")
        self.assertInUrl("/signed-out")

    def test_no_account_service_log_out_url_redirects_to_signed_out_page(self):
        self.launchSurvey("test_textfield")
        self.get("/sign-out")
        self.assertInUrl("/signed-out")

    def test_account_service_log_out_url_redirects_to_url(self):
        self.launchSurvey(
            "test_textfield", account_service_log_out_url="https://localhost/logout"
        )
        self.get("/sign-out")
        self.assertInUrl("/logout")
