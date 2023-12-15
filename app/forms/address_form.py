from __future__ import annotations

import logging
from functools import cached_property
from typing import Any

from wtforms import Form, HiddenField, StringField
from wtforms.validators import InputRequired

logger = logging.getLogger(__name__)

AddressValidatorTypes = list[InputRequired]


def get_address_form(
    validators: AddressValidatorTypes,
) -> Form:
    class AddressForm(Form):
        line1 = StringField(validators=validators)
        line2 = StringField()
        town = StringField()
        postcode = StringField()
        uprn = HiddenField()

        @cached_property
        def data(self) -> dict[str, Any]:
            data_: dict[str, Any] = super().data
            return data_

    return AddressForm
