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

    def test_google_analytics_code_and_credentials_are_present(self):
        self.launchSurvey("test_feedback")
        self._client.set_cookie(
            "localhost", key="ons_cookie_policy", value="'usage':true"
        )
        self.get("/questionnaire/feedback/")
        self.assertStatusOK()
        self.assertInHead("gtm.start")
        self.assertInHead(
            'dataLayer = [{"form_type": "H", "survey_id": "0", "title": "Feedback test schema"}]'
        )
        self.assertInBody("https://www.googletagmanager.com")
        self.assertInHead(settings.EQ_GOOGLE_TAG_MANAGER_AUTH)
        self.assertInHead(settings.EQ_GOOGLE_TAG_MANAGER_ID)

    def test_google_analytics_data_layer_has_no_null_fields(self):
        self.launchSurvey("test_textfield")
        self._client.set_cookie(
            "localhost", key="ons_cookie_policy", value="'usage':true"
        )
        self.get("/questionnaire/name-block/")
        self.assertStatusOK()
        self.assertInHead("gtm.start")
        # form_type is empty so should not be present
        self.assertInHead(
            'dataLayer = [{"survey_id": "001", "title": "Other input fields"}]'
        )

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
