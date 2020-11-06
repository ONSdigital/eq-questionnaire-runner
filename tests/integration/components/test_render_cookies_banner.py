from tests.integration.integration_test_case import IntegrationTestCase


class TestCookiesBanner(IntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.launchSurvey("test_dropdown_mandatory")

    def test_cookies_banner_contents(self):
        self.assertInBody("Tell us whether you accept cookies")
