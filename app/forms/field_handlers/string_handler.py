from wtforms import validators
from werkzeug.utils import cached_property
from wtforms import StringField


from app.forms.field_handlers.field_handler import FieldHandler


class StringHandler(FieldHandler):
    MAX_LENGTH = 10000
    MANDATORY_MESSAGE_KEY = "MANDATORY_TEXTFIELD"

    @cached_property
    def validators(self):
        validate_with = super().validators

        if not self.disable_validation:
            validate_with.append(self.get_length_validator)

        return validate_with

    @cached_property
    def get_length_validator(self):
        length_message = self.get_validation_message("MAX_LENGTH_EXCEEDED")

        return validators.length(-1, self.max_length, message=length_message)

    @cached_property
    def max_length(self):
        max_length = self.answer_schema.get("max_length", 0)
        return max_length if max_length > 0 else self.MAX_LENGTH

    def get_field(self) -> StringField:
        return StringField(
            label=self.label, description=self.guidance, validators=self.validators
        )
