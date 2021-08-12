from datetime import datetime
from typing import Union

from app.data_models import QuestionnaireStore
from app.data_models.session_data import SessionData
from app.libs.utils import convert_tx_id
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.contexts.summary_context import SummaryContext


def build_submitted_response_context(
    language: str,
    schema: QuestionnaireSchema,
    questionnaire_store: QuestionnaireStore,
    session_data: SessionData,
) -> dict[str, Union[str, datetime, dict]]:

    summary_context = SummaryContext(
        language=language,
        schema=schema,
        answer_store=questionnaire_store.answer_store,
        list_store=questionnaire_store.list_store,
        progress_store=questionnaire_store.progress_store,
        metadata=questionnaire_store.metadata,
    )
    context = {
        "submitted_at": questionnaire_store.submitted_at,
        "tx_id": convert_tx_id(session_data.tx_id),
        "trad_as": session_data.trad_as,
        "summary": summary_context(answers_are_editable=False),
        "hide_sign_out_button": True,
    }
    if session_data.ru_name:
        context["ru_name"] = session_data.ru_name
    return context
