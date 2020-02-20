from werkzeug.utils import cached_property
from app.forms.fields.max_string_field import MaxStringField
from wtforms import validators

from app.forms.field_handlers.field_handler import FieldHandler


class StringHandler(FieldHandler):
    MANDATORY_MESSAGE_KEY = "MANDATORY_TEXTFIELD"

    @cached_property
    def validators(self):
        validate_with = super().validators

        if self.disable_validation is False:
            validate_with.append(self.get_length_validator())

        return validate_with

    @cached_property
    def get_length_validator(self):
        length_message = self.get_validation_message("MAX_LENGTH_EXCEEDED")

        return validators.length(-1, self.max_length, message=length_message)

    @cached_property
    def max_length(self):
        return self.answer_schema.get("max_length", 10000)

    def get_field(self) -> MaxStringField:
        return MaxStringField(
            label=self.label,
            description=self.guidance,
            validators=self.validators,
            maxlength=self.max_length,
        )
