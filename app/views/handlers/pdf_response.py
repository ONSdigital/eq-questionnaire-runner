import io
import re
from datetime import datetime, timezone

import pdfkit
from flask import current_app

from app.data_models import QuestionnaireStore
from app.questionnaire import QuestionnaireSchema


class PDFResponse:
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
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._language = language

    @property
    def filename(self) -> str:
        """The name to use for the PDF file"""
        formatted_title = re.sub(
            "[^0-9a-zA-Z]+", "-", self._schema.json["title"].lower()
        )
        if self._questionnaire_store.submitted_at:
            formatted_date = self._questionnaire_store.submitted_at.date().isoformat()
        else:
            formatted_date = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        return f"{formatted_title}-{formatted_date}.pdf"

    def _get_pdf(self, rendered_html: str) -> io.BytesIO:
        """
        Generates a PDF document from the rendered html.
        :return: The generated PDF document as BytesIO
        :rtype: io.BytesIO
        """
        content_as_bytes = pdfkit.from_string(
            input=rendered_html,
            output_path=None,
            css=f'{current_app.config["PRINT_STYLE_SHEET_FILE_PATH"]}/print.css',
            options=self.wkhtmltopdf_options,
        )

        return io.BytesIO(content_as_bytes)
