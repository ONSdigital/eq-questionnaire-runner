from functools import cached_property
from typing import List

from app.forms.field_handlers.field_handler import FieldHandler
from app.forms.fields import AddressField
from app.forms.validators import AddressLine1Required, format_message_with_title


class AddressHandler(FieldHandler):
    MANDATORY_MESSAGE_KEY = "MANDATORY_ADDRESS"

    @cached_property
    def validators(self) -> List:
        validate_with: List = []

        if self.answer_schema["mandatory"]:
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
