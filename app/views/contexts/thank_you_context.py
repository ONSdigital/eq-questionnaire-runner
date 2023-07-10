from datetime import datetime
from typing import Any, Optional

from flask import url_for
from flask_babel import lazy_gettext

from app.data_models.metadata_proxy import MetadataProxy
from app.forms.email_form import EmailForm
from app.globals import (
    get_view_submitted_response_expiration_time,
    has_view_submitted_response_expired,
)
from app.questionnaire import QuestionnaireSchema
from app.survey_config.survey_type import SurveyType
from app.views.contexts.email_form_context import build_email_form_context
from app.views.contexts.submission_metadata_context import (
    build_submission_metadata_context,
)


def build_thank_you_context(
    schema: QuestionnaireSchema,
    metadata: MetadataProxy,
    submitted_at: datetime,
    survey_type: SurveyType,
    guidance_content: Optional[dict] = None,
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
    return {
        "hide_sign_out_button": True,
        "submission_text": submission_text,
        "metadata": context_metadata,
        "guidance": guidance_content,
        "view_submitted_response": build_view_submitted_response_context(
            schema, submitted_at
        ),
    }


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


def build_census_thank_you_context(
    metadata: MetadataProxy,
    confirmation_email_form: Optional[EmailForm],
    form_type: str,
) -> dict[str, bool | str | None]:
    context = {
        "display_address": metadata["display_address"],
        "form_type": form_type,
        "hide_sign_out_button": False,
        "sign_out_url": url_for("session.get_sign_out"),
    }
    if confirmation_email_form:
        context.update(build_email_form_context(confirmation_email_form))
    return context
