from functools import cached_property
from typing import Sequence, Union

from wtforms import validators
from wtforms.fields.core import UnboundField
from wtforms.validators import Length

from app.forms.field_handlers.field_handler import FieldHandler
from app.forms.fields import MaxTextAreaField
from app.utilities.types import TextAreaValidatorType


class TextAreaHandler(FieldHandler):
    MAX_LENGTH = 2000
    DEFAULT_ROWS = 8
    MANDATORY_MESSAGE_KEY = "MANDATORY_TEXTAREA"

    @cached_property
    def validators(self) -> list[TextAreaValidatorType]:
        validate_with: list[TextAreaValidatorType] = super().validators
        if self.disable_validation is False:
            validate_with.append(self.get_length_validator())
        return validate_with

    @cached_property
    def max_length(self) -> int:
        max_length: int = self.answer_schema.get("max_length", 0)
        return max_length if max_length > 0 else self.MAX_LENGTH

    def get_length_validator(self) -> Length:
        length_message = self.get_validation_message("MAX_LENGTH_EXCEEDED")

        return validators.length(-1, self.max_length, message=length_message)

    def get_field(self) -> UnboundField | MaxTextAreaField:
        return MaxTextAreaField(
            label=self.label,
            description=self.guidance,
            validators=self.validators,
            rows=self.answer_schema.get("rows", self.DEFAULT_ROWS),
            maxlength=self.max_length,
        )
