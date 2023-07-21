from functools import cached_property

from flask import current_app
from flask_babel import LazyString, gettext, lazy_gettext
from itsdangerous import BadSignature
from werkzeug.exceptions import BadRequest

from app.data_models import SessionData, SessionStore
from app.forms.email_form import EmailForm
from app.helpers import url_safe_serializer
from app.questionnaire import QuestionnaireSchema
from app.views.contexts.email_form_context import build_confirmation_email_form_context


class ConfirmationEmailNotEnabled(Exception):
    pass


class ConfirmationEmailLimitReached(Exception):
    pass


class ConfirmationEmail:
    def __init__(
        self,
        session_store: SessionStore,
        schema: QuestionnaireSchema,
        page_title: str | None = None,
        serialised_email: str | None = None,
    ):
        if not self.is_enabled(schema):
            raise ConfirmationEmailNotEnabled

        # Type ignore: session_data is populated at login therefore won't be None for confirmation email
        if self.is_limit_reached(session_store.session_data):  # type: ignore
            raise ConfirmationEmailLimitReached

        self._session_store = session_store
        self._schema = schema
        self._page_title = page_title
        self._serialised_email = serialised_email

    @property
    def page_title(self) -> str:
        return self._page_title or lazy_gettext("Confirmation email")

    @cached_property
    def form(self) -> EmailForm:
        if self._serialised_email:
            try:
                email = url_safe_serializer().loads(self._serialised_email)
            except BadSignature as exc:
                raise BadRequest from exc
            return EmailForm(email=email)
        return EmailForm()

    def get_context(self) -> dict[str, bool | str]:
        return build_confirmation_email_form_context(self.form)

    def get_url_safe_serialized_email(self) -> str | bytes:
        return url_safe_serializer().dumps(self.form.email.data)

    def get_page_title(self) -> str | LazyString | None:
        # pylint: disable=no-member
        # wtforms Form parents are not discoverable in the 2.3.3 implementation
        if self.form.errors:
            return gettext("Error: {page_title}").format(page_title=self.page_title)
        return self.page_title

    @staticmethod
    def is_limit_reached(session_data: SessionData) -> bool:
        # Type ignore: confirmation_email_count already declared an int
        return session_data.confirmation_email_count >= current_app.config["CONFIRMATION_EMAIL_LIMIT"]  # type: ignore

    @staticmethod
    def is_enabled(schema: QuestionnaireSchema) -> bool:
        if submission_schema := schema.get_post_submission():
            return submission_schema.get("confirmation_email", False)
        return False
