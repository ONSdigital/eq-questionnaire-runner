from app.helpers.template_helpers import (
    CENSUS_CY_BASE_URL,
    CENSUS_EN_BASE_URL,
    CENSUS_NIR_BASE_URL,
)
from tests.integration.integration_test_case import IntegrationTestCase

SIGN_OUT_URL_PATH = "/sign-out"
SIGNED_OUT_URL_PATH = "/signed-out"
ACCOUNT_SERVICE_LOG_OUT_URL = "http://localhost/logout"
ACCOUNT_SERVICE_LOG_OUT_URL_PATH = "/logout"


class TestSaveAndSignOut(IntegrationTestCase):
    # Test the behaviour when using Hub/No Hub

    def test_no_session_cookie_redirects_to_census_home_page(self):
        for schema in ["test_textfield", "test_hub_and_spoke"]:
            with self.subTest(schema=schema):
                self.get(SIGN_OUT_URL_PATH, follow_redirects=False)
                self.assertInRedirect(CENSUS_EN_BASE_URL)

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


class TestExitPostSubmissionWithFinalSummaryCensusTheme(TestExitPostSubmissionTestCase):
    def test_no_account_service_log_out_url_redirects_to_census_home_page(self):
        self._launch_and_submit_questionnaire(schema="test_thank_you_census_individual")
        self.get(SIGN_OUT_URL_PATH, follow_redirects=False)
        self.assertInRedirect(CENSUS_EN_BASE_URL)

    def test_redirects_to_census_home_page_and_not_account_service_log_out_url(self):
        self._launch_and_submit_questionnaire(
            schema="test_thank_you_census_individual",
            account_service_log_out_url=ACCOUNT_SERVICE_LOG_OUT_URL,
        )
        self.get(SIGN_OUT_URL_PATH, follow_redirects=False)
        self.assertInRedirect(CENSUS_EN_BASE_URL)

    def test_redirects_to_census_cy_home_page_when_submitting_in_welsh(self):
        self._launch_and_submit_questionnaire(
            schema="test_thank_you_census_individual",
            account_service_log_out_url=ACCOUNT_SERVICE_LOG_OUT_URL,
            language_code="cy",
        )
        self.get(SIGN_OUT_URL_PATH, follow_redirects=False)
        self.assertInRedirect(CENSUS_CY_BASE_URL)

    def test_redirects_to_census_nir_home_page_when_submitting_nir_theme(self):
        self._launch_and_submit_questionnaire(
            schema="test_thank_you_census_individual",
            account_service_log_out_url=ACCOUNT_SERVICE_LOG_OUT_URL,
        )

        with self.session as cookie_session:
            cookie_session["theme"] = "census-nisra"

        self.get(SIGN_OUT_URL_PATH, follow_redirects=False)
        self.assertInRedirect(CENSUS_NIR_BASE_URL)


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


class TestExitPostSubmissionWithHubCensusTheme(TestExitPostSubmissionTestCase):
    def test_no_account_service_log_out_url_redirects_to_census_home_page(self):
        self._launch_and_submit_questionnaire(schema="test_thank_you_census_household")
        self.get(SIGN_OUT_URL_PATH, follow_redirects=False)
        self.assertInRedirect(CENSUS_EN_BASE_URL)

    def test_redirects_to_census_home_page_and_not_account_service_log_out_url(self):
        self._launch_and_submit_questionnaire(
            schema="test_thank_you_census_household",
            account_service_log_out_url=ACCOUNT_SERVICE_LOG_OUT_URL,
        )
        self.get(SIGN_OUT_URL_PATH, follow_redirects=False)
        self.assertInRedirect(CENSUS_EN_BASE_URL)

    def test_redirects_to_census_cy_home_page_when_submitting_in_welsh(self):
        self._launch_and_submit_questionnaire(
            schema="test_thank_you_census_household",
            account_service_log_out_url=ACCOUNT_SERVICE_LOG_OUT_URL,
            language_code="cy",
        )
        self.get(SIGN_OUT_URL_PATH, follow_redirects=False)
        self.assertInRedirect(CENSUS_CY_BASE_URL)

    def test_redirects_to_census_nir_home_page_when_submitting_nir_theme(self):
        self._launch_and_submit_questionnaire(
            schema="test_thank_you_census_household",
            account_service_log_out_url=ACCOUNT_SERVICE_LOG_OUT_URL,
        )

        with self.session as cookie_session:
            cookie_session["theme"] = "census-nisra"

        self.get(SIGN_OUT_URL_PATH, follow_redirects=False)
        self.assertInRedirect(CENSUS_NIR_BASE_URL)
