import logging
from functools import cached_property

from wtforms import Form, FormField, StringField

logger = logging.getLogger(__name__)


def get_form_class(validators):
    class AddressForm(Form):
        line1 = StringField(validators=validators)
        line2 = StringField()
        town = StringField()
        postcode = StringField()

        @cached_property
        def data(self):
            return super().data

    return AddressForm


class AddressField(FormField):
    def __init__(self, validators, **kwargs):
        form_class = get_form_class(validators)
        super().__init__(form_class, **kwargs)
