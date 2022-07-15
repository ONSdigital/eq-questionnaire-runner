from mock import Mock, patch

from app.settings import ACCOUNT_SERVICE_BASE_URL, ACCOUNT_SERVICE_BASE_URL_SOCIAL
from tests.integration.create_token import ACCOUNT_SERVICE_URL
from tests.integration.integration_test_case import IntegrationTestCase

DEFAULT_URL = ACCOUNT_SERVICE_URL
BUSINESS_URL = ACCOUNT_SERVICE_BASE_URL
SOCIAL_URL = ACCOUNT_SERVICE_BASE_URL_SOCIAL


class TestErrors(IntegrationTestCase):  # pylint: disable=too-many-public-methods
    example_payload = {
        "user_id": "integration-test",
        "period_str": "April 2016",
        "period_id": "201604",
        "collection_exercise_sid": "789",
        "ru_ref": "123456789012A",
        "response_id": "1234567890123456",
        "ru_name": "Integration Testing",
        "ref_p_start_date": "2016-04-01",
        "ref_p_end_date": "2016-04-30",
        "return_by": "2016-05-06",
        "employment_date": "1983-06-02",
        "region_code": "GB-ENG",
        "language_code": "en",
        "account_service_url": "http://correct.place",
        "roles": [],
    }

    def test_errors_404(self):
        self.get("/hfjdskahfjdkashfsa")
        self.assertStatusNotFound()

        # Test that my account link does not show
        self.assertNotInBody("Help")
        self.assertNotInBody("My account")
        self.assertNotInBody("Sign out")

    def test_errors_404_with_payload(self):
        with patch("tests.integration.create_token.PAYLOAD", self.example_payload):
            self.launchSurvey("test_percentage")
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
        with patch("tests.integration.create_token.PAYLOAD", self.example_payload):
            self.launchSurvey("test_percentage")
            # When / Then
            # Patch out a class in post to raise an exception so that the application error handler
            # gets called
            with patch(
                "app.routes.questionnaire.get_block_handler",
                side_effect=Exception("You broked it"),
            ):
                self.post({"answer": "5000000"})
                self.assertStatusCode(500)

    def test_errors_500_exception_during_error_handling(self):
        # Given
        with patch("tests.integration.create_token.PAYLOAD", self.example_payload):
            self.launchSurvey("test_percentage")
            # When

            # Patch out a class in post to raise an exception so that the application error handler
            # gets called
            with patch(
                "app.routes.questionnaire.get_block_handler",
                side_effect=Exception("You broked it"),
            ):
                # Another exception occurs during exception handling
                with patch(
                    "app.routes.errors.log_exception",
                    side_effect=Exception("You broked it again"),
                ):
                    self.post({"answer": "5000000"})

                    self.assertStatusCode(500)
                    self.assertInBody("Sorry, there is a problem with this service")

    def test_401_theme_default_cookie_exists(self):
        # Given
        self.launchSurvey("test_introduction")
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
        self.launchSurvey("test_theme_social", account_service_url=SOCIAL_URL)
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
            f'<p>To access this page you need to <a href="{SOCIAL_URL}/sign-in/logout">re-enter your access code</a>.</p>'
        )

    def test_401_no_cookie(self):
        # Given
        self.launchSurvey("test_introduction")
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
                f'<p>If you started your survey using an access code, you need to <a href="{SOCIAL_URL}/sign-in/logout">re-enter your code</a>.</p>',
            ]
        )

    def test_403_theme_default_cookie_exists(self):
        # Given
        self.launchSurvey("test_introduction")

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
        self.launchSurvey("test_theme_social", account_service_url=SOCIAL_URL)

        # When
        cookie = self.getUrlAndCookie("/dump/debug")

        # Then
        self.assertEqual(cookie.get("theme"), "social")
        self.assertStatusForbidden()
        self.assertInBody(
            f'<p>For further help, please <a href="{SOCIAL_URL}/contact-us/">contact us</a>.</p>'
        )

    def test_403_no_cookie(self):
        # Given
        self.launchSurvey("test_introduction")

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
                    f'<p>If you started your survey using an access code and you need further help, please <a href="{SOCIAL_URL}/contact-us/">contact us</a>.</'
                    "p>"
                ),
            ]
        )

    def test_404_theme_default_cookie_exists(self):
        # Given
        self.launchSurvey("test_introduction")

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
        self.launchSurvey("test_theme_social", account_service_url=SOCIAL_URL)

        # When
        cookie = self.getUrlAndCookie("/abc123")

        # Then
        self.assertEqual(cookie.get("theme"), "social")
        self.assertStatusNotFound()
        self.assertInBody(
            f'<p>If the web address is correct or you selected a link or button, <a href="{SOCIAL_URL}/contact-us/">contact us</a> for more help.</p>'
        )

    def test_404_no_cookie(self):
        # Given
        self.launchSurvey("test_introduction")

        # When
        self.deleteCookieAndGetUrl("/abc123")

        # Then
        self.assertStatusNotFound()
        self.assertInBody(
            [
                "<p>If the web address is correct or you selected a link or button, please see the following help links.</p>",
                f'<p>If you are completing a business survey, please <a href="{BUSINESS_URL}/contact-us/">contact us</a>.</p>',
                f'<p>If you started your survey using an access code, please <a href="{SOCIAL_URL}/contact-us/">contact us</a>.</p>',
            ]
        )

    def test_404_no_cookie_unauthenticated(self):
        # Given
        self.launchSurvey("test_introduction")

        # When
        self.exit()
        self.deleteCookieAndGetUrl("/abc123")

        # Then
        self.assertStatusNotFound()
        self.assertInBody(
            [
                "<p>If the web address is correct or you selected a link or button, please see the following help links.</p>",
                f'<p>If you are completing a business survey, please <a href="{BUSINESS_URL}/contact-us/">contact us</a>.</p>',
                f'<p>If you started your survey using an access code, please <a href="{SOCIAL_URL}/contact-us/">contact us</a>.</p>',
            ]
        )

    def test_500_theme_default_cookie_exists(self):
        # Given
        self.launchSurvey("test_introduction")

        # When
        with patch(
            "app.routes.questionnaire.get_block_handler",
            side_effect=Exception("You broke it"),
        ):
            self.post({"answer": "test"})
            cookie = self.getCookie()

            # Then
            self.assertEqual(cookie.get("theme"), "default")
            self.assertException()
            self.assertInBody(
                f'<p><a href="{DEFAULT_URL}/contact-us/">Contact us</a> if you need to speak to someone about your survey.</p>'
            )

    def test_500_theme_social_cookie_exists(self):
        # Given
        self.launchSurvey("test_introduction")

        # When
        with patch(
            "app.routes.questionnaire.get_block_handler",
            side_effect=Exception("You broke it"),
        ):
            self.post({"answer": "test"})
            cookie = self.getCookie()

            # Then
            self.assertEqual(cookie.get("theme"), "default")
            self.assertException()
            self.assertInBody(
                f'<p><a href="{DEFAULT_URL}/contact-us/">Contact us</a> if you need to speak to someone about your survey.</p>'
            )

    def test_500_theme_census_cookie_exists(self):
        # Given
        self.launchSurvey("test_thank_you_census_household")

        # When
        with patch(
            "app.routes.questionnaire.get_block_handler",
            side_effect=Exception("You broked it"),
        ):
            self.post({"answer": "test"})

            # Then
            self.assertException()
            self.assertInBody(
                "<p>If you are completing a business survey and you need to speak to someone about your survey,"
                f' please <a href="{DEFAULT_URL}/contact-us/">contact us</a>.</p>'
            )

    def test_submission_failed_theme_default_cookie_exists(self):
        # Given
        submitter = self._application.eq["submitter"]
        submitter.send_message = Mock(return_value=False)

        # When
        self.launchAndFailSubmission("test_introduction")

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
        self.launchSurvey("test_theme_social", account_service_url=SOCIAL_URL)
        self.post()
        self.post()
        self.post()

        # Then
        self.assertStatusCode(500)
        self.assertInBody(
            f'<p>If this problem keeps happening, please <a href="{SOCIAL_URL}/contact-us/">contact us</a> for help.</p>'
        )

    def test_submission_failed_theme_census_cookie_exists(self):
        # Given
        submitter = self._application.eq["submitter"]
        submitter.send_message = Mock(return_value=False)

        # When
        self.launchAndFailSubmission("test_thank_you_census_individual")

        # Then
        self.assertStatusCode(500)
        self.assertInBody(
            f'<p>If you are completing a business survey, please <a href="{DEFAULT_URL}/contact-us/">contact us</a>.</p>'
        )

    def launchAndFailSubmission(self, schema):
        self.launchSurvey(schema)
        self.post()
        self.post()
        self.post()

    def getUrlAndCookie(self, url):
        self.get(url=url)
        return self.getCookie()

    def deleteCookieAndGetUrl(self, url):
        self.deleteCookie()
        self.get(url=url)
