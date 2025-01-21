import logging
from functools import cached_property
from typing import Any, Callable, Sequence

from werkzeug.datastructures import MultiDict
from wtforms import Form, FormField, StringField
from wtforms.utils import UnsetValue, unset_value

from app.utilities.types import DateValidatorType

logger = logging.getLogger(__name__)


def get_form_class(validators: Sequence[DateValidatorType]) -> type[Form]:
    class YearMonthDateForm(Form):
        year = StringField(validators=validators)
        month = StringField()

        @cached_property
        def data(self) -> str | None:
            data = super().data

            try:
                return f'{int(data["year"]):04d}-{int(data["month"]):02d}'
            except (TypeError, ValueError):
                return None

    return YearMonthDateForm


class MonthYearDateField(FormField):
    def __init__(
        self,
        *,
        validators: Sequence[DateValidatorType],
        **kwargs: Any,
    ) -> None:
        form_class = get_form_class(validators)
        super().__init__(
            form_class,
            **kwargs,
        )

    def process(
        self,
        formdata: MultiDict | None = None,
        data: str | UnsetValue = unset_value,
        extra_filters: Sequence[Callable] | None = None,
    ) -> None:
        if data is not unset_value:
            substrings = data.split("-")
            data = {"year": substrings[0], "month": substrings[1]}

        super().process(formdata, data)
