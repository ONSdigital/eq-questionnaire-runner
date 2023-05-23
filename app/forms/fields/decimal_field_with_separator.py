from decimal import Decimal, InvalidOperation

from babel import numbers
from wtforms import DecimalField

from app.settings import DEFAULT_LOCALE


class DecimalFieldWithSeparator(DecimalField):
    """
    The default wtforms field coerces data to an number and raises
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
            try:
                data = valuelist[0]
                if numbers.get_group_symbol(DEFAULT_LOCALE) in data:
                    data = data.replace(numbers.get_group_symbol(DEFAULT_LOCALE), "")
                try:
                    self.data = Decimal(
                        numbers.format_decimal(
                            data, locale=DEFAULT_LOCALE, group_separator=False
                        )
                    )
                except InvalidOperation:
                    self.data = Decimal(data)
            except (ValueError, TypeError, InvalidOperation):
                pass
