from datetime import datetime
from typing import Union

from flask import url_for

from app.data_models import QuestionnaireStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.survey_config.survey_type import SurveyType
from app.views.contexts.preview_context import PreviewContext
from app.views.contexts.submission_metadata_context import (
    build_submission_metadata_context,
)


def build_view_preview_questions_context(
    language: str,
    schema: QuestionnaireSchema,
    questionnaire_store: QuestionnaireStore,
    survey_type: SurveyType,
) -> dict[str, Union[str, Union[str, datetime], dict]]:

    metadata = questionnaire_store.metadata

    metadata = build_submission_metadata_context(
        survey_type,
        questionnaire_store.submitted_at,  # type: ignore
        metadata.tx_id,  # type: ignore
    )
    context = {
        "hide_sign_out_button": True,
        "metadata": metadata,
        "submitted_text": "",
    }

    summary_context = PreviewContext(
        language=language,
        schema=schema,
        answer_store=questionnaire_store.answer_store,
        list_store=questionnaire_store.list_store,
        progress_store=questionnaire_store.progress_store,
        metadata=questionnaire_store.metadata,
        response_metadata=questionnaire_store.response_metadata,
    )
    context["summary"] = summary_context()  # type: ignore
    context["pdf_url"] = url_for("questionnaire.get_preview_questions_pdf")

    return context  # type: ignore
