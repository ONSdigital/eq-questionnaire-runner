from functools import cached_property

from flask_babel import gettext

from app.forms.questionnaire_form import generate_form
from app.globals import get_session_store
from app.views.contexts.feedback_form_context import build_feedback_context


class FeedbackFormNotAccessible(Exception):
    pass


class FeedbackAlreadySent(Exception):
    pass


class Feedback:
    PAGE_TITLE = gettext("Feedback")
    QUESTION_SCHEMA = {
        "type": "General",
        "id": "feedback",
        "title": "Give feedback about this service",
        "label": "Select what feedback is about",
        "answers": [
            {
                "type": "Radio",
                "id": "feedback-type",
                "mandatory": True,
                "options": [
                    {
                        "label": "The census questions",
                        "value": "The census questions",
                        "description": "For example, question not clear, answer option not relevant",
                    },
                    {
                        "label": "Page design and structure",
                        "value": "Page design and structure",
                    },
                    {
                        "label": "General feedback about this service",
                        "value": "General feedback about this service",
                    },
                ],
                "validation": {
                    "messages": {
                        "MANDATORY_RADIO": "Select what your feedback is about"
                    }
                },
            },
            {
                "id": "feedback-text",
                "label": "Enter your comments",
                "description": "For example, question not clear, answer option not relevant",
                "rows": 8,
                "mandatory": True,
                "type": "TextArea",
                "max_length": 1000,
                "validation": {
                    "messages": {"MANDATORY_TEXTAREA": "Enter your feedback"}
                },
            },
        ],
    }

    def __init__(self, schema, form_data):
        self._schema = schema
        self._answers = None
        self._form_data = form_data
        self._session_store = get_session_store()

        if not schema.get_submission().get("feedback"):
            raise FeedbackFormNotAccessible

        if not self._session_store.session_data.submitted_time:
            raise FeedbackFormNotAccessible

        if get_session_store().session_data.feedback_sent:
            raise FeedbackAlreadySent

    @cached_property
    def form(self):
        return generate_form(
            schema=self._schema,
            question_schema=self.QUESTION_SCHEMA,
            answer_store=None,
            metadata=None,
            data=self._answers,
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
