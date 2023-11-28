from datetime import datetime, timezone
from functools import cached_property
from typing import Any, Mapping, MutableMapping, Optional, Union

from flask import current_app
from flask_babel import gettext, lazy_gettext
from sdc.crypto.encrypter import encrypt
from werkzeug.datastructures import MultiDict

from app.authentication.auth_payload_versions import AuthPayloadVersion
from app.data_models import QuestionnaireStore
from app.data_models.metadata_proxy import MetadataProxy, NoMetadataException
from app.data_models.session_data import SessionData
from app.data_models.session_store import SessionStore
from app.forms.questionnaire_form import QuestionnaireForm, generate_form
from app.keys import KEY_PURPOSE_SUBMISSION
from app.questionnaire.questionnaire_schema import (
    DEFAULT_LANGUAGE_CODE,
    QuestionnaireSchema,
)
from app.submitter import GCSFeedbackSubmitter, LogFeedbackSubmitter, converter_v2
from app.submitter.converter import (
    build_collection,
    build_metadata,
    get_optional_payload_properties,
)
from app.views.contexts.feedback_form_context import build_feedback_context
from app.views.handlers.submission import get_receipting_metadata


class FeedbackNotEnabled(Exception):
    pass


class FeedbackLimitReached(Exception):
    pass


class FeedbackUploadFailed(Exception):
    pass


class Feedback:
    PAGE_TITLE: str = lazy_gettext("Feedback")

    def __init__(
        self,
        questionnaire_store: QuestionnaireStore,
        schema: QuestionnaireSchema,
        session_store: SessionStore,
        form_data: Optional[MultiDict[str, Any]],
    ):
        if not self.is_enabled(schema):
            raise FeedbackNotEnabled
        if self.is_limit_reached(session_store.session_data):  # type: ignore
            raise FeedbackLimitReached

        self._questionnaire_store = questionnaire_store
        self._schema = schema
        self._session_store = session_store
        self._form_data = form_data

    @cached_property
    def form(self) -> QuestionnaireForm:
        return generate_form(
            schema=self._schema,
            question_schema=self.question_schema,
            data_stores=self._questionnaire_store.data_stores,
            data=None,
            form_data=self._form_data,
        )

    def get_context(self) -> Mapping[str, Union[str, bool, dict]]:
        return build_feedback_context(self.question_schema, self.form)

    def get_page_title(self) -> str:
        # pylint: disable=no-member
        # wtforms Form parents are not discoverable in the 2.3.3 implementation
        if self.form.errors:
            title: str = gettext("Error: {page_title}").format(
                page_title=self.PAGE_TITLE
            )
            return title
        return self.PAGE_TITLE

    def handle_post(self) -> None:
        session_data: SessionData = self._session_store.session_data  # type: ignore
        session_data.feedback_count += 1

        metadata = self._questionnaire_store.data_stores.metadata
        if not metadata:
            raise NoMetadataException  # pragma: no cover

        case_id = metadata.case_id
        tx_id = metadata.tx_id

        # pylint: disable=no-member
        # wtforms Form parents are not discoverable in the 2.3.3 implementation
        feedback_converter = (
            FeedbackPayloadV2
            if metadata.version is AuthPayloadVersion.V2
            else FeedbackPayload
        )
        feedback_message = feedback_converter(
            metadata=metadata,
            response_metadata=self._questionnaire_store.data_stores.response_metadata,
            schema=self._schema,
            case_id=case_id,
            submission_language_code=session_data.language_code,
            feedback_count=session_data.feedback_count,
            feedback_text=self.form.data.get("feedback-text"),
            feedback_type=self.form.data.get("feedback-type"),
        )

        encrypted_message = encrypt(
            feedback_message(), current_app.eq["key_store"], KEY_PURPOSE_SUBMISSION  # type: ignore
        )

        additional_metadata = get_receipting_metadata(metadata)

        feedback_metadata = FeedbackMetadata(
            tx_id=tx_id, case_id=case_id, **additional_metadata
        )

        submitter: Union[GCSFeedbackSubmitter, LogFeedbackSubmitter] = current_app.eq["feedback_submitter"]  # type: ignore
        if not submitter.upload(feedback_metadata(), encrypted_message):
            raise FeedbackUploadFailed()

        self._session_store.save()

    @cached_property
    def question_schema(self) -> Mapping[str, Union[str, list]]:
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
                            "label": lazy_gettext("The survey questions"),
                            "value": lazy_gettext("The survey questions"),
                            "description": lazy_gettext(
                                "For example, questions not clear, answer options not relevant"
                            ),
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
        return session_data.feedback_count >= current_app.config["EQ_FEEDBACK_LIMIT"]  # type: ignore

    @staticmethod
    def is_enabled(schema: QuestionnaireSchema) -> bool:
        if submission_schema := schema.get_post_submission():
            return bool(submission_schema.get("feedback"))
        return False


class FeedbackMetadata:
    def __init__(self, case_id: str, tx_id: str, **kwargs: dict):
        self.case_id = case_id
        self.tx_id = tx_id

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __call__(self) -> dict[str, str]:
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
                "feedback_count": "7",
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
        "case_id": "c39e1246-debd-473a-894f-85c8397ba5ea",
        "case_type": "I",
        "flushed": False,
        "survey_id": "001",
        "form_type: "0007",
        "submission_language_code": "en",
        "tx_id": "5d4e1a37-ed21-440a-8c4d-3054a124a104",
        "type": "uk.gov.ons.edc.eq:feedback",
        "launch_language_code: "en",
        "submission_language_code: "en",
        "version": "0.0.1"
    }
    ```
    :param metadata: Questionnaire metadata
    :param response_metadata: Response metadata
    :param schema: QuestionnaireSchema class with populated schema json
    :param case_id: Questionnaire case id
    :param submission_language_code: Language being used at the point of feedback submission
    :param feedback_count: Number of feedback submissions attempted by the user
    :param feedback_text: Feedback text input by the user
    :param feedback_type: Type of feedback selected by the user


    :return payload: Feedback payload object
    """

    def __init__(
        self,
        metadata: MetadataProxy,
        response_metadata: MutableMapping[str, Union[str, int, list]],
        schema: QuestionnaireSchema,
        case_id: Optional[str],
        submission_language_code: Optional[str],
        feedback_count: int,
        feedback_text: str,
        feedback_type: str,
    ):
        self.metadata = metadata
        self.response_metadata = response_metadata
        self.case_id = case_id
        self.schema = schema
        self.submission_language_code = submission_language_code
        self.feedback_count = feedback_count
        self.feedback_text = feedback_text
        self.feedback_type = feedback_type

    def __call__(self) -> dict[str, Any]:
        payload = {
            "origin": "uk.gov.ons.edc.eq",
            "case_id": self.case_id,
            "submitted_at": datetime.now(tz=timezone.utc).isoformat(),
            "flushed": False,
            "collection": build_collection(self.metadata),
            "metadata": build_metadata(self.metadata),
            "survey_id": self.schema.json["survey_id"],
            "submission_language_code": (
                self.submission_language_code or DEFAULT_LANGUAGE_CODE
            ),
            "tx_id": self.metadata.tx_id,
            "type": "uk.gov.ons.edc.eq:feedback",
            "launch_language_code": self.metadata.language_code
            or DEFAULT_LANGUAGE_CODE,
            "version": "0.0.1",
        }

        optional_properties = get_optional_payload_properties(
            self.metadata, self.response_metadata
        )

        payload["data"] = {
            "feedback_text": self.feedback_text,
            "feedback_type": self.feedback_type,
            "feedback_count": str(self.feedback_count),
        }

        return payload | optional_properties


class FeedbackPayloadV2:
    """
    Create the feedback payload object for down stream processing in the following format:
    v0.0.1: https://github.com/ONSdigital/ons-schema-definitions/blob/main/examples/eq_runner_to_downstream/payload_v2/business/feedback_0_0_1.json
    v0.0.3: https://github.com/ONSdigital/ons-schema-definitions/blob/main/examples/eq_runner_to_downstream/payload_v2/business/feedback_0_0_3.json
    ```
    :param metadata: Questionnaire metadata
    :param response_metadata: Response metadata
    :param schema: QuestionnaireSchema class with populated schema json
    :param case_id: Questionnaire case id
    :param submission_language_code: Language being used at the point of feedback submission
    :param feedback_count: Number of feedback submissions attempted by the user
    :param feedback_text: Feedback text input by the user
    :param feedback_type: Type of feedback selected by the user


    :return payload: Feedback payload object
    """

    def __init__(
        self,
        metadata: MetadataProxy,
        response_metadata: MutableMapping[str, Union[str, int, list]],
        schema: QuestionnaireSchema,
        case_id: Optional[str],
        submission_language_code: Optional[str],
        feedback_count: int,
        feedback_text: str,
        feedback_type: str,
    ):
        self.metadata = metadata
        self.response_metadata = response_metadata
        self.case_id = case_id
        self.schema = schema
        self.submission_language_code = submission_language_code
        self.feedback_count = feedback_count
        self.feedback_text = feedback_text
        self.feedback_type = feedback_type

    def __call__(self) -> dict[str, Any]:
        payload = {
            "tx_id": self.metadata.tx_id,
            "type": "uk.gov.ons.edc.eq:feedback",
            "version": AuthPayloadVersion.V2.value,
            "data_version": self.schema.json["data_version"],
            "origin": "uk.gov.ons.edc.eq",
            "flushed": False,
            "submitted_at": datetime.now(tz=timezone.utc).isoformat(),
            "launch_language_code": self.metadata.language_code
            or DEFAULT_LANGUAGE_CODE,
            "submission_language_code": (
                self.submission_language_code or DEFAULT_LANGUAGE_CODE
            ),
            "collection_exercise_sid": self.metadata.collection_exercise_sid,
            "schema_name": self.metadata.schema_name,
            "case_id": self.case_id,
            "survey_metadata": {"survey_id": self.schema.json["survey_id"]},
        }

        if self.metadata.survey_metadata:
            payload["survey_metadata"] |= self.metadata.survey_metadata.data

        optional_properties = converter_v2.get_optional_payload_properties(
            self.metadata, self.response_metadata
        )

        payload["data"] = {
            "feedback_text": self.feedback_text,
            "feedback_type": self.feedback_type,
            "feedback_count": str(self.feedback_count),
        }

        return payload | optional_properties
