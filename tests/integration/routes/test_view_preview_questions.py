from tests.integration.integration_test_case import IntegrationTestCase


class TestPreviewPDF(IntegrationTestCase):
    def test_download_pdf(self):
        super().setUp()

        # Given I launch a questionnaire and open preview of questions
        self.launchSurveyV2(schema_name="test_introduction")
        self.get("/questionnaire/preview/")

        # When I try to download preview of questions from the preview page
        download_pdf_url = (
            self.getHtmlSoup()
            .find("a", {"href": "/questionnaire/preview/download-pdf"})
            .attrs["href"]
        )

        self.get(download_pdf_url)

        # Then I get 200 status code
        self.assertStatusOK()

    def test_download_pdf_no_preview(self):
        super().setUp()

        # Given I launch a questionnaire without preview enabled
        self.launchSurveyV2(schema_name="test_checkbox")

        # When I try to download preview of questions
        self.get("/questionnaire/preview/download-pdf")

        # Then I get 404 status code
        self.assertStatusNotFound()

    def test_print_button(self):
        super().setUp()

        # Given I launch a questionnaire and open preview of questions
        self.launchSurveyV2(schema_name="test_introduction")
        self.get("/questionnaire/preview/")

        # Then the print button is displayed correctly
        print_button = self.getHtmlSoup().find("button", {"data-qa": "btn-print"})
        self.assertIsNotNone(print_button)
