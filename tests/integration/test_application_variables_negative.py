from app import settings
from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationVariablesNegative(IntegrationTestCase):
    def setUp(self):
        settings.EQ_ENABLE_LIVE_RELOAD = False
        super().setUp()

    def test_livereload_script_not_rendered(self):
        self.launchSurveyV2(schema_name="test_textfield")
        self.assertStatusOK()
        self.assertFalse("__bs_script__" in self.getResponseData())
