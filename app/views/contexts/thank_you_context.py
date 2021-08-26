from datetime import datetime
from typing import Mapping, Optional

from dateutil.tz import tzutc
from flask import url_for
from flask_babel import lazy_gettext

from app.data_models.session_data import SessionData
from app.questionnaire import QuestionnaireSchema
from app.views.contexts.email_form_context import build_email_form_context
from app.views.contexts.submission_metadata_context import (
    build_submission_metadata_context,
)


def build_thank_you_context(
    session_data: SessionData,
    submitted_at: datetime,
    survey_type: str,
    schema: QuestionnaireSchema,
    guidance_content: Optional[dict] = None,
) -> Mapping:

    submission_schema: Mapping = schema.get_submission() or {}
    view_answers = int((datetime.now(tz=tzutc()) - submitted_at).total_seconds()) < 2700
    view_submitted_url = (
        url_for("post_submission.get_view_submitted_response") if view_answers else None
    )

    if survey_type == "social":
        submission_text = lazy_gettext("Your answers have been submitted.")
    elif session_data.trad_as and session_data.ru_name:
        submission_text = lazy_gettext(
            "Your answers have been submitted for <span>{company_name}</span> ({trading_name})."
        ).format(company_name=session_data.ru_name, trading_name=session_data.trad_as)
    else:
        submission_text = lazy_gettext(
            "Your answers have been submitted for <span>{company_name}</span>."
        ).format(company_name=session_data.ru_name)
    metadata = build_submission_metadata_context(
        survey_type, submitted_at, session_data.tx_id
    )
    return {
        "hide_sign_out_button": True,
        "submission_text": submission_text,
        "metadata": metadata,
        "guidance": guidance_content,
        "view_response_enabled": submission_schema.get("view_response"),
        "view_submitted_url": view_submitted_url,
        "view_answers": view_answers,
    }


def build_census_thank_you_context(
    session_data: SessionData, confirmation_email_form, form_type
) -> Mapping:

    context = {
        "display_address": session_data.display_address,
        "form_type": form_type,
        "hide_sign_out_button": False,
        "sign_out_url": url_for("session.get_sign_out"),
    }
    if confirmation_email_form:
        context.update(build_email_form_context(confirmation_email_form))
    return context
