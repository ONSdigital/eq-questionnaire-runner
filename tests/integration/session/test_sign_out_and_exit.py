from app.settings import ACCOUNT_SERVICE_BASE_URL as DEFAULT_ACCOUNT_SERVICE_BASE_URL
from tests.integration.integration_test_case import IntegrationTestCase

SIGN_OUT_URL_PATH = "/sign-out"
SIGNED_OUT_URL_PATH = "/signed-out"
SESSION_EXPIRED_PATH = "/session-expired"
ACCOUNT_SERVICE_BASE_URL = "http://localhost"
ACCOUNT_SERVICE_LOG_OUT_URL_PATH = "/sign-in/logout"
ACCOUNT_SERVICE_LOG_OUT_URL = (
    f"{ACCOUNT_SERVICE_BASE_URL}{ACCOUNT_SERVICE_LOG_OUT_URL_PATH}"
)
DEFAULT_ACCOUNT_SERVICE_LOG_OUT_URL = (
    f"{DEFAULT_ACCOUNT_SERVICE_BASE_URL}{ACCOUNT_SERVICE_LOG_OUT_URL_PATH}"
)


class TestSaveAndSignOut(IntegrationTestCase):
    def test_sign_out_button_link(self):
        self.launchSurvey("test_textfield")
        self.assertEqual(
            "/sign-out?internal_redirect=True", self.getSignOutButton()["href"]
        )

    def test_sign_out_url(self):
        self.launchSurvey("test_textfield")
        self.saveAndSignOut()
        self.assertInRedirect(SIGNED_OUT_URL_PATH)

    def test_sign_out_button_text(self):
        self.launchSurvey("test_textfield")
        self.assertEqual("Save and exit survey", self.getSignOutButton().text.strip())

    def test_sign_out_button_displayed_pre_submission(self):
        self.launchSurvey("test_textfield")
        self.assertIsNotNone(self.getSignOutButton())

    def test_no_session_cookie_redirects_to_default_account_service_log_out_url(self):
        self.deleteCookie()
        self.get(SIGN_OUT_URL_PATH, follow_redirects=False)
        self.assertInRedirect(DEFAULT_ACCOUNT_SERVICE_LOG_OUT_URL)

    def test_no_session_cookie_signed_out_redirects_to_session_expiry(self):
        self.deleteCookie()
        self.get(SIGNED_OUT_URL_PATH, follow_redirects=False)
        self.assertInRedirect(SESSION_EXPIRED_PATH)

    # Test the behaviour when using Hub/No Hub
    def test_redirects_to_account_service_log_out_url_using_base_url_from_claims(self):
        for schema in ["test_textfield", "test_hub_and_spoke"]:
            with self.subTest(schema=schema):
                self.launchSurvey(schema, account_service_url=ACCOUNT_SERVICE_BASE_URL)
                self.signOut()
                self.assertInRedirect(ACCOUNT_SERVICE_LOG_OUT_URL)

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
    def test_redirects_to_account_service_log_out_url_using_base_url_from_claims(self):
        self._launch_and_submit_questionnaire(
            schema="test_textfield",
            account_service_url=ACCOUNT_SERVICE_BASE_URL,
        )
        self.signOut()
        self.assertInRedirect(ACCOUNT_SERVICE_LOG_OUT_URL)


class TestExitPostSubmissionWithHubDefaultTheme(IntegrationTestCase):
    def _launch_and_submit_questionnaire(self, schema, **kwargs):
        self.launchSurvey(schema, **kwargs)
        self.post({"household-relationships-answer": "No"})
        self.post()
        self.assertInUrl("/thank-you")

    def test_redirects_to_account_service_log_out_url_using_base_url_from_claims(self):
        self._launch_and_submit_questionnaire(
            schema="test_hub_section_required_and_enabled",
            account_service_url=ACCOUNT_SERVICE_BASE_URL,
        )
        self.signOut()
        self.assertInRedirect(ACCOUNT_SERVICE_LOG_OUT_URL)


# class TestCensusSignOut(IntegrationTestCase):
#     def setUp(self):
#         self._set_up_app(setting_overrides={"SURVEY_TYPE": "census"})
#
#     def test_sign_out_url(self):
#         self.launchSurvey(schema_name="test_individual_response")
#         self.saveAndSignOut()
#         self.assertInRedirect(SIGNED_OUT_URL_PATH)
#
#     # def test_sign_out_button_text(self):
#     #     self.launchSurvey(schema_name="test_individual_response")
#     #     self.assertEqual(
#     #         "Save and complete later", self.getSignOutButton().text.strip()
#     #     )
#
#     # def test_no_session_cookie_redirects_to_default_account_service_log_out_url(self):
#     #     self.launchSurvey(schema_name="test_individual_response")
#     #     self.assertInBody("Save and sign out")
#     #
#     #     self.deleteCookie()
#     #     self.signOut()
#     #
#     #     self.assertInRedirect("census.gov.uk")
