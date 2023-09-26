from __future__ import annotations

from typing import Sequence, Callable, Any, TYPE_CHECKING, TypeAlias, Generator

from wtforms import SelectMultipleField, SelectFieldBase

if TYPE_CHECKING:
    from app.forms.field_handlers.select_handlers import ChoiceType     # pragma: no cover

ChoiceWidgetRenderType: TypeAlias = tuple[str, str, bool, str | None]


class MultipleSelectFieldWithDetailAnswer(SelectMultipleField):
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
        validators: Sequence[Callable],
        **kwargs: Any,
    ) -> None:
        super().__init__(
            description=description,
            label=label,
            choices=choices,
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
            selected = self.data is not None and self.coerce(value) in self.data
            yield value, label, selected, detail_answer_id
