from dataclasses import dataclass
from functools import cached_property
from typing import Mapping

from flask import current_app, url_for
from flask_babel import gettext, lazy_gettext
from itsdangerous import BadSignature
from markupsafe import escape
from werkzeug.exceptions import BadRequest

from app.cloud_tasks.exceptions import CloudTaskCreationFailed
from app.data_models import (
    FulfilmentRequest,
    QuestionnaireStore,
    SessionData,
    SessionStore,
)
from app.data_models.metadata_proxy import MetadataProxy
from app.forms.questionnaire_form import generate_form
from app.helpers import url_safe_serializer
from app.questionnaire import QuestionnaireSchema, QuestionSchemaType
from app.settings import (
    EQ_SUBMISSION_CONFIRMATION_CLOUD_FUNCTION_NAME,
    EQ_SUBMISSION_CONFIRMATION_QUEUE,
)
from app.views.contexts.confirm_email_context import build_confirm_email_context
from app.views.handlers.confirmation_email import (
    ConfirmationEmail,
    ConfirmationEmailLimitReached,
    ConfirmationEmailNotEnabled,
)


class ConfirmationEmailFulfilmentRequestPublicationFailed(Exception):
    pass


CONFIRM_EMAIL_YES_VALUE = lazy_gettext("Yes, send the confirmation email")


class ConfirmEmail:
    def __init__(
        self,
        questionnaire_store: QuestionnaireStore,
        schema: QuestionnaireSchema,
        session_store: SessionStore,
        serialized_email,
        form_data: Mapping,
    ):
        if not ConfirmationEmail.is_enabled(schema):
            raise ConfirmationEmailNotEnabled

        if ConfirmationEmail.is_limit_reached(session_store.session_data):  # type: ignore
            raise ConfirmationEmailLimitReached

        self._serialized_email = serialized_email

        try:
            email = url_safe_serializer().loads(self._serialized_email)
        except BadSignature as exc:
            raise BadRequest from exc

        self._questionnaire_store = questionnaire_store
        self._schema = schema
        self._session_store = session_store
        self._form_data = form_data
        self._email = email
        self.page_title = lazy_gettext("Confirm your email address")

    @cached_property
    def form(self):
        return generate_form(
            schema=self._schema,
            question_schema=self.question_schema,
            answer_store=self._questionnaire_store.answer_store,
            list_store=self._questionnaire_store.list_store,
            metadata=self._questionnaire_store.metadata,
            response_metadata=self._questionnaire_store.metadata,
            data=None,
            form_data=self._form_data,
            progress_store=self._questionnaire_store.progress_store,
            supplementary_data_store=self._questionnaire_store.supplementary_data_store,
        )

    @cached_property
    def question_schema(self) -> QuestionSchemaType:
        return {
            "type": "General",
            "id": "confirm-email",
            "title": lazy_gettext("Is this email address correct?"),
            "description": escape(self._email),
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
                        {
                            "label": lazy_gettext("No, I need to change it"),
                            "value": lazy_gettext("No, I need to change it"),
                        },
                    ],
                },
            ],
        }

    @cached_property
    def is_email_correct(self):
        return self._form_data.get("confirm-email") == CONFIRM_EMAIL_YES_VALUE

    def get_context(self):
        return build_confirm_email_context(self.question_schema, self.form)

    def get_next_location_url(self):
        if self.is_email_correct:
            return url_for(
                ".get_confirmation_email_sent",
                email=self._serialized_email,
            )
        return url_for(".send_confirmation_email", email=self._serialized_email)

    def get_page_title(self):
        # pylint: disable=no-member
        # wtforms Form parents are not discoverable in the 2.3.3 implementation
        if self.form.errors:
            return gettext("Error: {page_title}").format(page_title=self.page_title)
        return self.page_title

    def handle_post(self):
        if self.is_email_correct:
            self._publish_fulfilment_request()
            self._session_store.session_data.confirmation_email_count += 1
            self._session_store.save()

    def _publish_fulfilment_request(self):
        fulfilment_request = ConfirmationEmailFulfilmentRequest(
            self._email,
            self._session_store.session_data,
            self._questionnaire_store.metadata,
            self._schema,
        )

        try:
            return current_app.eq["cloud_tasks"].create_task(
                body=fulfilment_request.message,
                queue_name=EQ_SUBMISSION_CONFIRMATION_QUEUE,
                function_name=EQ_SUBMISSION_CONFIRMATION_CLOUD_FUNCTION_NAME,
                fulfilment_request_transaction_id=fulfilment_request.transaction_id,
            )
        except CloudTaskCreationFailed as exc:
            raise ConfirmationEmailFulfilmentRequestPublicationFailed from exc


@dataclass
class ConfirmationEmailFulfilmentRequest(FulfilmentRequest):
    email_address: str
    session_data: SessionData
    metadata: MetadataProxy
    schema: QuestionnaireSchema

    def _payload(self) -> Mapping:
        return {
            "fulfilmentRequest": {
                "email_address": self.email_address,
                "display_address": self.metadata["display_address"],
                "form_type": self.schema.form_type,
                "language_code": self.session_data.language_code,
                "region_code": self.schema.region_code,
                "tx_id": self.metadata.tx_id,
            }
        }
