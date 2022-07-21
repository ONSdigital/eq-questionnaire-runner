import io
import re
from collections import Generator
from datetime import datetime

import pdfkit
from flask import current_app

from app.data_models import QuestionnaireStore
from app.helpers.template_helpers import render_template
from app.questionnaire import QuestionnaireSchema
from app.views.contexts.preview_context import PreviewContext
from app.views.handlers.view_submitted_response import (
    ViewSubmittedResponse,
    ViewSubmittedResponseExpired,
)


class ViewPreviewQuestionPDF(ViewSubmittedResponse):
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
        formatted_title = re.sub(
            "[^0-9a-zA-Z]+", "-", self._schema.json["title"].lower()
        )
        formatted_date = datetime.now().isoformat()  # type: ignore
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

    def get_rendered_html(self) -> str:
        title = "test"
        submit_button = "Submit answers"
        guidance = "Please submit this survey to complete it"

        warning = None
        preview_context = PreviewContext(
            answer_store=self._questionnaire_store.answer_store,
            language=self._language,
            list_store=self._questionnaire_store.list_store,
            metadata=self._metadata,
            progress_store=self._questionnaire_store.progress_store,
            response_metadata={},
            schema=self._schema,
        )

        context = {
            "title": "test",
            "guidance": guidance,
            "warning": warning,
            "submit_button": submit_button,
            "summary": preview_context(),
        }

        return render_template(template="preview", content=context)

    def get_context(self) -> Generator[dict, None, None]:
        preview_context = PreviewContext(
            answer_store=self._questionnaire_store.answer_store,
            language=self._language,
            list_store=self._questionnaire_store.list_store,
            metadata=self._metadata,
            progress_store=self._questionnaire_store.progress_store,
            response_metadata={},
            schema=self._schema,
        )
        return preview_context._build_all_groups(return_to=None)
