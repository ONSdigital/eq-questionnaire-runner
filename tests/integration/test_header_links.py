from app.settings import ACCOUNT_SERVICE_BASE_URL
from tests.integration.create_token import ACCOUNT_SERVICE_URL
from tests.integration.integration_test_case import IntegrationTestCase


class TestHeaderLinks(IntegrationTestCase):
    def assert_my_account_link_exist(self):
        account_link = self.getLinkById("header-link-my-account")
        self.assertIsNotNone(account_link)
        self.assertEqual(account_link.text, "My account")
        self.assertEqual(account_link["href"], f"{ACCOUNT_SERVICE_URL}/my-account")

    def assert_my_account_link_does_not_exist(self):
        account_link = self.getLinkById("header-link-my-account")
        self.assertIsNone(account_link)
        self.assertNotInBody("My account")

    def assert_sign_out_link_exist(self):
        sign_out_link = self.getLinkById("header-link-sign-out")
        self.assertIsNotNone(sign_out_link)
        self.assertEqual(sign_out_link.text, "Sign out")
        self.assertEqual(sign_out_link["href"], "/sign-out")

    def assert_sign_out_link_does_not_exist(self):
        sign_out_link = self.getLinkById("header-link-sign-out")
        self.assertIsNone(sign_out_link)
        self.assertNotInBody("Sign out")

    def assert_help_link_exist(self):
        help_link = self.getLinkById("header-link-help")
        self.assertIsNotNone(help_link)
        self.assertEqual(help_link.text, "Help")
        self.assertEqual(
            help_link["href"],
            f"{ACCOUNT_SERVICE_URL}/surveys/surveys-help?survey_ref=001&ru_ref=12345678901",
        )

    def assert_help_link_exist_not_authenticated(self):
        help_link = self.getLinkById("header-link-help")
        self.assertIsNotNone(help_link)
        self.assertEqual(help_link.text, "Help")
        self.assertEqual(
            help_link["href"],
            f"{ACCOUNT_SERVICE_BASE_URL}/help",
        )

    def assert_help_link_exist_not_authenticated_after_sign_out(self):
        help_link = self.getLinkById("header-link-help")
        self.assertIsNotNone(help_link)
        self.assertEqual(help_link.text, "Help")
        self.assertEqual(
            help_link["href"],
            f"{ACCOUNT_SERVICE_URL}/help",
        )

    def assert_help_link_does_not_exist_not_authenticated_after_sign_out(self):
        help_link = self.getLinkById("header-link-help")
        self.assertIsNone(help_link)

    def assert_help_link_does_not_exist(self):
        help_link = self.getLinkById("header-link-help")
        self.assertIsNone(help_link)
        self.assertNotInBody("Help")


class TestHeaderLinksPreSubmission(TestHeaderLinks):
    def test_links_in_header_when_valid_session(self):
        # Given
        self.launchSurvey("test_thank_you")

        # When
        self.assertStatusOK()

        # Then
        self.assert_my_account_link_exist()
        self.assert_sign_out_link_exist()
        self.assert_help_link_exist()

    def test_links_in_header_when_no_session_but_cookie_exists(self):
        # Given
        self.launchSurvey("test_thank_you")
        self.assertInUrl("questionnaire/did-you-know/")
        self.saveAndSignOut()

        # When
        self.assertStatusCode(302)
        self.get("questionnaire/")

        # Then
        self.assertInUrl("questionnaire/")
        cookie = self.getCookie()
        self.assertEqual(cookie.get("theme"), "default")
        self.assert_my_account_link_does_not_exist()
        self.assert_sign_out_link_does_not_exist()
        self.assert_help_link_exist_not_authenticated_after_sign_out()

    def test_links_in_header_when_no_session_but_cookie_exists_theme_social(self):
        # Given
        self.launchSurveyV2(schema_name="test_theme_social", theme="social")
        self.assertInUrl("/questionnaire/radio/")
        self.saveAndSignOut()

        # When
        self.assertStatusCode(302)
        self.get("questionnaire/")

        # Then
        self.assertInUrl("questionnaire/")
        cookie = self.getCookie()
        self.assertEqual(cookie.get("theme"), "social")
        self.assert_my_account_link_does_not_exist()
        self.assert_sign_out_link_does_not_exist()
        self.assert_help_link_does_not_exist()

    def test_links_not_in_header_when_no_session(self):
        # Given
        self.get("/questionnaire")

        # When
        self.assertStatusUnauthorised()

        # Then
        self.assert_my_account_link_does_not_exist()
        self.assert_sign_out_link_does_not_exist()
        self.assert_help_link_does_not_exist()

    def test_links_not_in_header_when_valid_session_theme_social(self):
        # Given
        self.launchSurveyV2(schema_name="test_theme_social", theme="social")

        # When
        self.assertStatusOK()

        # Then
        self.assert_my_account_link_does_not_exist()
        self.assert_sign_out_link_does_not_exist()
        self.assert_help_link_does_not_exist()


class TestHeaderLinksPostSubmission(TestHeaderLinks):
    def test_links_in_header_when_valid_session(self):
        # Given
        self.launchSurvey("test_thank_you")
        self.post()
        self.post()

        # When
        self.assertInUrl("/thank-you")
        self.assertStatusOK()

        # Then
        self.assert_my_account_link_exist()
        self.assert_sign_out_link_exist()
        self.assert_help_link_exist()

    def test_links_not_in_header_when_no_session(self):
        # Given
        self.get("/submitted/thank-you/")

        # When
        self.assertStatusUnauthorised()

        # Then
        self.assert_my_account_link_does_not_exist()
        self.assert_sign_out_link_does_not_exist()
        self.assert_help_link_does_not_exist()

    def test_links_not_in_header_when_valid_session_theme_social_thank_you_page(self):
        # Given
        self.launchSurveyV2(schema_name="test_theme_social", theme="social")
        self.post()
        self.post()

        # When
        self.assertInUrl("/thank-you")
        self.assertStatusOK()

        # Then
        self.assert_my_account_link_does_not_exist()
        self.assert_sign_out_link_does_not_exist()
        self.assert_help_link_does_not_exist()


class TestHeaderLinksPostSignOut(TestHeaderLinks):
    def test_links_not_in_header_after_sign_out(self):
        # Given
        self.launchSurvey("test_thank_you")
        self.assert_my_account_link_exist()
        self.assert_sign_out_link_exist()
        self.assert_help_link_exist()

        # When I sign out and go back to previous url since we will be redirected
        current_url = self.last_url
        self.signOut()
        self.get(current_url)

        # Then
        self.assertInBody("Sorry, you need to sign in again")
        self.assert_my_account_link_does_not_exist()
        self.assert_sign_out_link_does_not_exist()
        self.assert_help_link_exist_not_authenticated_after_sign_out()

    def test_links_not_in_header_after_sign_out_theme_social(self):
        # Given
        self.launchSurvey("test_theme_social")
        self.assert_my_account_link_does_not_exist()
        self.assert_sign_out_link_does_not_exist()
        self.assert_help_link_does_not_exist()

        # When I sign out and go back to previous url since we will be redirected
        current_url = self.last_url
        self.signOut()
        self.get(current_url)

        # Then
        self.assertInBody("Sorry, you need to sign in again")
        self.assert_my_account_link_does_not_exist()
        self.assert_sign_out_link_does_not_exist()
        self.assert_help_link_does_not_exist_not_authenticated_after_sign_out()
