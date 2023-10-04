from wtforms import FormField
from wtforms.fields.core import UnboundField

from app.forms.duration_form import get_duration_form
from app.forms.field_handlers.field_handler import FieldHandler


class DurationHandler(FieldHandler):
    MANDATORY_MESSAGE_KEY = "MANDATORY_DURATION"

    def get_field(self) -> UnboundField | FormField:
        return FormField(
            get_duration_form(self.answer_schema, dict(self.error_messages)),
            label=self.label,
            description=self.guidance,
        )
