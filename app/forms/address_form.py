import logging
from functools import cached_property

from wtforms import Form, HiddenField, StringField

logger = logging.getLogger(__name__)


def get_address_form(validators):
    class AddressForm(Form):
        line1 = StringField(validators=validators)
        line2 = StringField()
        town = StringField()
        postcode = StringField()
        uprn = HiddenField()

        @cached_property
        def data(self):
            return super().data

    return AddressForm
