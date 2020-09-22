from functools import cached_property

from wtforms import StringField

from app.forms.field_handlers.field_handler import FieldHandler
from app.forms.validators import MobileNumberCheck


class MobileNumberHandler(FieldHandler):
    MANDATORY_MESSAGE_KEY = "MANDATORY_MOBILE_NUMBER"

    @cached_property
    def validators(self):
        validate_with = super().validators

        if not self.disable_validation:
            validate_with.append(MobileNumberCheck())

        return validate_with

    def get_field(self) -> StringField:
        return StringField(
            label=self.label, description=self.guidance, validators=self.validators
        )
