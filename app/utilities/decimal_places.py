from decimal import Decimal

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
    locale_format = locale_format.number_pattern.split(".")[0]
    locale_format = f'{locale_format}{decimal_separator}{"0" * decimal_places}'

    formatted_number = numbers.format_decimal(
        value,
        format=locale_format,
        locale=locale_p,
    )
    return formatted_number
