from abc import abstractmethod, ABC
from functools import cached_property

from wtforms import validators, Field

from app.data_model.answer_store import AnswerStore
from app.questionnaire.location import Location
from app.forms.validators import ResponseRequired
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
        self.question_title = question_title

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

    @staticmethod
    def format_question_title(error_message, question_title):
        error_message = error_message or ""
        if "%(question_title)s" in error_message:
            error_message = error_message % dict(question_title=question_title)
        return error_message

    def get_validation_message(self, message_key):
        message = self.answer_schema.get("validation", {}).get("messages", {}).get(
            message_key
        ) or self.error_messages.get(message_key)

        return self.format_question_title(message, self.question_title)

    def get_mandatory_validator(self):
        if self.answer_schema["mandatory"] is True:
            mandatory_message = self.get_validation_message(self.MANDATORY_MESSAGE_KEY)

            return ResponseRequired(message=mandatory_message)

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
