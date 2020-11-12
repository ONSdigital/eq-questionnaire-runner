from typing import List

from flask_babel import lazy_gettext
from wtforms import SelectField

from app.forms.field_handlers.field_handler import FieldHandler


class DropdownHandler(FieldHandler):
    MANDATORY_MESSAGE_KEY = "MANDATORY_DROPDOWN"
    DEFAULT_PLACEHOLDER = lazy_gettext("Select an answer")

    def _get_placeholder_text(self) -> str:
        return self.answer_schema.get("placeholder", self.DEFAULT_PLACEHOLDER)

    def build_choices(self, options: List):
        choices = [("", self._get_placeholder_text())]
        for option in options:
            choices.append((option["value"], option["label"]))
        return choices

    def get_field(self) -> SelectField:
        return SelectField(
            label=self.label,
            description=self.guidance,
            choices=self.build_choices(self.answer_schema["options"]),
            default="",
            validators=self.validators,
        )
