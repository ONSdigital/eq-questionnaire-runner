from datetime import datetime
from typing import Union

from flask_babel import lazy_gettext

from app.data_models import QuestionnaireStore
from app.helpers.template_helpers import get_survey_type, render_template
from app.questionnaire import QuestionnaireSchema
from app.views.contexts.view_preview_questions_context import (
    build_view_preview_questions_context,
)


class ViewPreviewQuestions:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        language: str,
    ):
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._language = language

    def get_context(self) -> dict[str, Union[str, datetime, dict]]:
        return build_view_preview_questions_context(
            self._language, self._schema, self._questionnaire_store, get_survey_type()
        )

    @staticmethod
    def get_page_title() -> str:
        title: str = lazy_gettext("Preview Questions")
        return title

    def get_rendered_html(self) -> str:
        return render_template(
            template="preview",
            content=self.get_context(),
            page_title=self.get_page_title(),
        )
