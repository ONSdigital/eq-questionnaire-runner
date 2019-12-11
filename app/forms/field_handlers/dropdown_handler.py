from flask_babel import gettext
from wtforms import SelectField

from app.forms.field_handlers.field_handler import FieldHandler


class DropdownHandler(FieldHandler):
    MANDATORY_MESSAGE_KEY = 'MANDATORY_DROPDOWN'

    @staticmethod
    def build_choices(options: dict):
        choices = [('', gettext('Select an answer'))]
        for option in options:
            choices.append((option['value'], option['label']))
        return choices

    def get_field(self) -> SelectField:
        return SelectField(
            label=self.label,
            description=self.guidance,
            choices=self.build_choices(self.answer_schema['options']),
            default='',
            validators=self.validators,
        )
