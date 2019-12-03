from flask_babel import gettext
from wtforms import SelectField

from app.forms.handlers.string_handler import StringHandler


class DropdownHandler(StringHandler):
    MANDATORY_MESSAGE = 'MANDATORY_DROPDOWN'

    def get_field(self):
        return SelectField(
            label=self.label,
            description=self.guidance,
            choices=[('', gettext('Select an answer'))]
            + self.build_choices(self.answer['options']),
            default='',
            validators=self.validators,
        )
