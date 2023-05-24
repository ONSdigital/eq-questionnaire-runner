from babel import numbers
from wtforms import IntegerField, ValidationError

from app.forms import error_messages
from app.settings import DEFAULT_LOCALE


class IntegerFieldWithSeparator(IntegerField):
    """
    The default wtforms field coerces data to an int and raises
    cast errors outside of it's validation chain. In order to stop
    the validation chain, we create a custom field that doesn't
    raise the error and we can instead fail and stop other calls to
    further validation steps by using a separate NumberCheck and
    DecimalPlace validators
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = None

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == "NaN":
                raise ValidationError(error_messages["INVALID_NUMBER"])
            try:
                self.data = int(
                    valuelist[0]
                    .replace(numbers.get_group_symbol(DEFAULT_LOCALE), "")
                    .replace("_", "")
                )
            except ValueError:
                pass
