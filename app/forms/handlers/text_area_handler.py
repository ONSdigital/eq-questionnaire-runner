from werkzeug.utils import cached_property
from wtforms import validators

from app.forms.custom_fields import MaxTextAreaField
from app.forms.handlers.string_handler import StringHandler


class TextAreaHandler(StringHandler):
    MANDATORY_MESSAGE = 'MANDATORY_TEXTAREA'

    @cached_property
    def validators(self):
        validate_with = super().validators
        if self.disable_validation is False:
            validate_with.extend(self.get_length_validator())
        return validate_with

    def get_length_validator(self):
        validate_with = []
        max_length = StringHandler.MAX_LENGTH
        length_message = self.error_messages['MAX_LENGTH_EXCEEDED']

        if 'max_length' in self.answer and self.answer['max_length'] > 0:
            max_length = self.answer['max_length']

        if (
            'validation' in self.answer
            and 'messages' in self.answer['validation']
            and 'MAX_LENGTH_EXCEEDED' in self.answer['validation']['messages']
        ):
            length_message = self.answer['validation']['messages'][
                'MAX_LENGTH_EXCEEDED'
            ]

        validate_with.append(validators.length(-1, max_length, message=length_message))

        return validate_with

    def get_field(self):
        return MaxTextAreaField(
            label=self.label,
            description=self.guidance,
            validators=self.validators,
            maxlength=StringHandler.MAX_LENGTH,
        )
