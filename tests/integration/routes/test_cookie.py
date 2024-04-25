from tests.integration.integration_test_case import IntegrationTestCase


class TestCookie(IntegrationTestCase):
    def test_cookie_contents(self):
        self.launchSurveyV2()
        cookie = self.getCookie()

        self.assertIsNotNone(cookie.get("_fresh"))
        self.assertIsNotNone(cookie.get("csrf_token"))
        self.assertIsNotNone(cookie.get("eq-session-id"))
        self.assertIsNotNone(cookie.get("expires_in"))
        self.assertIsNotNone(cookie.get("theme"))
        self.assertIsNotNone(cookie.get("title"))
        self.assertIsNotNone(cookie.get("survey_id"))
        self.assertIsNotNone(cookie.get("user_ik"))
        self.assertIsNotNone(cookie.get("account_service_base_url"))
        self.assertIsNotNone(cookie.get("language_code"))
        self.assertEqual(len(cookie), 10)

        self.assertIsNone(cookie.get("user_id"))
        self.assertIsNone(cookie.get("_permanent"))
