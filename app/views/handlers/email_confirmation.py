from werkzeug.exceptions import NotFound
from app.forms.email_conformation_form import EmailConformationForm
from app.globals import get_session_store
from app.views.contexts.email_context import build_email_context


class EmailConfirmation:
    def __init__(self):
        if not get_session_store().session_data.email_confirmation_sent:
            raise NotFound

        self.email_confirmation_form = EmailConformationForm()

    def get_context(self):
        return build_email_context(self.email_confirmation_form)

    def validate(self):
        return self.email_confirmation_form.validate_on_submit()
