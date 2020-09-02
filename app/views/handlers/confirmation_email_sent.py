from flask.helpers import url_for
from werkzeug.exceptions import NotFound
from app.globals import get_session_store
from app.helpers.url_safe_helper import URLSafeSerializerHelper


class ConfirmationEmailSent:
    def __init__(self, email):
        if not get_session_store().session_data.confirmation_email:
            raise NotFound

        url_safe_serializer_handler = URLSafeSerializerHelper()
        self.email = url_safe_serializer_handler.loads(email)

    def get_context(self):
        return {
            "email": self.email,
            "url": url_for("post_submission.get_confirmation_email"),
            "hide_signout_button": False,
            "sign_out_url": url_for("session.get_sign_out"),
        }
