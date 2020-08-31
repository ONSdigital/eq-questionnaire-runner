from werkzeug.exceptions import NotFound
from app.views.handlers.url_safe_serializer import URLSafeSerializerHandler
from app.forms.email_form import EmailForm
from app.globals import get_session_store
from app.views.contexts.email_context import build_email_context


class AnotherEmail:
    def __init__(self):
        if not get_session_store().session_data.email_confirmation:
            raise NotFound

        self.email_form = EmailForm()

    def get_context(self):
        return build_email_context(self.email_form)

    def validate(self):
        return self.email_form.validate_on_submit()

    def get_url_safe_serialized_email_address(self):
        url_safe_serializer_handler = URLSafeSerializerHandler()
        return url_safe_serializer_handler.dumps(self.email_form.email_address.data)
