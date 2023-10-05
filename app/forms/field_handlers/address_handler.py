from functools import cached_property

from wtforms import FormField
from wtforms.fields.core import UnboundField
from wtforms.validators import InputRequired

from app.forms.address_form import AddressValidatorTypes, get_address_form
from app.forms.field_handlers.field_handler import FieldHandler
from app.forms.validators import format_message_with_title


class AddressHandler(FieldHandler):
    MANDATORY_MESSAGE_KEY = "MANDATORY_ADDRESS"

    @cached_property
    def validators(self) -> AddressValidatorTypes:
        validate_with: AddressValidatorTypes = []

        if self.answer_schema["mandatory"]:
            validate_with = [
                InputRequired(
                    message=self.get_validation_message(
                        format_message_with_title(
                            self.MANDATORY_MESSAGE_KEY, self.question_title
                        )
                    )
                )
            ]

        return validate_with

    def get_field(self) -> UnboundField | FormField:
        return FormField(
            get_address_form(self.validators),
            label=self.label,
            description=self.guidance,
        )
