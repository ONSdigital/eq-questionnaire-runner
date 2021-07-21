import logging
from functools import cached_property

from wtforms import Form, FormField, StringField

logger = logging.getLogger(__name__)


def get_form_class(validators):
    class DateForm(Form):
        # Validation is only ever added to the 1 field that shows in all 3 variants
        # This is to prevent an error message for each input box
        year = StringField(validators=validators)
        month = StringField()
        day = StringField()

        @cached_property
        def data(self):
            data = super().data

            try:
                return "{year:04d}-{month:02d}-{day:02d}".format(
                    year=int(data["year"]),
                    month=int(data["month"]),
                    day=int(data["day"]),
                )
            except (TypeError, ValueError):
                return None

    return DateForm


class DateField(FormField):
    def __init__(self, validators, **kwargs):
        form_class = get_form_class(validators)
        super().__init__(form_class, **kwargs)

    def process(self, formdata, data=None):
        if data is not None:
            substrings = data.split("-")
            data = {"year": substrings[0], "month": substrings[1], "day": substrings[2]}

        super().process(formdata, data)
