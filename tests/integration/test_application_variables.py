from app import settings
from app.utilities.json import json_loads
from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationVariables(IntegrationTestCase):
    def setUp(self):
        settings.EQ_ENABLE_LIVE_RELOAD = True
        settings.EQ_GOOGLE_TAG_ID = "TestId"
        super().setUp()

    def tearDown(self):
        super().tearDown()
        settings.EQ_ENABLE_LIVE_RELOAD = False
        settings.EQ_GOOGLE_TAG_ID = None

    def test_google_analytics_code_and_credentials_are_present(self):
        self.launchSurveyV2(schema_name="test_feedback", roles=["dumper"])
        self.get("/dump/debug")
        actual = json_loads(self.getResponseData())
        self._client.set_cookie(
            domain="localhost", key="ons_cookie_policy", value="'usage':true"
        )
        self.get("/questionnaire/feedback/")
        self.assertStatusOK()
        self.assertInHead(
            f'"form_type": "H", "survey_id": "0", "title": "Feedback test schema", "tx_id": "{actual["METADATA"]["tx_id"]}"'
        )
        self.assertInHead("https://www.googletagmanager.com")
        self.assertInHead(settings.EQ_GOOGLE_TAG_ID)

    def test_google_analytics_data_layer_has_no_null_fields(self):
        self.launchSurveyV2(schema_name="test_textfield", roles=["dumper"])
        self.get("/dump/debug")
        actual = json_loads(self.getResponseData())
        self._client.set_cookie(
            domain="localhost", key="ons_cookie_policy", value="'usage':true"
        )
        self.get("/questionnaire/name-block/")
        self.assertStatusOK()
        # form_type is empty so should not be present
        self.assertInHead(
            f'"survey_id": "001", "title": "Other input fields", "tx_id": "{actual["METADATA"]["tx_id"]}"'
        )

    def test_livereload_script_rendered(self):
        self.launchSurveyV2(schema_name="test_textfield")
        self.assertStatusOK()
        self.assertTrue("__bs_script__" in self.getResponseData())
