from typing import Sequence

from flask_babel import lazy_gettext
from wtforms import SelectField

from app.forms.field_handlers.select_handlers import (
    Choice,
    ChoiceWithDetailAnswer,
    SelectHandlerBase,
)


class DropdownHandler(SelectHandlerBase):
    MANDATORY_MESSAGE_KEY = "MANDATORY_DROPDOWN"
    DEFAULT_PLACEHOLDER = lazy_gettext("Select an answer")

    @property
    def choices(self) -> Sequence[Choice]:
        _choices: list[ChoiceWithDetailAnswer] = (
            self._build_dynamic_choices() + self._build_static_choices()
        )

        return [
            Choice("", self._get_placeholder_text()),
            *(Choice(i.value, i.label) for i in _choices),
        ]

    def _get_placeholder_text(self) -> str:
        return self.answer_schema.get("placeholder", self.DEFAULT_PLACEHOLDER)

    def get_field(self) -> SelectField:
        return SelectField(
            label=self.label,
            description=self.guidance,
            choices=self.choices,
            default="",
            validators=self.validators,
        )
