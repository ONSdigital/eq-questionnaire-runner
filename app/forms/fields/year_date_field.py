import logging
from functools import cached_property

from wtforms import Form, FormField, StringField

logger = logging.getLogger(__name__)


def get_form_class(validators):
    class YearDateForm(Form):
        year = StringField(validators=validators)

        @cached_property
        def data(self):
            data = super().data

            try:
                return "{year:04d}".format(year=int(data["year"]))
            except (TypeError, ValueError):
                return None

    return YearDateForm


class YearDateField(FormField):
    def __init__(self, validators, **kwargs):
        form_class = get_form_class(validators)
        super().__init__(form_class, **kwargs)

    def process(self, formdata, data=None):
        if data is not None:
            substrings = data.split("-")
            data = {"year": substrings[0]}

        super().process(formdata, data)
