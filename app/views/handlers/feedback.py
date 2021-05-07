from datetime import datetime
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


class FeedbackUploadFailed(Exception):
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
        session_data = self._session_store.session_data
        session_data.feedback_count += 1

        feedback_metadata = FeedbackMetadata(
            session_data.feedback_count,
            self._schema.form_type,
            session_data.language_code,
            self._schema.region_code,
            session_data.tx_id,
        )

        feedback_message = FeedbackPayload(
            self.form.data.get("feedback-text"),
            self.form.data.get("feedback-type"),
            self.form.data.get("feedback-type-question-category"),
        )

        if not current_app.eq["feedback_submitter"].upload(
            feedback_metadata(), feedback_message()
        ):
            raise FeedbackUploadFailed()

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
                            "description": lazy_gettext(
                                "For example, questions not clear, answer options not relevant"
                            ),
                            "detail_answer": {
                                "type": "Dropdown",
                                "id": "feedback-type-question-category",
                                "mandatory": True,
                                "label": lazy_gettext("Question topic"),
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
                        "Do not include confidential information, such as your contact details"
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
        if submission_schema := schema.get_submission():
            return submission_schema.get("feedback", False)
        return False


class FeedbackMetadata:
    def __init__(self, feedback_count, form_type, language_code, region_code, tx_id):
        self.feedback_count = feedback_count
        self.feedback_submission_date = datetime.utcnow().strftime("%Y-%m-%d")
        self.form_type = form_type
        self.language_code = language_code
        self.region_code = region_code
        self.tx_id = tx_id

    def __call__(self) -> Mapping:
        return vars(self)


class FeedbackPayload:
    def __init__(
        self,
        feedback_text,
        feedback_type,
        feedback_type_question_category=None,
    ):
        self.feedback_text = feedback_text
        self.feedback_type = feedback_type
        self.feedback_type_question_category = feedback_type_question_category

    def __call__(self) -> Mapping:
        payload = vars(self)
        if not self.feedback_type_question_category:
            del payload["feedback_type_question_category"]

        return payload
