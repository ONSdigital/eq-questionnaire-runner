from abc import abstractmethod, ABC

from werkzeug.utils import cached_property
from wtforms import validators, Field

from app.data_model.answer_store import AnswerStore
from app.questionnaire.location import Location
from app.forms.validators import ResponseRequired
from app.questionnaire.rules import get_answer_value, get_metadata_value
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
    ):
        self.answer_schema = answer_schema
        self.error_messages = error_messages or {}
        self.answer_store = answer_store or AnswerStore()
        self.metadata = metadata or {}
        self.location = location
        self.disable_validation = disable_validation

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
        message = self.answer_schema.get("validation", {}).get("messages", {}).get(
            message_key
        ) or self.error_messages.get(message_key)
        return message

    def get_mandatory_validator(self):
        if self.answer_schema["mandatory"] is True:
            mandatory_message = self.get_validation_message(self.MANDATORY_MESSAGE_KEY)

            return ResponseRequired(message=mandatory_message)

        return validators.Optional()

    def get_schema_value(self, schema_element):
        if "meta" in schema_element:
            return get_metadata_value(self.metadata, schema_element["meta"])
        if "value" in schema_element:
            return schema_element["value"]
        if "answer_id" in schema_element:
            schema = load_schema_from_metadata(self.metadata)
            answer_id = schema_element.get("answer_id")
            list_item_id = self.location.list_item_id if self.location else None

            return get_answer_value(
                answer_id, self.answer_store, schema, list_item_id=list_item_id
            )

    @abstractmethod
    def get_field(self) -> Field:
        pass  # pragma: no cover
