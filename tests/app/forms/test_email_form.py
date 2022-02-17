from werkzeug.datastructures import MultiDict

from app.forms.email_form import EmailForm


def test_email_filters_strip(app):
    with app.test_request_context():
        email_form = EmailForm(MultiDict({"email": " email@example.com "}))

        assert email_form.email.data == "email@example.com"
