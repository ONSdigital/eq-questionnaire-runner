from werkzeug.utils import cached_property
from wtforms import validators

from app.forms.fields.max_text_area_field import MaxTextAreaField
from app.forms.field_handlers.field_handler import FieldHandler


class TextAreaHandler(FieldHandler):
    MAX_LENGTH = 2000
    MANDATORY_MESSAGE_KEY = 'MANDATORY_TEXTAREA'

    @cached_property
    def validators(self):
        validate_with = super().validators
        if self.disable_validation is False:
            validate_with.append(self.get_length_validator())
        return validate_with

    @cached_property
    def max_length(self):
        if 'max_length' in self.answer_schema and self.answer_schema['max_length'] > 0:
            return self.answer_schema['max_length']
        return self.MAX_LENGTH

    def get_length_validator(self):
        length_message = self.get_validation_message('MAX_LENGTH_EXCEEDED')

        return validators.length(-1, self.max_length, message=length_message)

    def get_field(self) -> MaxTextAreaField:
        return MaxTextAreaField(
            label=self.label,
            description=self.guidance,
            validators=self.validators,
            maxlength=self.max_length,
        )
