from decimal import Decimal, InvalidOperation

from wtforms import DecimalField

from app.helpers.form_helpers import sanitise_number


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
                self.data = Decimal(sanitise_number(valuelist[0]))
            except (ValueError, TypeError, InvalidOperation):
                pass
