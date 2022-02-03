import io

from flask_weasyprint import HTML, CSS
from flask import current_app
import pdfkit

from app.data_models import QuestionnaireStore
from app.questionnaire import QuestionnaireSchema
from app.views.handlers.view_submitted_response import (
    ViewSubmittedResponse,
    ViewSubmittedResponseExpired,
)


class ViewSubmittedResponsePDF(ViewSubmittedResponse):
    """
    Responsible for the PDF generation for the view submitted response.

    Subclassed from `ViewSubmittedResponse`.

    Attributes:
        schema: The questionnaire schema object representing the schema JSON.
        questionnaire_store: The questionnaire store object.
        language: The language the user is currently in.

    Raises:
        ViewSubmittedResponseExpired: If the submitted response has expired.
    """

    # The mimetype to use for response
    mimetype = "application/pdf"

    # Options to be passed to wkhtmltopdf via PDFKit
    wkhtmltopdf_options = {
        "quiet": "",
        "margin-top": "0.30in",
        "margin-right": "0.40in",
        "margin-bottom": "0.30in",
        "margin-left": "0.40in",
        "dpi": 365,
    }

    def __init__(
        self,
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        language: str,
    ):
        super().__init__(schema, questionnaire_store, language)
        self._metadata = self._questionnaire_store.metadata

        if self.has_expired:
            raise ViewSubmittedResponseExpired

    @property
    def filename(self) -> str:
        """The name to use for the PDF file"""
        return f"{self._metadata['schema_name']}.pdf"

    def get_pdf(self) -> io.BytesIO:
        """
        Generates a PDF document from the rendered ViewSubmittedResponse html.
        :return: The generated PDF document as BytesIO
        :rtype: io.BytesIO
        """

        html = self.get_rendered_html()
        css = """
            .header__main {
                background: none !important;
            }
            .header__title {
                color: black !important;
            }
        """
        file = io.BytesIO()
        HTML(file_obj=html).write_pdf(
            "file",
            stylesheets=[
                CSS(
                    filename=f'{current_app.config["PRINT_STYLE_SHEET_FILE_PATH"]}/print.css'
                )
            ],
        )
        return file

        # content_as_bytes = pdfkit.from_string(
        #     input=self.get_rendered_html(),
        #     output_path=None,
        #     css=f'{current_app.config["PRINT_STYLE_SHEET_FILE_PATH"]}/print.css',
        #     options=self.wkhtmltopdf_options,
        # )

        # return io.BytesIO(content_as_bytes)
