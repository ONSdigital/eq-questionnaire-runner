from decimal import Decimal

import flask_babel
from babel import Locale, numbers, units


def unit_dec(value: int | Decimal | float):
    decimal_places = len(str(value).split(".")[-1])
    locale_f = Locale.parse(flask_babel.get_locale())
    locale_format = locale_f.decimal_formats[None]
    locale_format = locale_format.number_pattern.split(".")[0]
    locale_format = f'{locale_format}.{"0" * decimal_places}'

    y = numbers.format_decimal(
        value,
        format=locale_format,
        locale="en_GB",
    )
    return y
