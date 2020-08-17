from functools import cached_property

from app.forms.field_handlers.field_handler import FieldHandler
from app.forms.fields.address_field import AddressField
from app.forms.validators import (
    OptionalForm,
    format_message_with_title,
    AddressLine1Required,
)


class AddressHandler(FieldHandler):
    MANDATORY_MESSAGE_KEY = "MANDATORY_ADDRESS"

    @cached_property
    def validators(self):
        validate_with = [OptionalForm()]

        if self.answer_schema["mandatory"] is True:
            validate_with = [
                AddressLine1Required(
                    message=self.get_validation_message(
                        format_message_with_title(
                            self.MANDATORY_MESSAGE_KEY, self.question_title
                        )
                    )
                )
            ]

        return validate_with

    def get_field(self) -> AddressField:
        return AddressField(
            self.validators, label=self.label, description=self.guidance
        )
