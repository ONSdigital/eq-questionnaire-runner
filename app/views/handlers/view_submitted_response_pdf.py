import io

import pdfkit
from flask import current_app

from app.data_models import QuestionnaireStore
from app.questionnaire import QuestionnaireSchema
from app.views.handlers.view_submitted_response import (
    ViewSubmittedResponse,
    ViewSubmittedResponseExpired,
)


class ViewSubmittedResponsePDF(ViewSubmittedResponse):
    mimetype = "application/pdf"

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
        return f"{self._metadata['schema_name']}.pdf"

    def get_pdf(self) -> io.BytesIO:
        content_as_bytes = pdfkit.from_string(
            input=self.get_rendered_html(),
            output_path=None,
            css=f'{current_app.config["PRINT_STYLE_SHEET_FILE_PATH"]}/print.css',
            options={
                "quiet": "",
                "dpi": 365,
            },
        )

        return io.BytesIO(content_as_bytes)
