from app.forms.email_conformation_form import EmailConformationForm
from werkzeug.exceptions import MethodNotAllowed
from app.views.contexts.email_context import build_email_context
from app.globals import get_session_store

class EmailConfirmation:
    def __init__(self):
        if not get_session_store().session_data.confirmation_email_sent:
            raise MethodNotAllowed

        self.email_confirmation_form = EmailConformationForm()


    def get_context(self):
        return build_email_context(self.email_confirmation_form)

    def validate(self):
        return self.email_confirmation_form.validate_on_submit()

