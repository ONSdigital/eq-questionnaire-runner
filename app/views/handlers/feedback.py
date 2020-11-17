from functools import cached_property
from typing import Mapping

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


class Feedback:
    PAGE_TITLE = lazy_gettext("Feedback")

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
            question_schema=self.question_schema,
            answer_store=None,
            metadata=None,
            data=None,
            form_data=self._form_data,
        )

    def get_context(self):
        return build_feedback_context(self.question_schema, self.form)

    def get_page_title(self):
        if self.form.errors:
            return gettext("Error: {page_title}").format(page_title=self.PAGE_TITLE)
        return self.PAGE_TITLE

    def handle_post(self):
        self._session_store.session_data.feedback_count += 1
        self._session_store.save()

    @cached_property
    def question_schema(self):
        detail_answers_option_map = {
            "C": [
                lazy_gettext("General"),
                lazy_gettext("This establishment"),
                lazy_gettext("People who live here"),
                lazy_gettext("Visitors"),
            ],
            "I": [
                lazy_gettext("General"),
                lazy_gettext("Accommodation"),
                lazy_gettext("Personal details"),
                lazy_gettext("Health"),
                lazy_gettext("Qualifications"),
                lazy_gettext("Employment"),
            ],
            "H": [
                lazy_gettext("General"),
                lazy_gettext("People who live here"),
                lazy_gettext("Visitors"),
                lazy_gettext("Household and accommodation"),
                lazy_gettext("Personal details"),
                lazy_gettext("Health"),
                lazy_gettext("Qualifications"),
                lazy_gettext("Employment"),
            ],
        }

        options = (
            {"label": value, "value": value}
            for value in detail_answers_option_map.get(self._schema.form_type or "H")
        )

        return {
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
                            "detail_answer": {
                                "type": "Dropdown",
                                "id": "feedback-type-question-category",
                                "mandatory": True,
                                "label": lazy_gettext(
                                    "For example, question not clear, answer option not relevant"
                                ),
                                "placeholder": lazy_gettext("Select an option"),
                                "validation": {
                                    "messages": {
                                        "MANDATORY_DROPDOWN": lazy_gettext(
                                            "Select an option"
                                        )
                                    }
                                },
                                "options": options,
                            },
                        },
                        {
                            "label": lazy_gettext("Page design and structure"),
                            "value": lazy_gettext("Page design and structure"),
                        },
                        {
                            "label": lazy_gettext(
                                "General feedback about this service"
                            ),
                            "value": lazy_gettext(
                                "General feedback about this service"
                            ),
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

    @staticmethod
    def is_limit_reached(session_data: SessionData) -> bool:
        return session_data.feedback_count >= current_app.config["EQ_FEEDBACK_LIMIT"]

    @staticmethod
    def is_enabled(schema: QuestionnaireSchema) -> bool:
        return schema.get_submission().get("feedback")
