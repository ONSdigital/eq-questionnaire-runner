import logging
from functools import cached_property
from typing import Sequence, Callable, Any

from werkzeug.datastructures import MultiDict
from wtforms import Form, FormField, StringField
from wtforms.utils import unset_value, UnsetValue

logger = logging.getLogger(__name__)


def get_form_class(validators: Sequence[Callable]) -> Form:
    class DateForm(Form):
        # Validation is only ever added to the 1 field that shows in all 3 variants
        # This is to prevent an error message for each input box
        year = StringField(validators=validators)
        month = StringField()
        day = StringField()

        @cached_property
        def data(self) -> str | None:
            # pylint: disable=no-member
            # wtforms Form parents are not discoverable in the 2.3.3 implementation
            data = super().data

            try:
                return f'{int(data["year"]):04d}-{int(data["month"]):02d}-{int(data["day"]):02d}'
            except (TypeError, ValueError):
                return None

    return DateForm


class DateField(FormField):
    def __init__(
        self,
        *,
        validators: Sequence[Callable],
        label: str | None = None,
        description: str,
        **kwargs: Any
    ) -> None:
        form_class = get_form_class(validators)
        super().__init__(
            form_class,
            label=label,
            description=description,
            **kwargs,
        )

    def process(
        self,
        formdata: MultiDict | None = None,
        data: UnsetValue = unset_value,
        extra_filters: None = None
    ) -> None:
        if data is not unset_value:
            substrings = data.split("-")
            data = {"year": substrings[0], "month": substrings[1], "day": substrings[2]}

        super().process(formdata, data)
