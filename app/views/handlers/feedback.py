from functools import cached_property
from typing import Mapping

from flask_babel import gettext, lazy_gettext

from app.forms.questionnaire_form import generate_form
from app.globals import get_session_store
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.contexts.feedback_form_context import build_feedback_context


class FeedbackNotEnabled(Exception):
    pass


class FeedbackAlreadySent(Exception):
    pass


class Feedback:
    PAGE_TITLE = lazy_gettext("Feedback")
    QUESTION_SCHEMA = {
        "type": "General",
        "id": "feedback",
        "title": lazy_gettext("Give feedback about this service"),
        "label": lazy_gettext("Select what feedback is about"),
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
                "label": lazy_gettext("Enter your comments"),
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

    def __init__(self, schema: QuestionnaireSchema, form_data: Mapping):
        self._schema = schema

        if not schema.get_submission().get("feedback"):
            raise FeedbackNotEnabled

        self._session_store = get_session_store()
        if not self._session_store.session_data.submitted_time:
            raise FeedbackNotEnabled

        if self._session_store.session_data.feedback_sent:
            raise FeedbackAlreadySent

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
        self._session_store.session_data.feedback_sent = True
        self._session_store.save()
