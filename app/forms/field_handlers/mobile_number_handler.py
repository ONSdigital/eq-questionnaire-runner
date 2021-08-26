from functools import cached_property
from typing import Union

from wtforms import StringField

from app.forms.field_handlers.field_handler import FieldHandler
from app.forms.validators import MobileNumberCheck, ResponseRequired

MobileNumberValidators = list[Union[ResponseRequired, MobileNumberCheck]]


class MobileNumberHandler(FieldHandler):
    MANDATORY_MESSAGE_KEY = "MANDATORY_MOBILE_NUMBER"

    @cached_property
    def validators(self) -> MobileNumberValidators:
        validate_with: MobileNumberValidators = super().validators

        if not self.disable_validation:
            validate_with.append(MobileNumberCheck())

        return validate_with

    def get_field(self) -> StringField:
        return StringField(
            label=self.label, description=self.guidance, validators=self.validators
        )
