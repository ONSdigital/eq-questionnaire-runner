from mock import Mock, patch

from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.settings import (
    ACCOUNT_SERVICE_BASE_URL,
    ACCOUNT_SERVICE_BASE_URL_SOCIAL,
    ONS_URL,
)
from tests.app.parser.conftest import get_response_expires_at
from tests.integration.create_token import ACCOUNT_SERVICE_URL
from tests.integration.integration_test_case import IntegrationTestCase

DEFAULT_URL = ACCOUNT_SERVICE_URL
BUSINESS_URL = ACCOUNT_SERVICE_BASE_URL
SOCIAL_URL = ACCOUNT_SERVICE_BASE_URL_SOCIAL


class TestErrors(IntegrationTestCase):  # pylint: disable=too-many-public-methods
    example_payload = {
        "survey_metadata": {
            "data": {
                "user_id": "integration-test",
                "period_str": "April 2016",
                "period_id": "201604",
                "ru_ref": "12345678901A",
                "ru_name": "Integration Testing",
                "ref_p_start_date": "2016-04-01",
                "ref_p_end_date": "2016-04-30",
                "return_by": "2016-05-06",
                "employment_date": "1983-06-02",
                "region_code": "GB-ENG",
            }
        },
        "collection_exercise_sid": "789",
        "response_id": "1234567890123456",
        "language_code": "en",
        "account_service_url": "http://correct.place",
        "roles": [],
        "response_expires_at": get_response_expires_at(),
        "version": "v2",
    }

    def _assert_generic_500_page_content(self):
        self.assertInBody(
            "<h1>Sorry, there is a problem with this service</h1>\n"
            "<p>Try again later.</p>\n"
            "<p>If you have started a survey, your answers have been saved.</p>"
        )

    def _assert_default_theme_500_page_content(
        self, *, url=DEFAULT_URL, has_header=False, contact_us_text="contact us"
    ):
        header_text = "<h2>Business surveys</h2>\n" if has_header else ""
        self.assertInBody(
            f"{header_text}<p>If you have attempted to submit your survey, you should check that this was successful. To do this, "
            f'<a href="{url}/sign-in/logout">sign in to your business survey account</a>.</p>\n'
            f'<p>If you need more help, <a href="{url}/contact-us/">{contact_us_text}</a>.</p>'
        )

    def _assert_social_theme_500_page_content(
        self, has_header=False, contact_us_text="contact us"
    ):
        header_text = "<h2>All other surveys</h2>\n" if has_header else ""

        self.assertInBody(
            f"{header_text}<p>If you have attempted to submit your survey, you should check that this was successful. To do this, "
            f'<a href="{SOCIAL_URL}/{DEFAULT_LANGUAGE_CODE}/start/">re-enter your code</a>.</p>\n'
            f'<p>If you need more help, <a href="{ONS_URL}/aboutus/contactus/surveyenquiries/">{contact_us_text}</a>.</p>'
        )

    def test_errors_404(self):
        self.get("/hfjdskahfjdkashfsa")
        self.assertStatusNotFound()

        # Test that my account link does not show
        self.assertNotInBody("Help")
        self.assertNotInBody("My account")
        self.assertNotInBody("Sign out")

    def test_errors_404_with_payload(self):
        with patch(
            "tests.integration.create_token.PAYLOAD_V2_BUSINESS", self.example_payload
        ):
            self.launchSurveyV2(schema_name="test_percentage")
            self.get("/hfjdskahfjdkashfsa")
            self.assertStatusNotFound()

    def test_errors_405(self):
        # Given / When
        self.get("/flush")

        # Then
        self.assertStatusCode(405)  # 405 is returned as the status code
        self.assertInBody("Page not found")  # 404 page template is used

    def test_errors_500_with_payload(self):
        # Given
        with patch(
            "tests.integration.create_token.PAYLOAD_V2_BUSINESS", self.example_payload
        ):
            self.launchSurveyV2(schema_name="test_percentage")
            # When / Then
            # Patch out a class in post to raise an exception so that the application error handler
            # gets called
            with patch(
                "app.routes.questionnaire.get_block_handler",
                side_effect=Exception("You broke it"),
            ):
                self.post({"answer": "5000000"})
                self.assertStatusCode(500)

    def test_errors_500_exception_during_error_handling(self):
        # Given
        with patch(
            "tests.integration.create_token.PAYLOAD_V2_BUSINESS", self.example_payload
        ):
            self.launchSurveyV2(schema_name="test_percentage")
            # When

            # Patch out a class in post to raise an exception so that the application error handler
            # gets called
            with patch(
                "app.routes.questionnaire.get_block_handler",
                side_effect=Exception("You broke it"),
            ):
                # Another exception occurs during exception handling
                with patch(
                    "app.routes.errors.log_exception",
                    side_effect=Exception("You broke it again"),
                ):
                    self.post({"answer": "5000000"})

                    self.assertStatusCode(500)
                    self._assert_generic_500_page_content()

    def test_401_theme_default_cookie_exists(self):
        # Given
        self.launchSurveyV2(schema_name="test_introduction")
        self.assertInUrl("/questionnaire/introduction/")

        # When
        current_url = self.last_url
        self.exit()
        self.get(current_url)

        # Then
        self.assertStatusUnauthorised()
        cookie = self.getCookie()
        self.assertEqual(cookie.get("theme"), "default")
        self.assertInBody(
            f'<p>You will need to <a href="{DEFAULT_URL}/sign-in/logout">sign back in</a> to access your account</p>'
        )

    def test_401_theme_social_cookie_exists(self):
        # Given
        self.launchSurveyV2(
            schema_name="test_theme_social",
            theme="social",
            account_service_url=SOCIAL_URL,
        )
        self.assertInUrl("/questionnaire/radio/")

        # When
        current_url = self.last_url
        self.saveAndSignOut()
        self.get(current_url)

        # Then
        self.assertStatusUnauthorised()
        cookie = self.getCookie()
        self.assertEqual(cookie.get("theme"), "social")
        self.assertInBody(
            f'<p>To access this page you need to <a href="{SOCIAL_URL}/{DEFAULT_LANGUAGE_CODE}/start/">re-enter your access code</a>.</p>'
        )

    def test_401_no_cookie(self):
        # Given
        self.launchSurveyV2(schema_name="test_introduction")
        self.assertInUrl("/questionnaire/introduction/")

        # When
        current_url = self.last_url
        self.exit()
        self.deleteCookieAndGetUrl(current_url)

        # Then
        self.assertStatusUnauthorised()
        self.assertInBody(
            [
                (
                    f'<p>If you are completing a business survey, you need to sign back in to <a href="{BUSINESS_URL}/sign-in/logout">your account</a>.</p>'
                ),
                f'<p>If you started your survey using an access code, you need to <a href="{SOCIAL_URL}/{DEFAULT_LANGUAGE_CODE}/start/">re-enter your code</a>.'
                "</p>",
            ]
        )

    def test_403_theme_default_cookie_exists(self):
        # Given
        self.launchSurveyV2(schema_name="test_introduction")

        # When
        cookie = self.getUrlAndCookie("/dump/debug")

        # Then
        self.assertEqual(cookie.get("theme"), "default")
        self.assertStatusForbidden()
        self.assertInBody(
            f'<p>For further help, please <a href="{DEFAULT_URL}/contact-us/">contact us</a>.</p>'
        )

    def test_403_theme_social_cookie_exists(self):
        # Given
        self.launchSurveyV2(
            schema_name="test_theme_social",
            theme="social",
            account_service_url=SOCIAL_URL,
        )

        # When
        cookie = self.getUrlAndCookie("/dump/debug")
        # Then
        self.assertEqual(cookie.get("theme"), "social")
        self.assertStatusForbidden()
        self.assertInBody(
            f'<p>For further help, please <a href="{ONS_URL}/aboutus/contactus/surveyenquiries/">contact us</a>.</p>'
        )

    def test_403_no_cookie(self):
        # Given
        self.launchSurveyV2(schema_name="test_introduction")

        # When
        token = 123
        self.get(url=f"/session?token={token}")

        # Then
        self.assertStatusForbidden()
        self.assertInBody(
            [
                (
                    f'<p>If you are completing a business survey and you need further help, please <a href="{BUSINESS_URL}/contact-us/">contact us</a>.</p>'
                ),
                (
                    f'<p>If you started your survey using an access code and you need further help, please <a href="{ONS_URL}/aboutus/contactus/surveyenquiries'
                    '/">contact us</a>.</p>'
                ),
            ]
        )

    def test_404_theme_default_cookie_exists(self):
        # Given
        self.launchSurveyV2(schema_name="test_introduction")

        # When
        cookie = self.getUrlAndCookie("/abc123")

        # Then
        self.assertEqual(cookie.get("theme"), "default")
        self.assertStatusNotFound()
        self.assertInBody(
            f'<p>If the web address is correct or you selected a link or button, <a href="{DEFAULT_URL}/contact-us/">contact us</a> for more help.</p>'
        )

    def test_404_theme_social_cookie_exists(self):
        # Given
        self.launchSurveyV2(
            schema_name="test_theme_social",
            theme="social",
            account_service_url=SOCIAL_URL,
        )

        # When
        cookie = self.getUrlAndCookie("/abc123")

        # Then
        self.assertEqual(cookie.get("theme"), "social")
        self.assertStatusNotFound()
        self.assertInBody(
            f'<p>If the web address is correct or you selected a link or button, <a href="{ONS_URL}/aboutus/contactus/surveyenquiries/">contact us</a> for more'
            " help.</p>"
        )

    def test_404_no_cookie(self):
        # Given
        self.launchSurveyV2(schema_name="test_introduction")

        # When
        self.deleteCookieAndGetUrl("/abc123")

        # Then
        self.assertStatusNotFound()
        self.assertInBody(
            [
                "<p>If the web address is correct or you selected a link or button, please see the following help links.</p>",
                f'<p>If you are completing a business survey, please <a href="{BUSINESS_URL}/contact-us/">contact us</a>.</p>',
                f'<p>If you started your survey using an access code, please <a href="{ONS_URL}/aboutus/contactus/surveyenquiries/">contact us</a>.</p>',
            ]
        )

    def test_404_no_cookie_unauthenticated(self):
        # Given
        self.launchSurveyV2(schema_name="test_introduction")

        # When
        self.exit()
        self.deleteCookieAndGetUrl("/abc123")

        # Then
        self.assertStatusNotFound()
        self.assertInBody(
            [
                "<p>If the web address is correct or you selected a link or button, please see the following help links.</p>",
                f'<p>If you are completing a business survey, please <a href="{BUSINESS_URL}/contact-us/">contact us</a>.</p>',
                f'<p>If you started your survey using an access code, please <a href="{ONS_URL}/aboutus/contactus/surveyenquiries/">contact us</a>.</p>',
            ]
        )

    def test_500_theme_default_cookie_exists(self):
        # Given
        self.launchSurveyV2(schema_name="test_introduction")

        # When
        with patch(
            "app.routes.questionnaire.get_block_handler",
            side_effect=Exception("You broke it"),
        ):
            self.post({"answer": "test"})
            cookie = self.getCookie()

            # Then
            self.assertEqual(cookie.get("theme"), "default")
            self.assertStatusCode(500)
            self._assert_generic_500_page_content()
            self._assert_default_theme_500_page_content()

    def test_500_theme_social_cookie_exists(self):
        # Given
        self.launchSurveyV2(
            schema_name="test_theme_social",
            theme="social",
            account_service_url=SOCIAL_URL,
        )
        # When
        with patch(
            "app.routes.questionnaire.get_block_handler",
            side_effect=Exception("You broke it"),
        ):
            self.post({"answer": "test"})
            cookie = self.getCookie()

            # Then
            self.assertEqual(cookie.get("theme"), "social")
            self.assertStatusCode(500)
            self._assert_generic_500_page_content()
            self._assert_social_theme_500_page_content()

    def test_500_theme_not_set_in_cookie(self):
        # Given I launch a survey, When the 'theme' is not set in the cookie
        with patch(
            "app.routes.session.set_schema_context_in_cookie",
            side_effect=Exception("Theme set failed"),
        ):
            self.launchSurveyV2(schema_name="test_introduction")

        # Then I see the generic 500 error page
        cookie = self.getCookie()
        self.assertEqual(cookie.get("theme"), None)
        self.assertStatusCode(500)
        self._assert_generic_500_page_content()
        self._assert_default_theme_500_page_content(
            url=BUSINESS_URL,
            has_header=True,
            contact_us_text="contact us about business surveys",
        )
        self._assert_social_theme_500_page_content(
            has_header=True, contact_us_text="contact us about all other surveys"
        )

    def test_submission_failed_theme_default_cookie_exists(self):
        # Given
        submitter = self._application.eq["submitter"]
        submitter.send_message = Mock(return_value=False)

        # When
        self.launchAndFailSubmission("test_instructions")
        self.post()

        # Then
        self.assertStatusCode(500)
        self.assertInBody(
            f'<p>If this problem keeps happening, please <a href="{DEFAULT_URL}/contact-us/">contact us</a> for help.</p>'
        )

    def test_submission_failed_theme_social_cookie_exists(self):
        # Given
        submitter = self._application.eq["submitter"]
        submitter.send_message = Mock(return_value=False)

        # When
        self.launchSurveyV2(
            schema_name="test_theme_social",
            theme="social",
            account_service_url=SOCIAL_URL,
        )
        self.post()
        self.post()
        self.post()

        # Then
        self.assertStatusCode(500)
        self.assertInBody(
            f'<p>If this problem keeps happening, please <a href="{ONS_URL}/aboutus/contactus/surveyenquiries/">contact us</a> for help.</p>'
        )

    def test_preview_not_enabled_results_in_404(self):
        self.launchSurveyV2(schema_name="test_checkbox")
        self.post(action="start_questionnaire")
        self.get("/questionnaire/preview/")
        self.assertStatusCode(404)

    def launchAndFailSubmission(self, schema):
        self.launchSurveyV2(schema_name=schema)
        self.post()
        self.post()
        self.post()

    def getUrlAndCookie(self, url):
        self.get(url=url)
        return self.getCookie()

    def deleteCookieAndGetUrl(self, url):
        self.deleteCookie()
        self.get(url=url)
