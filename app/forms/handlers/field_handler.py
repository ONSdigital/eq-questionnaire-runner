from abc import abstractmethod, ABC

from werkzeug.utils import cached_property
from wtforms import validators

from app.data_model.answer_store import AnswerStore
from app.validation.validators import ResponseRequired


class FieldHandler(ABC):
    MANDATORY_MESSAGE = ''

    def __init__(
        self,
        answer,
        error_messages=None,
        answer_store=None,
        metadata=None,
        location=None,
        disable_validation=False,
    ):
        self.answer = answer
        self.error_messages = error_messages or {}
        self.answer_store = answer_store or AnswerStore()
        self.metadata = metadata or {}
        self.location = location
        self.disable_validation = disable_validation

    @cached_property
    def validators(self):
        if not self.disable_validation:
            return self.get_mandatory_validator(self.MANDATORY_MESSAGE)
        return []

    @cached_property
    def answer_type(self):
        return self.answer.get('type')

    @cached_property
    def label(self):
        return self.answer.get('label')

    @cached_property
    def guidance(self):
        return self.answer.get('guidance', '')

    def get_mandatory_validator(self, mandatory_message_key):
        validate_with = validators.Optional()

        if self.answer['mandatory'] is True:
            mandatory_message = self.error_messages[mandatory_message_key]

            if (
                'validation' in self.answer
                and 'messages' in self.answer['validation']
                and mandatory_message_key in self.answer['validation']['messages']
            ):
                mandatory_message = self.answer['validation']['messages'][
                    mandatory_message_key
                ]

            validate_with = ResponseRequired(message=mandatory_message)

        return [validate_with]

    @staticmethod
    def build_choices(options):
        choices = []
        for option in options:
            choices.append((option['value'], option['label']))
        return choices

    @staticmethod
    def build_choices_with_detail_answer_ids(options):
        choices = []
        for option in options:
            detail_answer_id = (
                option['detail_answer']['id'] if option.get('detail_answer') else None
            )
            choices.append((option['value'], option['label'], detail_answer_id))
        return choices

    @abstractmethod
    def get_field(self):
        pass  # pragma: no cover
