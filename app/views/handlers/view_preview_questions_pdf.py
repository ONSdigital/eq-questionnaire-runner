import io
import re

import pdfkit
from flask import current_app

from app.data_models import QuestionnaireStore
from app.questionnaire import QuestionnaireSchema
from app.views.handlers.view_preview_questions import (
    ViewPreviewQuestions,
)
from datetime import datetime, timezone


class ViewPreviewQuestionsPDF(ViewPreviewQuestions):

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

    @property
    def filename(self) -> str:
        """The name to use for the PDF file"""
        formatted_title = re.sub(
            "[^0-9a-zA-Z]+", "-", self._schema.json["title"].lower()
        )
        formatted_date = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        return f"{formatted_title}-{formatted_date}.pdf"

    def get_pdf(self) -> io.BytesIO:
        """
        Generates a PDF document from the rendered ViewSubmittedResponse html.
        :return: The generated PDF document as BytesIO
        :rtype: io.BytesIO
        """
        content_as_bytes = pdfkit.from_string(
            input=self.get_rendered_html(),
            output_path=None,
            css=f'{current_app.config["PRINT_STYLE_SHEET_FILE_PATH"]}/print.css',
            options=self.wkhtmltopdf_options,
        )

        return io.BytesIO(content_as_bytes)
