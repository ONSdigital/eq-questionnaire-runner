from typing import Any, Sequence

from wtforms import IntegerField

from app.helpers.form_helpers import sanitise_number


class IntegerFieldWithSeparator(IntegerField):
    """
    The default wtforms field coerces data to an int and raises
    cast errors outside of it's validation chain. In order to stop
    the validation chain, we create a custom field that doesn't
    raise the error and we can instead fail and stop other calls to
    further validation steps by using a separate NumberCheck and
    DecimalPlace validators
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.data: int | None = None

    def process_formdata(self, valuelist: Sequence[str] | None = None) -> None:
        if valuelist:
            try:
                self.data = int(sanitise_number(valuelist[0]))
            except ValueError:
                pass
