from wtforms import StringField

from app.forms.field_handlers.field_handler import FieldHandler


class StringHandler(FieldHandler):
    MANDATORY_MESSAGE_KEY = 'MANDATORY_TEXTFIELD'

    def get_field(self) -> StringField:
        return StringField(
            label=self.label, description=self.guidance, validators=self.validators
        )
