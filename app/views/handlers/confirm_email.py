from functools import cached_property
from typing import Mapping

from flask import url_for
from flask_babel import gettext, lazy_gettext
from itsdangerous import BadSignature
from werkzeug.exceptions import BadRequest

from app.data_models.session_store import SessionStore
from app.forms.questionnaire_form import generate_form
from app.helpers import url_safe_serializer
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.contexts.confirm_email_form_context import build_confirm_email_context

CONFIRM_EMAIL_YES_VALUE = lazy_gettext("Yes")


class ConfirmEmail:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        session_store: SessionStore,
        serialized_email,
        form_data: Mapping,
    ):
        self._serialized_email = serialized_email

        try:
            email = url_safe_serializer().loads(self._serialized_email)
        except BadSignature:
            raise BadRequest

        self._schema = schema
        self._session_store = session_store
        self._form_data = form_data
        self._email = email
        self.page_title = "Confirm your email address"

    @cached_property
    def form(self):
        return generate_form(
            schema=self._schema,
            question_schema=self.question_schema,
            answer_store=None,
            metadata=None,
            data=None,
            form_data=self._form_data,
        )

    def get_context(self):
        return build_confirm_email_context(self.question_schema, self.form)

    def get_next_location_url(self):
        if self._form_data.get("confirm-email") == CONFIRM_EMAIL_YES_VALUE:
            return url_for(
                ".get_confirmation_email_sent",
                email=self._serialized_email,
            )
        return url_for(".send_confirmation_email", email=self._serialized_email)

    def get_page_title(self):
        if self.form.errors:
            return gettext("Error: {page_title}").format(page_title=self.page_title)
        return self.page_title

    @cached_property
    def question_schema(self):
        return {
            "type": "General",
            "id": "confirm-email",
            "title": lazy_gettext("Is this email address correct?"),
            "label": self._email,
            "answers": [
                {
                    "type": "Radio",
                    "id": "confirm-email",
                    "mandatory": True,
                    "options": [
                        {
                            "label": CONFIRM_EMAIL_YES_VALUE,
                            "value": CONFIRM_EMAIL_YES_VALUE,
                        },
                        {"label": "No", "value": "No"},
                    ],
                },
            ],
        }
