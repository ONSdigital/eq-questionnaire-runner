from functools import cached_property

from flask import session as cookie_session
from flask_babel import gettext

from app.data_models.session_store import SessionStore
from app.questionnaire import QuestionnaireSchema
from app.views.contexts.thank_you_context import (
    build_census_thank_you_context,
    build_default_thank_you_context,
)
from app.views.handlers.confirmation_email import (
    ConfirmationEmail,
    ConfirmationEmailLimitReached,
    ConfirmationEmailNotEnabled,
)


class ThankYou:
    DEFAULT_THANK_YOU_TEMPLATE = "thank-you"
    CENSUS_THANK_YOU_TEMPLATE = "census-thank-you"
    PAGE_TITLE = gettext("Thank you for completing the census")

    def __init__(self, schema: QuestionnaireSchema, session_store: SessionStore):
        self._session_store: SessionStore = session_store
        self._schema: QuestionnaireSchema = schema

        self._is_census_theme = cookie_session.get("theme") in [
            "census",
            "census-nisra",
        ]
        self.template = (
            self.CENSUS_THANK_YOU_TEMPLATE
            if self._is_census_theme
            else self.DEFAULT_THANK_YOU_TEMPLATE
        )

    @cached_property
    def confirmation_email(self):
        try:
            return ConfirmationEmail(self._session_store, self._schema, self.PAGE_TITLE)
        except (ConfirmationEmailNotEnabled, ConfirmationEmailLimitReached):
            return None

    def get_context(self):
        if not self._is_census_theme:
            return build_default_thank_you_context(self._session_store.session_data)

        confirmation_email_form = (
            self.confirmation_email.form if self.confirmation_email else None
        )

        return build_census_thank_you_context(
            self._session_store.session_data,
            confirmation_email_form,
            self._schema.form_type,
        )

    def get_page_title(self):
        if self.confirmation_email:
            return self.confirmation_email.get_page_title()
        return self.PAGE_TITLE
