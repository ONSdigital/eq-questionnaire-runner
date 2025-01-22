from typing import Any

from flask import url_for

from app.forms.email_form import EmailForm


def build_confirmation_email_form_context(
    email_confirmation_form: EmailForm,
) -> dict[str, bool | str | Any]:
    return {
        "hide_sign_out_button": False,
        "sign_out_url": url_for("session.get_sign_out"),
        "form": build_email_form_context(email_confirmation_form),
    }


def build_email_form_context(email_confirmation_form: EmailForm) -> dict[str, Any]:
    return {
        "mapped_errors": email_confirmation_form.map_errors(),
        "email_field": email_confirmation_form.email,
        "errors": email_confirmation_form.errors,
    }
