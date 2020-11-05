from tests.integration.integration_test_case import IntegrationTestCase


class TestRenderCookiesBanner(IntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.launchSurvey("test_dropdown_mandatory")

    def test_cookies_banner_renders(self):
        self.assertInBody("Tell us whether you accept cookies")
