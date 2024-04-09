from time import sleep

from freezegun import freeze_time

from app import settings
from tests.integration.routes.test_view_submitted_response import (
    ViewSubmittedResponseBase,
)


class TestViewSubmissionResponsePDF(ViewSubmittedResponseBase):
    def test_download_when_submitted_response_not_enabled(self):
        # Given I launch and complete a questionnaire that does not have view-submitted-response enabled
        self.launchSurvey("test_confirmation_email")
        self.post()
        self.post()

        # When I try to download my answers
        self.get("/submitted/download-pdf")

        # Then a 404 page is returned
        self.assertStatusNotFound()

    @freeze_time("2022-06-01T15:34:54+00:00")
    def test_download_when_submitted_response_enabled_but_not_expired(self):
        # Given I launch and complete a questionnaire that has view-submitted-response enabled and has not expired
        self._launch_and_complete_questionnaire()

        # When I try to download my answers
        self.get(self.VIEW_RESPONSE_PAGE_URL)
        self.get(self.get_download_button().attrs["href"])

        # Then the download is successful
        self.assertStatusOK()

        # Check response content type is PDF
        self.assertEqual(self.last_response.content_type, "application/pdf")

        # Check file is set to download and not open inline
        self.assertIn("attachment;", self.last_response_headers["Content-Disposition"])

        # Check filename is set as expected
        self.assertIn(
            "filename=test-view-submitted-response-2022-06-01.pdf",
            self.last_response_headers["Content-Disposition"],
        )

        # Check content length is reasonable.
        # This is given some leeway as it can change with DS changes.
        self.assertGreater(self.last_response.content_length, 16000)

    def test_download_when_submitted_response_enabled_but_expired(self):
        settings.VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS = 3
        super().setUp()

        # Given I launch and complete a questionnaire that has view-submitted-response enabled and has expired
        self._launch_and_complete_questionnaire()

        # When I try to download my answers from the view response page
        self.get(self.VIEW_RESPONSE_PAGE_URL)
        download_pdf_url = self.get_download_button().attrs["href"]

        # Wait for submitted response to expire
        sleep(5)
        self.get(download_pdf_url)

        # Then the current page is reloaded and sensitive information should not be displayed
        self.assertInUrl(self.VIEW_RESPONSE_PAGE_URL)
        self.assert_expired_content()
