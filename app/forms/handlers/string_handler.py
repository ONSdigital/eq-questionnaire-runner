from wtforms import StringField

from app.forms.handlers.field_handler import FieldHandler


class StringHandler(FieldHandler):
    MANDATORY_MESSAGE = 'MANDATORY_TEXTFIELD'

    def get_field(self):
        return StringField(
            label=self.label, description=self.guidance, validators=self.validators
        )
