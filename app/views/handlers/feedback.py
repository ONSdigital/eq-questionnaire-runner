from functools import cached_property
from typing import Mapping
from uuid import uuid4

from flask import current_app
from flask_babel import gettext, lazy_gettext

from app.data_models.session_data import SessionData
from app.data_models.session_store import SessionStore
from app.forms.questionnaire_form import generate_form
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.contexts.feedback_form_context import build_feedback_context


class FeedbackNotEnabled(Exception):
    pass


class FeedbackLimitReached(Exception):
    pass


class FeedbackUploadFailed(Exception):
    pass


class Feedback:
    PAGE_TITLE = lazy_gettext("Feedback")
    QUESTION_SCHEMA = {
        "type": "General",
        "id": "feedback",
        "title": lazy_gettext("Give feedback about this service"),
        "label": lazy_gettext("Select what your feedback is about"),
        "answers": [
            {
                "type": "Radio",
                "id": "feedback-type",
                "mandatory": True,
                "options": [
                    {
                        "label": lazy_gettext("The census questions"),
                        "value": lazy_gettext("The census questions"),
                        "description": lazy_gettext(
                            "For example, question not clear, answer option not relevant"
                        ),
                    },
                    {
                        "label": lazy_gettext("Page design and structure"),
                        "value": lazy_gettext("Page design and structure"),
                    },
                    {
                        "label": lazy_gettext("General feedback about this service"),
                        "value": lazy_gettext("General feedback about this service"),
                    },
                ],
                "validation": {
                    "messages": {
                        "MANDATORY_RADIO": lazy_gettext(
                            "Select what your feedback is about"
                        )
                    }
                },
            },
            {
                "id": "feedback-text",
                "label": lazy_gettext("Enter your feedback"),
                "description": lazy_gettext(
                    "Do not include confidential information, such as your contact details."
                ),
                "rows": 8,
                "mandatory": True,
                "type": "TextArea",
                "max_length": 1000,
                "validation": {
                    "messages": {
                        "MANDATORY_TEXTAREA": lazy_gettext("Enter your feedback")
                    }
                },
            },
        ],
    }

    def __init__(
        self,
        schema: QuestionnaireSchema,
        session_store: SessionStore,
        form_data: Mapping,
    ):
        if not self.is_enabled(schema):
            raise FeedbackNotEnabled

        if self.is_limit_reached(session_store.session_data):
            raise FeedbackLimitReached

        self._schema = schema
        self._session_store = session_store
        self._form_data = form_data

    @cached_property
    def form(self):
        return generate_form(
            schema=self._schema,
            question_schema=self.QUESTION_SCHEMA,
            answer_store=None,
            metadata=None,
            data=None,
            form_data=self._form_data,
        )

    def get_context(self):
        return build_feedback_context(self.QUESTION_SCHEMA, self.form)

    def get_page_title(self):
        if self.form.errors:
            return gettext("Error: {page_title}").format(page_title=self.PAGE_TITLE)
        return self.PAGE_TITLE

    def handle_post(self):
        session_data = self._session_store.session_data
        self._session_store.session_data.feedback_count += 1

        data = {
            "feedback_text": self.form.data["feedback-type"],
            "feedback_topic": self.form.data["feedback-text"],
        }
        metadata = {
            "feedback_count": session_data.feedback_count,
            "form_type": self._schema.form_type,
            "language_code": session_data.language_code,
            "object_key": str(uuid4()),
            "region_code": self._schema.region_code,
            "tx_id": session_data.tx_id,
        }

        feedback_upload = current_app.eq["feedback"].upload(data, metadata)

        if not feedback_upload:
            raise FeedbackUploadFailed()

        self._session_store.save()

    @staticmethod
    def is_limit_reached(session_data: SessionData) -> bool:
        return session_data.feedback_count >= current_app.config["EQ_FEEDBACK_LIMIT"]

    @staticmethod
    def is_enabled(schema: QuestionnaireSchema) -> bool:
        return schema.get_submission().get("feedback")
