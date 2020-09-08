from flask import session as cookie_session
from werkzeug.exceptions import NotFound
from app.globals import get_session_store
from app.views.contexts.thank_you_context import (
    build_census_thank_you_context,
    build_default_thank_you_context,
)
from app.views.handlers.confirmation_email import ConfirmationEmail


class ThankYou:
    DEFAULT_THANK_YOU_TEMPLATE = "thank-you"
    CENSUS_THANK_YOU_TEMPLATE = "census-thank-you"
    PAGE_TITLE = "Thank you"

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
        self.confirmation_email = (
            ConfirmationEmail(self.PAGE_TITLE)
            if self._schema.get_submission().get("confirmation_email")
            else None
        )

    def get_context(self):
        if not self._is_census_theme:
            return build_default_thank_you_context(self.session_data)

        census_type_code = None
        for census_type in self.CENSUS_TYPE_MAPPINGS:
            if census_type in self.session_data.schema_name:
                census_type_code = self.CENSUS_TYPE_MAPPINGS[census_type]
                break

        confirmation_email_form = (
            self.confirmation_email.form if self.confirmation_email else None
        )

        return build_census_thank_you_context(
            self.session_data, census_type_code, confirmation_email_form
        )

    def get_page_title(self):
        if self.confirmation_email:
            return self.confirmation_email.get_page_title()
        return self.PAGE_TITLE
