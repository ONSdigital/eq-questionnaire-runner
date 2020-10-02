from flask import session as cookie_session
from flask_babel import gettext
from werkzeug.exceptions import NotFound

from app.globals import get_session_store
from app.views.contexts.thank_you_context import (
    build_census_thank_you_context,
    build_default_thank_you_context,
)
from app.views.handlers.confirmation_email import (
    ConfirmationEmail,
    ConfirmationEmailLimitReached,
)


class ThankYou:
    DEFAULT_THANK_YOU_TEMPLATE = "thank-you"
    CENSUS_THANK_YOU_TEMPLATE = "census-thank-you"
    PAGE_TITLE = gettext("Thank you")

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
        self.confirmation_email = self._get_confirmation_email()

    def _get_confirmation_email(self):
        if not self._schema.get_submission().get("confirmation_email"):
            return None

        try:
            return ConfirmationEmail(self.PAGE_TITLE)
        except ConfirmationEmailLimitReached:
            return None

    def get_context(self):
        if not self._is_census_theme:
            return build_default_thank_you_context(self.session_data)

        confirmation_email_form = (
            self.confirmation_email.form if self.confirmation_email else None
        )

        return build_census_thank_you_context(
            self.session_data, confirmation_email_form
        )

    def get_page_title(self):
        if self.confirmation_email:
            return self.confirmation_email.get_page_title()
        return self.PAGE_TITLE
