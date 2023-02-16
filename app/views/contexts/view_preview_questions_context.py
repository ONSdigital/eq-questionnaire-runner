from datetime import datetime
from typing import Union

from flask import url_for

from app.data_models import QuestionnaireStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.contexts.preview_context import PreviewContext


def build_view_preview_questions_context(
    language: str,
    schema: QuestionnaireSchema,
    questionnaire_store: QuestionnaireStore,
) -> dict[str, Union[str, Union[str, datetime], dict]]:

    metadata = questionnaire_store.metadata

    context = {
        "hide_sign_out_button": True,
        "metadata": metadata,
        "submitted_text": "",
    }

    preview_context = PreviewContext(
        language=language,
        schema=schema,
        answer_store=questionnaire_store.answer_store,
        list_store=questionnaire_store.list_store,
        progress_store=questionnaire_store.progress_store,
        metadata=questionnaire_store.metadata,
        response_metadata=questionnaire_store.response_metadata,
        questionnaire_store=questionnaire_store,
    )
    context["preview"] = preview_context()  # type: ignore
    # preview_context is in conflict with context variable return type, same problem below
    context["pdf_url"] = url_for("questionnaire.get_preview_questions_pdf")

    return context  # type: ignore
