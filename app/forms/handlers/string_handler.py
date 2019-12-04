from werkzeug.utils import cached_property
from wtforms import validators, StringField

from app.validation.validators import ResponseRequired


class StringHandler:
    MAX_LENGTH = 2000
    MANDATORY_MESSAGE = 'MANDATORY_TEXTFIELD'

    def __init__(
        self,
        answer,
        error_messages,
        answer_store,
        metadata,
        location=None,
        disable_validation=False,
    ):
        self.answer = answer
        self.error_messages = error_messages
        self.answer_store = answer_store
        self.metadata = metadata
        self.location = location
        self.disable_validation = disable_validation

    @cached_property
    def validators(self):
        if self.disable_validation is False:
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

    def get_field(self):
        return StringField(
            label=self.label, description=self.guidance, validators=self.validators
        )
