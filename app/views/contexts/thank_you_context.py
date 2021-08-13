from datetime import datetime
from typing import Mapping

from flask import url_for
from flask_babel import format_datetime, lazy_gettext

from app.data_models.session_data import SessionData
from app.libs.utils import convert_tx_id
from app.views.contexts.email_form_context import build_email_form_context


def build_default_thank_you_context(
    session_data: SessionData, submitted_at: datetime, survey_type: str
) -> Mapping:
    text = lazy_gettext("Your answers have been submitted for ")
    submitted_on = {
        "term": lazy_gettext("Submitted on:"),
        "descriptions": [
            {"description": format_datetime(submitted_at, format="dd LLLL yyyy HH:mm")}
        ],
    }
    submission_reference = {
        "term": lazy_gettext("Submission reference:"),
        "descriptions": [{"description": convert_tx_id(session_data.tx_id)}],
    }
    if survey_type == "social":
        submission_text = lazy_gettext("Your answers have been submitted")
        items_list = [submitted_on]
    elif session_data.trad_as and session_data.ru_name:
        submission_text = (
            f"{text}<span>{session_data.ru_name}</span> ({session_data.trad_as})"
        )
        items_list = [submitted_on, submission_reference]
    else:
        submission_text = f"{text}<span>{session_data.ru_name}</span>"
        items_list = [submitted_on, submission_reference]
    context = {
        "submitted_at": submitted_at,
        "tx_id": convert_tx_id(session_data.tx_id),
        "ru_ref": session_data.ru_ref,
        "trad_as": session_data.trad_as,
        "account_service_url": session_data.account_service_url,
        "hide_sign_out_button": True,
        "submission_text": submission_text,
        "items_list": items_list,
    }

    if session_data.period_str:
        context["period_str"] = session_data.period_str
    if session_data.ru_name:
        context["ru_name"] = session_data.ru_name

    return context


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
