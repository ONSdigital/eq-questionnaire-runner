from app.forms.email_form import EmailForm
from app.globals import get_session_store
from app.helpers.url_param_serializer import URLParamSerializer
from app.views.contexts.email_form_context import build_confirmation_email_form_context


class ConfirmationEmail:
    def __init__(self):
        self.form = EmailForm()

    def get_context(self):
        return build_confirmation_email_form_context(self.form)

    def get_url_safe_serialized_email(self):
        return URLParamSerializer().dumps(self.form.email.data)

    @staticmethod
    def handle_post():
        session_store = get_session_store()
        session_store.session_data.confirmation_email_sent = True
        session_store.save()
