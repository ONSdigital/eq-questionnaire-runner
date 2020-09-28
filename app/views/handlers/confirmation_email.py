from flask import current_app
from flask_babel import gettext

from app.forms.email_form import EmailForm
from app.globals import get_session_store
from app.helpers.url_param_serializer import URLParamSerializer
from app.views.contexts.email_form_context import build_confirmation_email_form_context


class ConfirmationEmail:
    PAGE_TITLE = gettext("Confirmation email")

    def __init__(self, page_title=None):
        self.form = EmailForm()
        self.page_title = page_title or self.PAGE_TITLE

    def get_context(self):
        return build_confirmation_email_form_context(self.form)

    def get_url_safe_serialized_email(self):
        return URLParamSerializer().dumps(self.form.email.data)

    def get_page_title(self):
        if self.form.errors:
            return gettext("Error: {page_title}").format(page_title=self.page_title)
        return self.page_title

    @staticmethod
    def handle_post():
        session_store = get_session_store()
        session_store.session_data.confirmation_email_count += 1
        session_store.save()


def email_limit_exceeded():
    return (
        True
        if get_session_store().session_data.confirmation_email_count
        >= current_app.config["CONFIRMATION_EMAIL_REQUEST_LIMIT"]
        else False
    )
