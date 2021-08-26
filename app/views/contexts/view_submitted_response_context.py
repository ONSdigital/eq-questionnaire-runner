from datetime import datetime
from typing import Union

from flask_babel import lazy_gettext

from app.data_models import QuestionnaireStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.contexts.submission_metadata_context import (
    build_submission_metadata_context,
)
from app.views.contexts.summary_context import SummaryContext


def build_view_submitted_response_context(
    language: str,
    schema: QuestionnaireSchema,
    questionnaire_store: QuestionnaireStore,
    survey_type: str,
) -> dict[str, Union[str, datetime, dict]]:

    store_metadata = questionnaire_store.metadata

    summary_context = SummaryContext(
        language=language,
        schema=schema,
        answer_store=questionnaire_store.answer_store,
        list_store=questionnaire_store.list_store,
        progress_store=questionnaire_store.progress_store,
        metadata=store_metadata,
    )

    if survey_type == "social":
        submitted_text = lazy_gettext("Answers submitted.")
    elif trad_as := store_metadata.get("trad_as"):
        submitted_text = lazy_gettext(
            "Answers submitted for <span>{ru_name}</span> ({trad_as})."
        ).format(ru_name=store_metadata["ru_name"], trad_as=trad_as)
    else:
        submitted_text = lazy_gettext(
            "Answers submitted for <span>{ru_name}</span>."
        ).format(ru_name=store_metadata["ru_name"])

    metadata = build_submission_metadata_context(
        survey_type, questionnaire_store.submitted_at, store_metadata["tx_id"]
    )
    context = {
        "hide_sign_out_button": True,
        "metadata": metadata,
        "submitted_text": submitted_text,
        "summary": summary_context(),
    }
    return context
