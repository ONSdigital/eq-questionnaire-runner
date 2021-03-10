from werkzeug.datastructures import MultiDict

from app.forms.email_form import EmailForm
from tests.app.app_context_test_case import AppContextTestCase


class TestEmailForm(AppContextTestCase):
    def test_email_filters_strip(self):
        with self._app.test_request_context():
            email_form = EmailForm(MultiDict({"email": " email@example.com "}))

            assert email_form.email.data == "email@example.com"
