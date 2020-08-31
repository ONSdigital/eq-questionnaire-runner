from werkzeug.exceptions import NotFound
from app.globals import get_session_store
from app.views.handlers.url_safe_serializer import URLSafeSerializerHandler


class EmailConfirmation:
    def __init__(self, email_address):
        if not get_session_store().session_data.email_confirmation:
            raise NotFound

        url_safe_serializer_handler = URLSafeSerializerHandler()
        self.email_address = url_safe_serializer_handler.loads(email_address)

    def get_context(self):
        return {"email_address": self.email_address}
