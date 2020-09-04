from app.forms.email_form import EmailForm
from app.globals import get_session_store
from app.helpers.url_param_serializer import URLParamSerializer
from app.views.contexts.email_context import build_confirmation_email_context


class ConfirmationEmail:
    def __init__(self):
        self.form_valid = False
        self.form = EmailForm()

    def get_context(self):
        return build_confirmation_email_context(self.form)

    def get_url_safe_serialized_email(self):
        url_param_serializer = URLParamSerializer()
        return url_param_serializer.dumps(self.form.email.data)

    @staticmethod
    def _update_session_data_confirmation_email_sent_to_true():
        session_store = get_session_store()
        session_store.session_data.confirmation_email_sent = True
        session_store.save()

    def handle_post(self):
        self.form_valid = self.form.validate()

        if self.form_valid:
            self._update_session_data_confirmation_email_sent_to_true()
