from decimal import Decimal

from babel import Locale, numbers


def custom_format_decimal(
    value: int | Decimal | float, locale: Locale | str, decimal_separator: str
) -> str:
    """
    Function is used to format decimal numbers avoiding the decimal_quantization=True/False constraints and preserving the number input by the user.
    e.g 123.430 stays as 123.430 (if schema allows).
    """
    decimal_places = len(str(value).split(f"{decimal_separator}")[1])
    # set the locale_format by parsing the number pattern for the given locale and applying the number of decimal places passed through
    locale = Locale.parse(locale)
    locale_decimal_format = locale.decimal_formats[None]
    locale_format = locale_decimal_format.number_pattern.split(f"{decimal_separator}")[
        0
    ]
    number_format = f'{locale_format}{decimal_separator}{"0" * decimal_places}'

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
    decimal_separator = numbers.get_decimal_symbol(locale)
    decimal_places = (
        len(str(value).split(f"{decimal_separator}")[1])
        if decimal_separator in str(value)
        else 0
    )

    # get local pattern
    parsed_locale = Locale.parse(locale)
    number_format = parsed_locale.currency_formats["standard"]
    number_format.frac_prec = (0, decimal_places)

    # if decimal_limit is less than 2 then return the value the user entered
    if decimal_limit and decimal_limit < 2:
        return numbers.format_currency(
            number=value,
            currency=currency,
            format=number_format,
            locale=locale,
            currency_digits=False,
        )

    currency_digits = decimal_places < 2
    return numbers.format_currency(
        number=value,
        currency=currency,
        format=number_format,
        locale=parsed_locale,
        currency_digits=currency_digits,
    )
