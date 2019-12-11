from abc import abstractmethod, ABC

from werkzeug.utils import cached_property
from wtforms import validators, Field

from app.data_model.answer_store import AnswerStore
from app.questionnaire.location import Location
from app.validation.validators import ResponseRequired


class FieldHandler(ABC):
    MANDATORY_MESSAGE = ''

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
            return self.get_mandatory_validator()
        return []

    @cached_property
    def answer_type(self):
        return self.answer_schema.get('type')

    @cached_property
    def label(self):
        return self.answer_schema.get('label')

    @cached_property
    def guidance(self):
        return self.answer_schema.get('guidance', '')

    def get_validation_message(self, message_key):
        message = (
            self.answer_schema.get('validation', {})
            .get('messages', {})
            .get(message_key)
            or self.error_messages[message_key]
        )
        return message

    def get_mandatory_validator(self):
        validate_with = validators.Optional()

        if self.answer_schema['mandatory'] is True:
            mandatory_message = self.get_validation_message(self.MANDATORY_MESSAGE)

            validate_with = ResponseRequired(message=mandatory_message)

        return [validate_with]

    @abstractmethod
    def get_field(self) -> Field:
        pass  # pragma: no cover
