def build_email_context(email_confirmation_form):
    return {
        "form": {
            "mapped_errors": email_confirmation_form.map_errors(),
            "fields": email_confirmation_form,
            "errors": email_confirmation_form.errors,
        }
    }
