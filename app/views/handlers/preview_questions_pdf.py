import io

from flask import Response

from app.views.handlers.pdf_response import PDFResponse
from app.views.handlers.view_preview_questions import ViewPreviewQuestions


class PreviewQuestionsPDF(PDFResponse, ViewPreviewQuestions):
    def get_pdf(self) -> Response:
        """
        Generates a PDF document from the rendered ViewSubmittedResponse html.
        :return: The generated PDF document as BytesIO
        :rtype: io.BytesIO
        """
        return self._get_pdf(rendered_html=self.get_rendered_html())
