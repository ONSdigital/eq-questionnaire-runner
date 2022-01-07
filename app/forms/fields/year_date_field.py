import logging
from functools import cached_property

from wtforms import Form, FormField, StringField
from wtforms.utils import unset_value

logger = logging.getLogger(__name__)


def get_form_class(validators):
    class YearDateForm(Form):
        year = StringField(validators=validators)

        @cached_property
        def data(self):
            # pylint: disable=no-member
            # wtforms Form parents are not discoverable in the 2.3.3 implementation
            data = super().data

            try:
                return f'{int(data["year"]):04d}'
            except (TypeError, ValueError):
                return None

    return YearDateForm


class YearDateField(FormField):
    def __init__(self, validators, **kwargs):
        form_class = get_form_class(validators)
        super().__init__(form_class, **kwargs)

    def process(self, formdata, data=None, extra_filters=None):
        if data is not unset_value:
            substrings = data.split("-")
            data = {"year": substrings[0]}

        super().process(formdata, data)
