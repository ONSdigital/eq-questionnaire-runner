from app.libs.utils import convert_tx_id
from app.views.contexts.email_context import build_email_context

def build_default_thank_you_context(session_data):
    context = {
        "submitted_time": session_data.submitted_time,
        "tx_id": convert_tx_id(session_data.tx_id),
        "ru_ref": session_data.ru_ref,
        "trad_as": session_data.trad_as,
        "account_service_url": session_data.account_service_url,
    }

    if session_data.period_str:
        context["period_str"] = session_data.period_str
    if session_data.ru_name:
        context["ru_name"] = session_data.ru_name

    return context


def build_census_thank_you_context(display_address, census_type, email_confirmation_form):
    context = {"display_address": display_address, "census_type": census_type}

    if email_confirmation_form:
        context.update(build_email_context(email_confirmation_form))
    return context
