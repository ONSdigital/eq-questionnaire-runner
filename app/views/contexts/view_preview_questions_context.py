from datetime import datetime
from typing import Union

from flask import url_for
from flask_babel import lazy_gettext

from app.data_models import QuestionnaireStore
from app.data_models.metadata_proxy import NoMetadataException
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
) -> dict[str, Union[str, datetime, dict]]:


    metadata = questionnaire_store.metadata
    if not metadata:
        raise NoMetadataException

    trad_as = metadata["trad_as"]
    ru_name = metadata["ru_name"]

    if survey_type is SurveyType.SOCIAL:
        submitted_text = lazy_gettext("Answers submitted.")
    elif trad_as:
        submitted_text = lazy_gettext(
            "Answers submitted for <span>{ru_name}</span> ({trad_as})"
        ).format(ru_name=ru_name, trad_as=trad_as)
    else:
        submitted_text = lazy_gettext(
            "Answers submitted for <span>{ru_name}</span>"
        ).format(ru_name=ru_name)

    metadata = build_submission_metadata_context(
        survey_type,
        questionnaire_store.submitted_at,  # type: ignore
        metadata.tx_id,
    )
    context = {
        "hide_sign_out_button": True,
        "metadata": metadata,
        "submitted_text": submitted_text,
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
    context["summary"] = summary_context()
    context["pdf_url"] = url_for("questionnaire.get_preview_questions_pdf")

    return context
