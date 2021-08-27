from datetime import datetime, timezone
from typing import Union

from app.data_models import QuestionnaireStore
from app.libs.utils import convert_tx_id
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.settings import VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS
from app.views.contexts.summary_context import SummaryContext


def build_view_submitted_response_context(
    language: str,
    schema: QuestionnaireSchema,
    questionnaire_store: QuestionnaireStore,
) -> dict[str, Union[str, datetime, dict]]:

    view_submitted_response_expired = (
        datetime.now(timezone.utc) - questionnaire_store.submitted_at
    ).total_seconds() > VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS

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
        "tx_id": convert_tx_id(questionnaire_store.metadata["tx_id"]),
        "ru_name": questionnaire_store.metadata["ru_name"],
        "summary": summary_context(),
        "hide_sign_out_button": True,
        "view_submitted_response_expired": view_submitted_response_expired,
    }
    if questionnaire_store.metadata.get("trad_as"):
        context["trad_as"] = questionnaire_store.metadata["trad_as"]
    return context
