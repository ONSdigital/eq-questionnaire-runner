from typing import Mapping

from flask import url_for

from app.data_models.session_data import SessionData
from app.libs.utils import convert_tx_id
from app.views.contexts.email_form_context import build_email_form_context


def build_default_thank_you_context(session_data: SessionData) -> Mapping:

    context = {
        "submitted_time": session_data.submitted_time,
        "tx_id": convert_tx_id(session_data.tx_id),
        "ru_ref": session_data.ru_ref,
        "trad_as": session_data.trad_as,
        "account_service_url": session_data.account_service_url,
        "hide_sign_out_button": True,
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
