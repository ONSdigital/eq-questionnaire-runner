from decimal import Decimal
from typing import Literal, TypeAlias

import flask_babel
from babel import Locale, numbers, units
from babel.numbers import get_currency_precision

UnitLengthType: TypeAlias = Literal["short", "long", "narrow"]


def custom_format_decimal(value: int | Decimal | float, locale: Locale | str) -> str:
    """
    This function provides a wrapper for the numbers `format_decimal` method, generating the
    number format (including the desired number of decimals), based on the value entered by the user and
    the locale.
    """
    number_format = get_number_format(value, locale)

    return numbers.format_decimal(
        value,
        format=number_format,
        locale=locale,
    )


def get_formatted_currency(
    *,
    value: float | Decimal,
    currency: str = "GBP",
    locale: str | None = None,
    decimal_limit: int | None = 0,
) -> str:
    """
    This function provides a wrapper for the numbers `format_currency` method, generating the
    number format (including the desired number of decimals).

    The number of decimals displayed is based on the value entered by the user, the decimal limit set in the schema
    and the locale.
    """
    locale = locale or flask_babel.get_locale()
    decimal_places = _get_decimal_places(value)

    # get locale pattern
    parsed_locale = Locale.parse(locale)

    # Use the default babel currency format "standard"
    number_format = parsed_locale.currency_formats["standard"]

    currency_precision = get_currency_precision(currency)

    # If there is no decimal limit then use the currency precision value if the number of decimals entered
    # is less than the value returned by babel's currency precision method.
    if (
        decimal_limit is not None
        and currency_precision > decimal_limit >= decimal_places
    ) or (decimal_limit is None and not decimal_places):
        currency_digits = False
    else:
        currency_digits = decimal_places < currency_precision

    # The decimal limit is set to either the number of decimal places entered by the user, or the currency precision
    # value for the given currency, whichever is larger.
    decimal_limit = max(decimal_places, currency_precision)

    # Formats the number based on the number of decimal places and the decimal limit that have been calcualted
    # above.
    number_format.frac_prec = (min(decimal_places, decimal_limit), decimal_limit)

    return numbers.format_currency(
        number=value,
        currency=currency,
        format=number_format,
        locale=parsed_locale,
        currency_digits=currency_digits,
    )


def custom_format_unit(
    value: int | float | Decimal,
    measurement_unit: str,
    locale: Locale | str,
    length: UnitLengthType = "short",
):
    """
    This function provides a wrapper for the numbers `format_unit` method, generating the
    number format (including the desired number of decimals), based on the value entered by the user and
    the locale.
    """
    number_format = get_number_format(value, locale)

    formatted_unit: str = units.format_unit(
        value=value,
        measurement_unit=measurement_unit,
        length=length,
        format=number_format,
        locale=locale,
    )

    return formatted_unit


def get_number_format(value: int | float | Decimal, locale: Locale | str) -> str:
    """
    Generates the number format based on the value entered by the user and the locale

    Format follows the number formats as specified in the babel docs e.g: '#,##0.###'

    Uses the decimal places set by the user with frac_prec to ensure that trailing zeroes
    are not dropped and that the correct number of decimal places as entered by the user are displayed
    after formatting.
    """
    decimal_places = _get_decimal_places(value)
    locale = Locale.parse(locale)
    locale_decimal_format = locale.decimal_formats[None]
    locale_decimal_format.frac_prec = (decimal_places, decimal_places)
    return locale_decimal_format


def _get_decimal_places(value: int | float | Decimal | None) -> int:
    """
    We use '.' rather than the decimal separator based on the locale as the separator will always be
    formatted so that it is '.' by the time it reaches this method.
    """
    return len(str(value).split(".")[1]) if "." in str(value) else 0
