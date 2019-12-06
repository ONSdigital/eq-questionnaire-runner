from werkzeug.utils import cached_property
from wtforms import validators

from app.forms.custom_fields import MaxTextAreaField
from app.forms.handlers.field_handler import FieldHandler


class TextAreaHandler(FieldHandler):
    MAX_LENGTH = 2000
    MANDATORY_MESSAGE = 'MANDATORY_TEXTAREA'

    @cached_property
    def validators(self):
        validate_with = super().validators
        if self.disable_validation is False:
            validate_with.extend(self.get_length_validator())
        return validate_with

    def get_length_validator(self):
        validate_with = []
        max_length = self.MAX_LENGTH
        length_message = self.error_messages['MAX_LENGTH_EXCEEDED']

        if 'max_length' in self.answer_schema and self.answer_schema['max_length'] > 0:
            max_length = self.answer_schema['max_length']

        if (
            'validation' in self.answer_schema
            and 'messages' in self.answer_schema['validation']
            and 'MAX_LENGTH_EXCEEDED' in self.answer_schema['validation']['messages']
        ):
            length_message = self.answer_schema['validation']['messages'][
                'MAX_LENGTH_EXCEEDED'
            ]

        validate_with.append(validators.length(-1, max_length, message=length_message))

        return validate_with

    def get_field(self):
        return MaxTextAreaField(
            label=self.label,
            description=self.guidance,
            validators=self.validators,
            maxlength=self.MAX_LENGTH,
        )
