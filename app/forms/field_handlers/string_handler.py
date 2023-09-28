from functools import cached_property
from typing import Union

from wtforms import StringField, validators
from wtforms.fields.core import UnboundField
from wtforms.validators import Length

from app.forms.field_handlers.field_handler import FieldHandler

StringValidatorTypes = list[Union[validators.Optional, validators.Length]]


class StringHandler(FieldHandler):
    MAX_LENGTH = 10_000
    MANDATORY_MESSAGE_KEY = "MANDATORY_TEXTFIELD"

    @cached_property
    def validators(self) -> StringValidatorTypes:
        validate_with: StringValidatorTypes = super().validators

        if not self.disable_validation:
            validate_with.append(self.get_length_validator)

        return validate_with

    @cached_property
    def get_length_validator(self) -> Length:
        length_message = self.get_validation_message("MAX_LENGTH_EXCEEDED")

        return validators.length(-1, self.max_length, message=length_message)

    @cached_property
    def max_length(self) -> int:
        max_length: int = self.answer_schema.get("max_length", self.MAX_LENGTH)
        return max_length

    def get_field(self) -> UnboundField | StringField:
        return StringField(
            label=self.label, description=self.guidance, validators=self.validators
        )
