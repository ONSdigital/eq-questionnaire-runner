from flask import url_for
from flask_babel import lazy_gettext

from app.data_models import QuestionnaireStore
from app.helpers.template_helpers import render_template
from app.questionnaire import QuestionnaireSchema
from app.views.contexts.preview_context import PreviewContext


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

    def get_context(self) -> dict[str, object]:
        preview_context = PreviewContext(
            language=self._language,
            schema=self._schema,
            answer_store=self._questionnaire_store.answer_store,
            list_store=self._questionnaire_store.list_store,
            progress_store=self._questionnaire_store.progress_store,
            metadata=self._questionnaire_store.metadata,
            response_metadata=self._questionnaire_store.response_metadata,
        )
        context = {"hide_sign_out_button": True, "preview": preview_context()}
        context["pdf_url"] = url_for("questionnaire.get_preview_questions_pdf")

        return context

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
