from datetime import datetime
from functools import cached_property

from flask_babel import LazyString, gettext
from flask_login import current_user

from app.data_models.metadata_proxy import MetadataProxy
from app.data_models.session_store import SessionStore
from app.globals import get_metadata
from app.helpers.template_helpers import get_survey_type
from app.questionnaire import QuestionnaireSchema
from app.views.contexts.thank_you_context import build_thank_you_context
from app.views.handlers.confirmation_email import (
    ConfirmationEmail,
    ConfirmationEmailLimitReached,
    ConfirmationEmailNotEnabled,
)


class ThankYou:
    DEFAULT_THANK_YOU_TEMPLATE = "thank-you"

    PAGE_TITLE = gettext("Thank you for completing the census")

    def __init__(
        self,
        schema: QuestionnaireSchema,
        session_store: SessionStore,
        submitted_at: datetime,
    ):
        self._session_store: SessionStore = session_store
        self._schema: QuestionnaireSchema = schema
        self._submitted_at = submitted_at

        # self._is_census_theme = cookie_session.get("theme") == "census"
        self.template = self.DEFAULT_THANK_YOU_TEMPLATE

    @cached_property
    def confirmation_email(self) -> ConfirmationEmail | None:
        try:
            return ConfirmationEmail(self._session_store, self._schema, self.PAGE_TITLE)
        except (ConfirmationEmailNotEnabled, ConfirmationEmailLimitReached):
            return None

    def get_context(self) -> dict:
        metadata: MetadataProxy = get_metadata(current_user)  # type: ignore

        confirmation_email_form = (
            self.confirmation_email.form if self.confirmation_email else None
        )

        guidance_content = self._schema.get_post_submission().get("guidance")
        return build_thank_you_context(
            self._schema,
            metadata,
            self._submitted_at,
            get_survey_type(),
            guidance_content,
            confirmation_email_form,
        )

    def get_page_title(self) -> str | LazyString:
        if self.confirmation_email:
            return self.confirmation_email.get_page_title()
        return self.PAGE_TITLE
