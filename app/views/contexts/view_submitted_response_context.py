from datetime import datetime
from typing import Union

from flask import url_for
from flask_babel import lazy_gettext

from app.data_models import QuestionnaireStore
from app.globals import has_view_submitted_response_expired
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.survey_config.survey_type import SurveyType
from app.views.contexts.submission_metadata_context import (
    build_submission_metadata_context,
)
from app.views.contexts.summary_context import SummaryContext


def build_view_submitted_response_context(
    language: str,
    schema: QuestionnaireSchema,
    questionnaire_store: QuestionnaireStore,
    survey_type: SurveyType,
) -> dict[str, Union[str, datetime, dict]]:

    view_submitted_response_expired = has_view_submitted_response_expired(
        questionnaire_store.submitted_at  # type: ignore
    )
    metadata_proxy = questionnaire_store.metadata
    trad_as = metadata_proxy["trad_as"]
    ru_name = metadata_proxy["ru_name"]

    if survey_type is SurveyType.SOCIAL:
        submitted_text = lazy_gettext("Answers submitted.")
    elif trad_as:
        submitted_text = lazy_gettext(
            "Answers submitted for <span>{ru_name}</span> ({trad_as})"
        ).format(ru_name=ru_name, trad_as=trad_as)
    else:
        submitted_text = lazy_gettext(
            "Answers submitted for <span>{ru_name}</span>"
        ).format(ru_name=metadata_proxy["ru_name"])

    metadata = build_submission_metadata_context(
        survey_type,
        questionnaire_store.submitted_at,  # type: ignore
        metadata_proxy["tx_id"],
    )
    context = {
        "hide_sign_out_button": True,
        "view_submitted_response": {
            "expired": view_submitted_response_expired,
        },
        "metadata": metadata,
        "submitted_text": submitted_text,
    }

    if not view_submitted_response_expired:
        summary_context = SummaryContext(
            language=language,
            schema=schema,
            answer_store=questionnaire_store.answer_store,
            list_store=questionnaire_store.list_store,
            progress_store=questionnaire_store.progress_store,
            metadata=questionnaire_store.metadata,  # type: ignore
            response_metadata=questionnaire_store.response_metadata,
        )
        context["summary"] = summary_context()
        context["pdf_url"] = url_for("post_submission.get_view_submitted_response_pdf")

    return context
