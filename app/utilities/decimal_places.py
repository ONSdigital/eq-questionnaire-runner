from decimal import Decimal

import babel
from babel import Locale, numbers


def eq_format_decimal(
    value: int | Decimal | float, locale_p: Locale | str, decimal_separator: str
):
    """
    Function is used to format decimal numbers avoiding the decimal_quantization=True/False constraints and preserving the number input by the user.
    e.g 123.430 stays as 123.430 (if schema allows).
    """
    decimal_places = len(str(value).split(f"{decimal_separator}")[1])
    # set the locale_format by parsing the number pattern for the given locale and applying the number of decimal places passed through
    locale_f = Locale.parse(locale_p)
    locale_format = locale_f.decimal_formats[None]
    locale_format = locale_format.number_pattern.split(f"{decimal_separator}")[0]
    locale_format = f'{locale_format}{decimal_separator}{"0" * decimal_places}'

    formatted_number = numbers.format_decimal(
        value,
        format=locale_format,
        locale=locale_p,
    )
    return formatted_number


def eq_custom_currency(
    value: float | Decimal,
    currency: str,
    locale_p: Locale,
    schema_limit: int | None = None,
):
    decimal_separator = babel.numbers.get_decimal_symbol(locale_p)
    decimal_places = (
        len(str(value).split(f"{decimal_separator}")[1])
        if decimal_separator in str(value)
        else 0
    )

    # get local pattern
    locale = Locale.parse(locale_p)
    pattern = locale.currency_formats["standard"]

    # if schema_limit is undefined then check if there are no decimal places first, format if so. If no decimal places then format currency as a default
    if schema_limit is None:
        if decimal_places == 0:
            pattern.frac_prec = (0, 0)
            currency_digits = False
        elif decimal_places < 2:
            currency_digits = True
        else:
            pattern.frac_prec = (0, decimal_places)
            currency_digits = False
        return numbers.format_currency(
            value, currency, pattern, locale_p, currency_digits=currency_digits
        )

    # if schema_limit is less than 2 then return the value the user entered
    if schema_limit < 2:
        pattern.frac_prec = (0, decimal_places)
        return numbers.format_currency(
            value, currency, pattern, locale, currency_digits=False
        )

    if schema_limit > 2:
        if decimal_places < 2:
            currency_digits = True
        elif decimal_places == 0:
            pattern.frac_prec = (0, 0)
            currency_digits = False
        else:
            pattern.frac_prec = (0, decimal_places)
            currency_digits = False
        return numbers.format_currency(
            value, currency, pattern, locale_p, currency_digits=currency_digits
        )

    return numbers.format_currency(value, currency=currency, locale=locale_p)
