from app import settings
from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationVariables(IntegrationTestCase):
    def setUp(self):
        settings.EQ_ENABLE_LIVE_RELOAD = True
        settings.EQ_GOOGLE_TAG_MANAGER_ID = "TestId"
        settings.EQ_GOOGLE_TAG_MANAGER_AUTH = "TestAuth"
        super().setUp()

    def tearDown(self):
        super().tearDown()
        settings.EQ_ENABLE_LIVE_RELOAD = False
        settings.EQ_GOOGLE_TAG_MANAGER_ID = None
        settings.EQ_GOOGLE_TAG_MANAGER_AUTH = None

    def test_google_analytics_code_is_present(self):
        self.launchSurvey("test_textfield")
        self._client.set_cookie(
            "localhost", key="ons_cookie_policy", value="'usage':true"
        )
        self.get("/questionnaire/name-block/")
        self.assertStatusOK()
        self.assertInHead("gtm.start")
        self.assertInHead("dataLayer = []")
        self.assertInBody("https://www.googletagmanager.com")

    def test_google_analytics_data_layer_is_set_to_nisra_false(self):
        self.launchSurvey("test_thank_you_census_individual")
        self._client.set_cookie(
            "localhost", key="ons_cookie_policy", value="'usage':true"
        )
        self.get("/questionnaire/individual-confirmation/")
        self.assertStatusOK()
        self.assertInHead("gtm.start")
        self.assertInHead('dataLayer = [{"nisra": false}]')

    def test_livereload_script_rendered(self):
        self.launchSurvey("test_textfield")
        self.assertStatusOK()
        self.assertTrue("__bs_script__" in self.getResponseData())
