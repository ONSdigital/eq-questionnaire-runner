from tests.integration.integration_test_case import IntegrationTestCase


class TestViewPreviewPDF(IntegrationTestCase):
    def test_download(self):
        super().setUp()

        # Given I launch and complete a questionnaire that has view-submitted-response enabled and has expired
        self.launchSurvey("test_introduction_preview_linear")
        self.get("/questionnaire/preview/")

        # When I try to download preview questions from the preview page
        download_pdf_url = (
            self.getHtmlSoup()
            .find("a", {"href": "/questionnaire/download-pdf"})
            .attrs["href"]
        )

        self.get(download_pdf_url)

        # Then I get 200 status code
        self.assertStatusCode(200)
