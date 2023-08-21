from decimal import Decimal
from typing import Literal, TypeAlias

from babel import Locale, numbers, units

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


def custom_format_currency(
    value: float | Decimal,
    currency: str,
    locale: Locale | str,
    decimal_limit: int | None = None,
) -> str:
    """
    This function provides a wrapper for the numbers `format_currency` method, generating the
    number format (including the desired number of decimals).

    The number of decimals displayed is based on the value entered by the user, the decimal limit set in the schema
    and the locale.
    """
    decimal_places = len(str(value).split(".")[1]) if "." in str(value) else 0

    # get locale pattern
    parsed_locale = Locale.parse(locale)
    number_format = parsed_locale.currency_formats["standard"]

    # If set, the number of decimals displayed is limited based on the value of the `decimal_limit` parameter.
    # If the number of decimal places entered by the user is less than the `decimal_limit` then we should display the
    # number of decimals as entered by the user. Otherwise, we should display the number of decimals as entered by the user.
    decimal_max = decimal_limit if decimal_limit is not None else decimal_places
    number_format.frac_prec = (min(decimal_places, decimal_max), decimal_max)

    # Needed to stop trailing decimal `.00` being added when no decimal places have been entered by the user
    #  and trailing decimals being cut off when two or more decimals have been entered by the user
    currency_digits = decimal_places < 2
    if decimal_limit is not None and decimal_limit < 2:
        currency_digits = False

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
    decimal_places = len(str(value).split(".")[1]) if "." in str(value) else 0
    locale = Locale.parse(locale)
    locale_decimal_format = locale.decimal_formats[None]
    locale_decimal_format.frac_prec = (decimal_places, decimal_places)
    return locale_decimal_format
