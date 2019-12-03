from wtforms import FormField

from app.forms.duration_form import get_duration_form
from app.forms.handlers.string_handler import StringHandler


class DurationHandler(StringHandler):
    MANDATORY_MESSAGE = 'MANDATORY_RADIO'

    def get_field(self):
        return FormField(
            get_duration_form(self.answer, self.error_messages),
            label=self.label,
            description=self.guidance,
        )
