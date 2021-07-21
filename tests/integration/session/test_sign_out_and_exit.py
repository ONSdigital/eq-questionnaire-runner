from app.survey_config.business_config import BASE_URL
from tests.integration.integration_test_case import IntegrationTestCase

SIGN_OUT_URL_PATH = "/sign-out"
SIGNED_OUT_URL_PATH = "/signed-out"
ACCOUNT_SERVICE_LOG_OUT_URL = "http://localhost/logout"
ACCOUNT_SERVICE_LOG_OUT_URL_PATH = "/logout"


class TestSaveAndSignOut(IntegrationTestCase):
    # Test the behaviour when using Hub/No Hub

    def test_no_session_cookie_redirects_to_correct_location(self):
        for schema in ["test_textfield", "test_hub_and_spoke"]:
            with self.subTest(schema=schema):
                self.get(SIGN_OUT_URL_PATH, follow_redirects=False)
                self.assertInRedirect(BASE_URL)

    def test_no_account_service_log_out_url_redirects_to_signed_out_page(self):
        for schema in ["test_textfield", "test_hub_and_spoke"]:
            with self.subTest(schema=schema):
                self.launchSurvey(schema)
                self.get(SIGN_OUT_URL_PATH)
                self.assertInUrl(SIGNED_OUT_URL_PATH)

    def test_redirects_to_account_service_log_out_url_when_present(self):
        for schema in ["test_textfield", "test_hub_and_spoke"]:
            with self.subTest(schema=schema):
                self.launchSurvey(
                    schema, account_service_log_out_url=ACCOUNT_SERVICE_LOG_OUT_URL
                )
                self.get(SIGN_OUT_URL_PATH)
                self.assertInUrl(ACCOUNT_SERVICE_LOG_OUT_URL_PATH)

    def test_head_request_doesnt_sign_out(self):
        self.launchSurvey("test_textfield")
        self.head(SIGN_OUT_URL_PATH)
        self.assertStatusCode(302)
        self.get("/questionnaire/name-block")
        self.assertStatusOK()


class TestExitPostSubmissionTestCase(IntegrationTestCase):
    def _launch_and_submit_questionnaire(self, schema, **kwargs):
        self.launchSurvey(schema, **kwargs)
        self.post()
        self.post()
        self.assertInUrl("/thank-you")


class TestExitPostSubmissionWithFinalSummaryDefaultTheme(
    TestExitPostSubmissionTestCase
):
    def test_no_account_service_log_out_url_redirects_to_signed_out_page(self):
        self._launch_and_submit_questionnaire(schema="test_textfield")
        self.get(SIGN_OUT_URL_PATH)
        self.assertInUrl(SIGNED_OUT_URL_PATH)

    def test_redirects_to_account_service_log_out_url_when_present(self):
        self._launch_and_submit_questionnaire(
            schema="test_textfield",
            account_service_log_out_url=ACCOUNT_SERVICE_LOG_OUT_URL,
        )
        self.get(SIGN_OUT_URL_PATH)
        self.assertInUrl(ACCOUNT_SERVICE_LOG_OUT_URL_PATH)


class TestExitPostSubmissionWithHubDefaultTheme(IntegrationTestCase):
    def _launch_and_submit_questionnaire(self, schema, **kwargs):
        self.launchSurvey(schema, **kwargs)
        self.post({"household-relationships-answer": "No"})
        self.post()
        self.assertInUrl("/thank-you")

    def test_no_account_service_log_out_url_redirects_to_signed_out_page(self):
        self._launch_and_submit_questionnaire(
            schema="test_hub_section_required_and_enabled"
        )
        self.get(SIGN_OUT_URL_PATH, follow_redirects=False)
        self.assertInUrl(SIGN_OUT_URL_PATH)

    def test_redirects_to_account_service_log_out_url_when_present(self):
        self._launch_and_submit_questionnaire(
            schema="test_hub_section_required_and_enabled",
            account_service_log_out_url=ACCOUNT_SERVICE_LOG_OUT_URL,
        )
        self.get(SIGN_OUT_URL_PATH)
        self.assertInUrl(ACCOUNT_SERVICE_LOG_OUT_URL_PATH)
