from abc import ABC, abstractmethod
from functools import cached_property

from wtforms import Field, validators

from app.data_models.answer_store import AnswerStore
from app.forms.validators import ResponseRequired, format_message_with_title
from app.questionnaire import Location
from app.questionnaire.rules import get_answer_value
from app.utilities.schema import load_schema_from_metadata


class FieldHandler(ABC):
    MANDATORY_MESSAGE_KEY = ""

    def __init__(
        self,
        answer_schema: dict,
        error_messages: dict = None,
        answer_store: AnswerStore = None,
        metadata: dict = None,
        location: Location = None,
        disable_validation: bool = False,
        question_title: str = None,
    ):
        self.answer_schema = answer_schema
        self.error_messages = error_messages or {}
        self.answer_store = answer_store or AnswerStore()
        self.metadata = metadata or {}
        self.location = location
        self.disable_validation = disable_validation
        self.question_title = str(question_title)
        self.validation_messages = self.answer_schema.get("validation", {}).get(
            "messages", {}
        )

    @cached_property
    def validators(self):
        if not self.disable_validation:
            return [self.get_mandatory_validator()]
        return []

    @cached_property
    def label(self):
        return self.answer_schema.get("label")

    @cached_property
    def guidance(self):
        return self.answer_schema.get("guidance", "")

    def get_validation_message(self, message_key):
        return self.validation_messages.get(message_key) or self.error_messages.get(
            message_key
        )

    def get_mandatory_validator(self):
        if self.answer_schema["mandatory"] is True:
            mandatory_message = self.get_validation_message(self.MANDATORY_MESSAGE_KEY)

            return ResponseRequired(
                message=format_message_with_title(
                    mandatory_message, self.question_title
                )
            )

        return validators.Optional()

    def get_schema_value(self, schema_element):
        if isinstance(schema_element["value"], dict):
            if schema_element["value"]["source"] == "metadata":
                identifier = schema_element["value"].get("identifier")
                return self.metadata.get(identifier)
            if schema_element["value"]["source"] == "answers":
                schema = load_schema_from_metadata(self.metadata)
                answer_id = schema_element["value"].get("identifier")
                list_item_id = self.location.list_item_id if self.location else None

                return get_answer_value(
                    answer_id, self.answer_store, schema, list_item_id=list_item_id
                )
        return schema_element["value"]

    @abstractmethod
    def get_field(self) -> Field:
        pass  # pragma: no cover
