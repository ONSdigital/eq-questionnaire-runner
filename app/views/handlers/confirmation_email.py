import json
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from dateutil.tz import tzutc
from flask import current_app
from flask_babel import gettext, lazy_gettext

from app.data_models.session_data import SessionData
from app.data_models.session_store import SessionStore
from app.forms.email_form import EmailForm
from app.globals import get_session_store
from app.helpers.url_param_serializer import URLParamSerializer
from app.publisher.exceptions import PublicationFailed
from app.questionnaire import QuestionnaireSchema
from app.utilities.schema import load_schema_from_session_data
from app.views.contexts.email_form_context import build_confirmation_email_form_context


class ConfirmationEmailLimitReached(Exception):
    pass


class ConfirmationEmailFulfilmentRequestFailed(Exception):
    pass


class ConfirmationEmail:
    def __init__(self, page_title=None, schema=None):
        self._session_store: SessionStore = get_session_store()
        self._session_data: SessionData = self._session_store.session_data

        if self._is_limit_reached():
            raise ConfirmationEmailLimitReached

        self.form: EmailForm = EmailForm()
        self.page_title: str = page_title or lazy_gettext("Confirmation email")
        self._schema: QuestionnaireSchema = schema or load_schema_from_session_data(
            self._session_data
        )

    def get_context(self):
        return build_confirmation_email_form_context(self.form)

    def get_url_safe_serialized_email(self):
        return URLParamSerializer().dumps(self.form.email.data)

    def get_page_title(self):
        if self.form.errors:
            return gettext("Error: {page_title}").format(page_title=self.page_title)
        return self.page_title

    def _publish_fulfilment_request(self):
        topic_id = current_app.config["EQ_SUBMISSION_CONFIRMATION_TOPIC_ID"]
        fulfilment_request = ConfirmationEmailFulfilmentRequest(
            self.form.email.data, self._session_data, self._schema
        )
        try:
            return current_app.eq["publisher"].publish(
                topic_id, message=fulfilment_request.payload
            )
        except PublicationFailed:
            raise ConfirmationEmailFulfilmentRequestFailed

    def handle_post(self):
        self._publish_fulfilment_request()
        self._session_store.session_data.confirmation_email_count += 1
        self._session_store.save()

    def _is_limit_reached(self):
        return (
            self._session_data.confirmation_email_count
            >= current_app.config["CONFIRMATION_EMAIL_LIMIT"]
        )


@dataclass
class ConfirmationEmailFulfilmentRequest:
    email_address: str
    session_data: SessionData
    schema: QuestionnaireSchema

    @property
    def payload(self):
        message = {
            "email_address": self.email_address,
            "form_type": self.schema.form_type,
            "region_code": self.schema.region_code,
            "questionnaire_id": self.session_data.questionnaire_id,
            "tx_id": self.session_data.tx_id,
            "language_code": self.session_data.language_code,
            "display_address": self.session_data.display_address,
            "submitted_at": self.session_data.submitted_time,
            "datetime": datetime.now(tzutc()).isoformat(),
            "id": str(uuid4()),
        }

        return json.dumps(message).encode("utf-8")
