import io

from app.data_models import QuestionnaireStore
from app.questionnaire import QuestionnaireSchema
from app.views.handlers.pdf_response import PDFResponse
from app.views.handlers.view_submitted_response import (
    ViewSubmittedResponse,
    ViewSubmittedResponseExpired,
)


class ViewSubmittedResponsePDF(ViewSubmittedResponse, PDFResponse):
    def __init__(
        self,
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        language: str,
    ):
        super().__init__(schema, questionnaire_store, language)
        if self.has_expired:
            raise ViewSubmittedResponseExpired

    def get_pdf(self) -> io.BytesIO:
        """
        Generates a PDF document from the rendered ViewSubmittedResponse html.
        :return: The generated PDF document as BytesIO
        :rtype: io.BytesIO
        """
        return self._get_pdf(rendered_html=self.get_rendered_html())
