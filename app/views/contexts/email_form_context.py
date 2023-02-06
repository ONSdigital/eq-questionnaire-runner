from typing import Any, Union

from flask import url_for

from app.forms.email_form import EmailForm


def build_confirmation_email_form_context(
    email_confirmation_form: EmailForm,
) -> dict[str, Union[bool, str, Any]]:
    context = {
        "hide_sign_out_button": False,
        "sign_out_url": url_for("session.get_sign_out"),
    }
    context.update(build_email_form_context(email_confirmation_form))
    return context


def build_email_form_context(email_confirmation_form: EmailForm) -> dict[str, Any]:
    return {
        "form": {
            "mapped_errors": email_confirmation_form.map_errors(),
            "email_field": email_confirmation_form.email,
            "errors": email_confirmation_form.errors,
        }
    }
