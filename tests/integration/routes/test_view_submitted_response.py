from app import settings
from tests.integration.integration_test_case import IntegrationTestCase


class ViewSubmittedResponseBase(IntegrationTestCase):
    VIEW_RESPONSE_PAGE_URL = "/submitted/view-response"

    def _launch_and_complete_questionnaire(self):
        self.launchSurveyV2(schema_name="test_view_submitted_response")
        self.post({"name-answer": "John Smith"})
        self.post({"address-answer": "NP10 8XG"})
        self.post()

    def get_print_button(self):
        return self.getHtmlSoup().find("button", {"data-qa": "btn-print"})

    def get_download_button(self):
        # This is a temporary solution as additional attributes do not work at the moment for the download button.
        return self.getHtmlSoup().find("a", {"href": "/submitted/download-pdf"})

    def assert_expired_content(self):
        self.assertEqualPageTitle(
            "View Submitted Response - Test View Submitted Response"
        )
        self.assertInBody("Answers submitted for <span>Integration Testing</span>")
        self.assertInBody("Submitted on:")
        self.assertInBody("Submission reference:")
        self.assertInBody(
            "For security, you can no longer view or get a copy of your answers"
        )

        self.assertNotInBody("What is your name?")
        self.assertNotInBody("John Smith")
        self.assertNotInBody("What is your address?")
        self.assertNotInBody("NP10 8XG")
        self.assertIsNone(self.get_print_button())
        self.assertIsNone(self.get_download_button())


class TestViewSubmissionResponse(ViewSubmittedResponseBase):
    def test_enabled(self):
        # Given I launch and complete a questionnaire that has view-submitted-response enabled
        self._launch_and_complete_questionnaire()

        # When I try to get the view-response page
        self.get(self.VIEW_RESPONSE_PAGE_URL)

        # Then the page is displayed correctly
        self.assertEqualPageTitle(
            "View Submitted Response - Test View Submitted Response"
        )
        self.assertInBody("Answers submitted for <span>Integration Testing</span>")
        self.assertInBody("Submitted on:")
        self.assertInBody("Submission reference:")
        self.assertInBody("What is your name?")
        self.assertInBody("John Smith")
        self.assertInBody("What is your address?")
        self.assertInBody("NP10 8XG")
        self.assertIsNotNone(self.get_print_button())
        self.assertIsNotNone(self.get_download_button())

    def test_not_enabled(self):
        # Given I launch and complete a questionnaire that does not have view-submitted-response enabled
        self.launchSurveyV2(schema_name="test_confirmation_email")
        self.post()
        self.post()

        # When I try to get the view-response page
        self.get(self.VIEW_RESPONSE_PAGE_URL)

        # Then I get shown a 404 error
        self.assertStatusNotFound()

    def test_expired(self):
        settings.VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS = 0
        super().setUp()
        # Given I launch and complete a questionnaire that has view-submitted-response enabled but has expired
        self._launch_and_complete_questionnaire()

        # When I try to get the view-response page
        self.get(self.VIEW_RESPONSE_PAGE_URL)

        # Then the page is displayed correctly
        self.assert_expired_content()
