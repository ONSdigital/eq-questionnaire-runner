from datetime import datetime
from typing import Any, Optional

from flask import url_for
from flask_babel import lazy_gettext

from app.data_models.metadata_proxy import MetadataProxy
from app.forms.email_form import EmailForm
from app.forms.questionnaire_form import QuestionnaireForm
from app.globals import (
    get_view_submitted_response_expiration_time,
    has_view_submitted_response_expired,
)
from app.questionnaire import QuestionnaireSchema
from app.survey_config.survey_type import SurveyType
from app.views.contexts.email_form_context import build_email_form_context
from app.views.contexts.feedback_form_context import build_feedback_context
from app.views.contexts.submission_metadata_context import (
    build_submission_metadata_context,
)
from app.views.handlers.feedback import Feedback


def build_thank_you_context(
    schema: QuestionnaireSchema,
    metadata: MetadataProxy,
    submitted_at: datetime,
    survey_type: SurveyType,
    guidance_content: Optional[dict] = None,
    confirmation_email_form: Optional[EmailForm] = None,
    feedback: Optional[Feedback] = None,
) -> dict[str, Any]:
    if (ru_name := metadata["ru_name"]) and (trad_as := metadata["trad_as"]):
        submission_text = lazy_gettext(
            "Your answers have been submitted for <span>{company_name}</span> ({trading_name})"
        ).format(
            company_name=ru_name,
            trading_name=trad_as,
        )
    elif ru_name:
        submission_text = lazy_gettext(
            "Your answers have been submitted for <span>{company_name}</span>"
        ).format(company_name=ru_name)
    else:
        submission_text = lazy_gettext("Your answers have been submitted.")
    context_metadata = build_submission_metadata_context(
        survey_type,
        submitted_at,
        metadata.tx_id,
    )

    context = {
        "hide_sign_out_button": True,
        "submission_text": submission_text,
        "metadata": context_metadata,
        "guidance": guidance_content,
        "view_submitted_response": build_view_submitted_response_context(
            schema, submitted_at
        ),
    }
    if confirmation_email_form:
        context["confirmation_email_form"] = build_email_form_context(
            confirmation_email_form
        )

    if feedback:
        context["feedback_form"] = feedback.get_context()
    return context


def build_view_submitted_response_context(
    schema: QuestionnaireSchema, submitted_at: datetime
) -> dict[str, bool | str]:
    view_submitted_response: dict[str, bool | str] = {
        "enabled": schema.is_view_submitted_response_enabled
    }

    if schema.is_view_submitted_response_enabled:
        expired = has_view_submitted_response_expired(submitted_at)
        view_submitted_response.update(
            expired=expired,
            expires_at=get_view_submitted_response_expiration_time(
                submitted_at
            ).isoformat(),
        )
        if not expired:
            view_submitted_response["url"] = url_for(
                "post_submission.get_view_submitted_response"
            )
    return view_submitted_response
