from werkzeug.exceptions import NotFound
from app.helpers.url_safe_helper import URLSafeSerializerHelper
from app.forms.email_form import EmailForm
from app.globals import get_session_store
from app.views.contexts.email_context import build_email_context


class ConfirmationEmail:
    def __init__(self):
        if not get_session_store().session_data.confirmation_email:
            raise NotFound

        self.email_form = EmailForm()

    def get_context(self):
        return build_email_context(self.email_form)

    def validate(self):
        return self.email_form.validate_on_submit()

    def get_url_safe_serialized_email(self):
        url_safe_serializer_handler = URLSafeSerializerHelper()
        return url_safe_serializer_handler.dumps(self.email_form.email.data)
