import io
import logging
from functools import lru_cache

import pdfkit
from flask import Response, current_app, send_file
from flask_weasyprint import CSS, HTML, render_pdf

from app.data_models import QuestionnaireStore
from app.questionnaire import QuestionnaireSchema
from app.settings import PRINT_STYLE_SHEET_FILE_PATH
from app.views.handlers.view_submitted_response import (
    ViewSubmittedResponse,
    ViewSubmittedResponseExpired,
)

# Set weasyprint logging level to ERROR to prevent verbose logs
weasyprint_logger = logging.getLogger("weasyprint")
weasyprint_progress_logger = logging.getLogger("weasyprint.progress")
font_logger = logging.getLogger("fontTools")

# weasyprint_logger.setLevel(level=logging.ERROR)
# weasyprint_progress_logger.setLevel(level=logging.ERROR)
# font_logger.setLevel(level=logging.ERROR)


@lru_cache(maxsize=None)
def get_print_css_weasy():
    with open(
        f"{PRINT_STYLE_SHEET_FILE_PATH}/print_weasy.css", encoding="utf-8"
    ) as css_file:
        css = css_file.read()
        return CSS(string=css)


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

    def get_pdf(self) -> Response:
        """
        Generates a PDF document from the rendered ViewSubmittedResponse html.
        :return: The generated PDF document as BytesIO
        :rtype: Response
        """
        content_as_bytes = pdfkit.from_string(
            input=self.get_rendered_html(),
            output_path=None,
            css=f'{current_app.config["PRINT_STYLE_SHEET_FILE_PATH"]}/print.css',
            options=self.wkhtmltopdf_options,
        )

        return send_file(
            path_or_file=io.BytesIO(content_as_bytes),
            mimetype=self.mimetype,
            as_attachment=True,
            download_name=self.filename,
        )

    def get_pdf_pdfkit_optimised(self) -> Response:
        """
        Generates a PDF document from the rendered ViewSubmittedResponse html.
        :return: The generated PDF document as BytesIO
        :rtype: Response
        """
        rendered_html = self.get_rendered_html()
        # This stylesheet is being removed so Weasyprint will not try resolve it and parse it.
        # This is hacky and we should look at solutions to making this configurable, so the DS is able to not output it / use a custom path.
        rendered_html_without_main_css = rendered_html.replace(
            f'<link rel="stylesheet" href="{current_app.config["CDN_URL"]}{current_app.config["CDN_ASSETS_PATH"]}/45.2.0/css/main.css">',
            "",
        )

        content_as_bytes = pdfkit.from_string(
            input=rendered_html_without_main_css,
            output_path=None,
            css=f"{PRINT_STYLE_SHEET_FILE_PATH}/print_weasy.css",
            options=self.wkhtmltopdf_options,
        )

        return send_file(
            path_or_file=io.BytesIO(content_as_bytes),
            mimetype=self.mimetype,
            as_attachment=True,
            download_name=self.filename,
        )

    def get_pdf_weasy(self) -> Response:
        """
        Generates a PDF document from the rendered ViewSubmittedResponse html.
        :return: The generated PDF document as BytesIO
        :rtype: Response
        """
        rendered_html = self.get_rendered_html()
        # This stylesheet is being removed so Weasyprint will not try resolve it and parse it.
        # This is hacky and we should look at solutions to making this configurable, so the DS is able to not output it / use a custom path.
        rendered_html_without_main_css = rendered_html.replace(
            f'<link rel="stylesheet" href="{current_app.config["CDN_URL"]}{current_app.config["CDN_ASSETS_PATH"]}/45.2.0/css/main.css">',
            "",
        )
        return render_pdf(
            html=HTML(string=rendered_html_without_main_css),
            stylesheets=[get_print_css_weasy()],
            download_filename=self.filename,
            automatic_download=True,
        )
