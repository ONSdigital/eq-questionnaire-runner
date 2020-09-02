from typing import Mapping

from flask import url_for

from app.libs.utils import convert_tx_id
from app.views.contexts.email_context import build_email_form_context
from app.data_model.session_data import SessionData


def build_default_thank_you_context(session_data: SessionData) -> Mapping:

    context = {
        "submitted_time": session_data.submitted_time,
        "tx_id": convert_tx_id(session_data.tx_id),
        "ru_ref": session_data.ru_ref,
        "trad_as": session_data.trad_as,
        "account_service_url": session_data.account_service_url,
        "hide_signout_button": True,
    }

    if session_data.period_str:
        context["period_str"] = session_data.period_str
    if session_data.ru_name:
        context["ru_name"] = session_data.ru_name

    return context


def build_census_thank_you_context(
    session_data: SessionData, census_type_code: str, email_form
) -> Mapping:

    context = {
        "display_address": session_data.display_address,
        "census_type": census_type_code,
        "hide_signout_button": False,
        "sign_out_url": url_for("session.get_sign_out"),
    }
    if email_form:
        context.update(build_email_form_context(email_form))
    return context
