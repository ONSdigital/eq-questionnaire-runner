from tests.integration.integration_test_case import IntegrationTestCase


class TestPreviewPDF(IntegrationTestCase):
    def test_download(self):
        super().setUp()

        # Given I launch a questionnaire and open preview of questions
        self.launchSurvey("test_introduction")
        self.get("/questionnaire/preview/")

        # When I try to download preview of questions from the preview page
        download_pdf_url = (
            self.getHtmlSoup()
            .find("a", {"href": "/questionnaire/download-pdf"})
            .attrs["href"]
        )

        self.get(download_pdf_url)

        # Then I get 200 status code
        self.assertStatusCode(200)

    def test_print_button(self):
        super().setUp()

        # Given I launch a questionnaire and open preview of questions
        self.launchSurvey("test_introduction")
        self.get("/questionnaire/preview/")

        # Then the print button is displayed correctly
        print_button = self.getHtmlSoup().find("button", {"data-qa": "btn-print"})
        self.assertIsNotNone(print_button)
