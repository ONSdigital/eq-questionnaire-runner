from datetime import datetime, timezone
from functools import cached_property
from typing import Mapping, Union

from flask import current_app
from flask_babel import gettext, lazy_gettext

from app.data_models import QuestionnaireStore
from app.data_models.session_data import SessionData
from app.data_models.session_store import SessionStore
from app.forms.questionnaire_form import generate_form
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.submitter.converter import build_collection, build_metadata
from app.views.contexts.feedback_form_context import build_feedback_context

DEFAULT_LANGUAGE_CODE = "en"


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
        questionnaire_store: QuestionnaireStore,
        schema: QuestionnaireSchema,
        session_store: SessionStore,
        form_data: Mapping,
    ):
        if not self.is_enabled(schema):
            raise FeedbackNotEnabled

        if self.is_limit_reached(session_store.session_data):
            raise FeedbackLimitReached

        self._questionnaire_store = questionnaire_store
        self._schema = schema
        self._session_store = session_store
        self._form_data = form_data

    @cached_property
    def form(self):
        return generate_form(
            schema=self._schema,
            question_schema=self.question_schema,
            answer_store=self._questionnaire_store.answer_store,
            list_store=self._questionnaire_store.list_store,
            metadata=self._questionnaire_store.metadata,
            response_metadata=self._questionnaire_store.response_metadata,
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
            session_data.case_id,
            session_data.tx_id,
        )

        feedback_message = FeedbackPayload(
            self._questionnaire_store.metadata,
            self._questionnaire_store.response_metadata["started_at"],
            session_data.case_id,
            self._schema,
            session_data.feedback_count,
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
            "answers": [
                {
                    "type": "Radio",
                    "id": "feedback-type",
                    "mandatory": True,
                    "label": lazy_gettext("Select what your feedback is about"),
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
        if submission_schema := schema.get_post_submission():
            return submission_schema.get("feedback", False)
        return False


class FeedbackMetadata:
    def __init__(self, case_id, tx_id):
        self.case_id = case_id
        self.tx_id = tx_id

    def __call__(self) -> Mapping:
        return vars(self)


class FeedbackPayload:
    """
    Create the feedback payload object for down stream processing in the following format:
    ```
    {
        "collection": {
            "exercise_sid": "eedbdf46-adac-49f7-b4c3-2251807381c3",
            "schema_name": "carbon_0007",
            "period": "3003"
        },
        "data": {
                "feedback_text": "Page design feedback",
                "feedback_type": "Page design and structure",
                "feedback_count": 7,
        },
        "metadata": {
            "ref_period_end_date": "2021-03-29",
            "ref_period_start_date": "2021-03-01",
            "ru_ref": "11110000022H",
            "user_id": "d98d78eb-d23a-494d-b67c-e770399de383"
        },
        "origin": "uk.gov.ons.edc.eq",
        "submitted_at": "2021-10-12T10:41:23+00:00",
        "started_at": "2021-10-12T10:41:23+00:00",
        "case_id": "'c39e1246-debd-473a-894f-85c8397ba5ea'",
        "flushed": False,
        "survey_id": "001",
        "form_type: "0007",
        "tx_id": "5d4e1a37-ed21-440a-8c4d-3054a124a104",
        "type": "uk.gov.ons.edc.eq:feedback",
        "launch_language_code: "en",
        "submission_language_code: "en",
        "version": "0.0.1"
    }
    ```
    :param metadata: Questionnaire metadata
    :param started_at: Datetime of questionnaire start
    :param case_id: Questionnaire case id
    :param schema: QuestionnaireSchema class with populated schema json
    :param feedback_count: Number of feedback submissions attempted by the user
    :param feedback_text: Feedback text input by the user
    :param feedback_type: Type of feedback selected by the user
    :param feedback_type_question_category: Feedback question category selected by the user


    :return payload: Feedback payload object
    """

    def __init__(
        self,
        metadata: Mapping[str, Union[str, int, list]],
        started_at: str,
        case_id: str,
        schema: QuestionnaireSchema,
        feedback_count: int,
        feedback_text: str,
        feedback_type: str,
        feedback_type_question_category: str = None,
    ):
        self.metadata = metadata
        self.started_at = started_at
        self.case_id = case_id
        self.schema = schema
        self.feedback_count = feedback_count
        self.feedback_text = feedback_text
        self.feedback_type = feedback_type
        self.feedback_type_question_category = feedback_type_question_category

    def __call__(self) -> Mapping:
        payload = {
            "origin": "uk.gov.ons.edc.eq",
            "case_id": self.case_id,
            "started_at": self.started_at,
            "submitted_at": datetime.now(tz=timezone.utc).isoformat(),
            "flushed": False,
            "collection": build_collection(self.metadata),
            "metadata": build_metadata(self.metadata),
            "survey_id": self.schema.json["survey_id"],
            "tx_id": self.metadata["tx_id"],
            "type": "uk.gov.ons.edc.eq:feedback",
            "launch_language_code": self.metadata.get(
                "language_code", DEFAULT_LANGUAGE_CODE
            ),
            "version": "0.0.1",
        }

        if form_type := self.metadata.get("form_type"):
            payload["form_type"] = form_type

        payload["data"] = {
            "feedback_text": self.feedback_text,
            "feedback_type": self.feedback_type,
            "feedback_count": str(self.feedback_count),
        }

        if self.feedback_type_question_category:
            payload["data"][
                "feedback_type_question_category"
            ] = self.feedback_type_question_category

        return payload
