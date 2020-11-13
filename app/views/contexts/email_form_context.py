from flask import url_for


def build_confirmation_email_form_context(email_confirmation_form):
    context = {
        "hide_sign_out_button": False,
        "sign_out_url": url_for("session.get_sign_out"),
    }
    context.update(build_email_form_context(email_confirmation_form))
    return context


def build_email_form_context(email_confirmation_form):
    return {
        "form": {
            "mapped_errors": email_confirmation_form.map_errors(),
            "email_field": email_confirmation_form.email,
            "errors": email_confirmation_form.errors,
        }
    }
