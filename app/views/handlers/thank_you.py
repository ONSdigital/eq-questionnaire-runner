from flask import session as cookie_session
from werkzeug.exceptions import NotFound
from app.helpers.url_safe_helper import URLSafeSerializerHelper
from app.forms.email_form import EmailForm
from app.globals import get_session_store
from app.views.contexts.thank_you_context import (
    build_default_thank_you_context,
    build_census_thank_you_context,
)


class ThankYou:
    DEFAULT_THANK_YOU_TEMPLATE = "thank-you"
    CENSUS_THANK_YOU_TEMPLATE = "census-thank-you"

    CENSUS_TYPE_MAPPINGS = {
        "household": "HH",
        "communal_establishment": "CE",
        "individual": "IR",
    }

    def __init__(self, schema):
        self.session_store = get_session_store()
        self.session_data = self.session_store.session_data
        self._schema = schema

        if not self.session_data.submitted_time:
            raise NotFound

        self._is_census_theme = cookie_session.get("theme") in [
            "census",
            "census-nisra",
        ]
        self.template = (
            self.CENSUS_THANK_YOU_TEMPLATE
            if self._is_census_theme
            else self.DEFAULT_THANK_YOU_TEMPLATE
        )
        self.email_form = (
            EmailForm()
            if self._schema.get_submission().get("confirmation_email")
            else None
        )
        self.is_valid_email_form = False

    def get_context(self):
        if not self._is_census_theme:
            return build_default_thank_you_context(self.session_data)

        census_type_code = None
        for census_type in self.CENSUS_TYPE_MAPPINGS:
            if census_type in self.session_data.schema_name:
                census_type_code = self.CENSUS_TYPE_MAPPINGS[census_type]
                break

        return build_census_thank_you_context(
            self.session_data, census_type_code, self.email_form
        )

    def validate(self):
        self.is_valid_email_form = self.email_form.validate_on_submit()

    def get_url_safe_serialized_email(self):
        url_safe_serializer_handler = URLSafeSerializerHelper()
        return url_safe_serializer_handler.dumps(self.email_form.email.data)

    def handle_post(self):
        if not self.email_form:
            raise NotFound

        self.validate()

        if self.is_valid_email_form:
            self._update_session_data_confirmation_email_sent_to_true()

    def _update_session_data_confirmation_email_sent_to_true(self):
        self.session_data.confirmation_email_sent = True
        self.session_store.save()
