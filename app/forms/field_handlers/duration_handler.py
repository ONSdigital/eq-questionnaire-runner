from wtforms import FormField

from app.forms.duration_form import get_duration_form
from app.forms.field_handlers.field_handler import FieldHandler


class DurationHandler(FieldHandler):
    MANDATORY_MESSAGE = 'MANDATORY_RADIO'

    def get_field(self) -> FormField:
        return FormField(
            get_duration_form(self.answer_schema, self.error_messages),
            label=self.label,
            description=self.guidance,
        )
