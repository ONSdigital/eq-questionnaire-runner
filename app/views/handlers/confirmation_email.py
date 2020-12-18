from dataclasses import dataclass
from functools import cached_property
from typing import Mapping, Optional

from flask import current_app
from flask_babel import gettext, lazy_gettext

from app.data_models import FulfilmentRequest, SessionData, SessionStore
from app.forms.email_form import EmailForm
from app.helpers import url_safe_serializer
from app.publisher.exceptions import PublicationFailed
from app.questionnaire import QuestionnaireSchema
from app.views.contexts.email_form_context import build_confirmation_email_form_context


class ConfirmationEmailNotEnabled(Exception):
    pass


class ConfirmationEmailLimitReached(Exception):
    pass


class ConfirmationEmailFulfilmentRequestPublicationFailed(Exception):
    pass


class ConfirmationEmail:
    def __init__(
        self,
        session_store: SessionStore,
        schema: QuestionnaireSchema,
        page_title: Optional[str] = None,
    ):

        if not self.is_enabled(schema):
            raise ConfirmationEmailNotEnabled

        if self.is_limit_reached(session_store.session_data):
            raise ConfirmationEmailLimitReached

        self._session_store = session_store
        self._schema = schema
        self._page_title = page_title

    @property
    def page_title(self):
        return self._page_title or lazy_gettext("Confirmation email")

    @cached_property
    def form(self):
        return EmailForm()

    def get_context(self):
        return build_confirmation_email_form_context(self.form)

    def get_url_safe_serialized_email(self):
        return url_safe_serializer().dumps(self.form.email.data)

    def get_page_title(self):
        if self.form.errors:
            return gettext("Error: {page_title}").format(page_title=self.page_title)
        return self.page_title

    def _publish_fulfilment_request(self):
        topic_id = current_app.config["EQ_SUBMISSION_CONFIRMATION_TOPIC_ID"]
        fulfilment_request = ConfirmationEmailFulfilmentRequest(
            self.form.email.data, self._session_store.session_data, self._schema
        )
        try:
            return current_app.eq["publisher"].publish(
                topic_id, message=fulfilment_request.message
            )
        except PublicationFailed:
            raise ConfirmationEmailFulfilmentRequestPublicationFailed

    def handle_post(self):
        self._publish_fulfilment_request()
        self._session_store.session_data.confirmation_email_count += 1
        self._session_store.save()

    @staticmethod
    def is_limit_reached(session_data: SessionData) -> bool:
        return (
            session_data.confirmation_email_count
            >= current_app.config["CONFIRMATION_EMAIL_LIMIT"]
        )

    @staticmethod
    def is_enabled(schema: QuestionnaireSchema):
        return schema.get_submission().get("confirmation_email")


@dataclass
class ConfirmationEmailFulfilmentRequest(FulfilmentRequest):
    email_address: str
    session_data: SessionData
    schema: QuestionnaireSchema

    def _payload(self) -> Mapping:
        return {
            "fulfilmentRequest": {
                "email_address": self.email_address,
                "form_type": self.schema.form_type,
                "region_code": self.schema.region_code,
                "questionnaire_id": self.session_data.questionnaire_id,
                "tx_id": self.session_data.tx_id,
                "language_code": self.session_data.language_code,
                "display_address": self.session_data.display_address,
                "submitted_at": self.session_data.submitted_time,
            }
        }
