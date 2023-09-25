from __future__ import annotations

from typing import Any, Callable, Sequence, Generator, TypeAlias, TYPE_CHECKING

from wtforms import SelectField, SelectFieldBase
from wtforms.validators import ValidationError

if TYPE_CHECKING:
    from app.forms.field_handlers.select_handlers import ChoiceType

ChoiceWidgetRenderType: TypeAlias = tuple[str, str, bool, str | None]


class SelectFieldWithDetailAnswer(SelectField):
    """
    This custom field allows us to add the additional detail_answer_id to choices/options.
    This saves us having to later map options with their detail_answer.
    """
    def __init__(
        self,
        *,
        description: str,
        label: str | None = None,
        choices: Sequence[ChoiceType],
        coerce: Callable[[str | None], str | None],
        validators: Sequence[Callable],
        **kwargs: Any
    ) -> None:
        super().__init__(
            description=description,
            label=label,
            choices=choices,
            coerce=coerce,
            validators=validators,
            **kwargs
        )

    def __iter__(self) -> Generator[SelectFieldBase._Option, None, None]:
        opts = {
            "widget": self.option_widget,
            "name": self.name,
            "_form": None,
            "_meta": self.meta,
        }
        for i, (value, label, checked, detail_answer_id) in enumerate(
            self.iter_choices()
        ):
            opt = self._Option(label=label, id=f"{self.id}-{i}", **opts)
            opt.process(None, value)
            opt.detail_answer_id = detail_answer_id
            opt.checked = checked
            yield opt

    def iter_choices(self) -> Generator[ChoiceWidgetRenderType, None, None]:
        for value, label, detail_answer_id in self.choices:
            yield value, label, self.coerce(value) == self.data, detail_answer_id

    def pre_validate(self, _: Any) -> None:
        for _, _, match, _ in self.iter_choices():
            if match:
                break
        else:
            raise ValidationError(self.gettext("Not a valid choice."))
