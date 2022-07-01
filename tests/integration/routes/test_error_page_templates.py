from mock import Mock, patch

from tests.integration.integration_test_case import IntegrationTestCase


class TestErrorPageTemplates(IntegrationTestCase):
    def test_401_theme_default(self):
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
            '<p>You will need to <a href="http://upstream.url/sign-in/logout">sign back in</a> to access your account</p>'
        )

    def test_401_theme_social(self):
        # Given
        self.launchSurvey("test_theme_social")
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
            '<p>To access this page you need to <a href="http://upstream.url/sign-in/logout">re-enter your access code</a>.</p>'
        )

    def test_401_theme_none(self):
        # Given
        self.launchSurvey("test_introduction")
        self.assertInUrl("/questionnaire/introduction/")

        # When
        current_url = self.last_url
        self.exit()
        self.deleteCookie()
        self.get(current_url)

        # Then
        self.assertStatusUnauthorised()
        self.assertInBody(
            '<p>If you are completing a business survey, you need to sign back in to <a href="https://surveys.ons.gov.uk/sign-in/logout">your account</a>.</p>'
        )

    def test_403_theme_default(self):
        # Given
        self.launchSurvey("test_introduction")

        # When
        self.get(url="/dump/debug")
        cookie = self.getCookie()

        # Then
        self.assertEqual(cookie.get("theme"), "default")
        self.assertStatusForbidden()
        self.assertInBody(
            '<p>For further help, please <a href="http://upstream.url/contact-us/">contact us</a>.</p>'
        )

    def test_403_theme_social(self):
        # Given
        self.launchSurvey("test_theme_social")

        # When
        self.get(url="/dump/debug")
        cookie = self.getCookie()

        # Then
        self.assertEqual(cookie.get("theme"), "social")
        self.assertStatusForbidden()
        self.assertInBody(
            '<p>For further help, please <a href="http://upstream.url/contact-us/">contact us</a>.</p>'
        )

    def test_403_theme_none(self):
        # Given
        self.launchSurvey("test_introduction")

        # When
        token = 123
        self.get(url=f"/session?token={token}")

        # Then
        self.assertStatusForbidden()
        self.assertInBody(
            '<p>If you are completing a business survey and you need further help, please <a href="https://surveys.ons.gov.uk/contact-us/">contact us</a>.</p>'
        )

    def test_404_theme_default(self):
        # Given
        self.launchSurvey("test_introduction")

        # When
        self.get(url="/abc123")
        cookie = self.getCookie()

        # Then
        self.assertEqual(cookie.get("theme"), "default")
        self.assertStatusNotFound()
        self.assertInBody(
            '<p>If the web address is correct or you selected a link or button, <a href="http://upstream.url/contact-us/">contact us</a> for more help.</p>'
        )

    def test_404_theme_social(self):
        # Given
        self.launchSurvey("test_theme_social")

        # When
        self.get(url="/abc123")
        cookie = self.getCookie()

        # Then
        self.assertEqual(cookie.get("theme"), "social")
        self.assertStatusNotFound()
        self.assertInBody(
            '<p>If the web address is correct or you selected a link or button, <a href="http://upstream.url/contact-us/">contact us</a> for more help.</p>'
        )

    def test_404_theme_none(self):
        # Given
        self.launchSurvey("test_introduction")

        # When
        self.deleteCookie()
        self.get(url="/abc123")

        # Then
        self.assertStatusNotFound()
        self.assertInBody(
            "<p>If the web address is correct or you selected a link or button, please see the following help links.</p>"
        )

    def test_500_theme_default(self):
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
                '<p><a href="http://upstream.url/contact-us/">Contact us</a> if you need to speak to someone about your survey.</p>'
            )

    def test_500_theme_census(self):
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
                ' please <a href="http://upstream.url/contact-us/">contact us</a>.</p>'
            )

    def test_submission_failed_theme_default(self):
        # Given
        submitter = self._application.eq["submitter"]
        submitter.send_message = Mock(return_value=False)

        # When
        self.launchSurvey("test_introduction")
        self.post()
        self.post()
        self.post()

        # Then
        self.assertStatusCode(500)
        self.assertInBody(
            '<p>If this problem keeps happening, please <a href="http://upstream.url/contact-us/">contact us</a> for help.</p>'
        )

    def test_submission_failed_theme_social(self):
        # Given
        submitter = self._application.eq["submitter"]
        submitter.send_message = Mock(return_value=False)

        # When
        self.launchSurvey("test_theme_social")
        self.post()
        self.post()
        self.post()

        # Then
        self.assertStatusCode(500)
        self.assertInBody(
            '<p>If this problem keeps happening, please <a href="http://upstream.url/contact-us/">contact us</a> for help.</p>'
        )

    def test_submission_failed_theme_census(self):
        # Given
        submitter = self._application.eq["submitter"]
        submitter.send_message = Mock(return_value=False)

        # When
        self.launchSurvey("test_thank_you_census_individual")
        self.post()
        self.post()

        # Then
        self.assertStatusCode(500)
        self.assertInBody(
            '<p>If you are completing a business survey, please <a href="http://upstream.url/contact-us/">contact us</a>.</p>'
        )
