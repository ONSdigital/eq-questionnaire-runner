import unicodedata
from decimal import Decimal

import pytest

from app.utilities.decimal_places import (
    custom_format_currency,
    custom_format_decimal,
    custom_format_unit,
)


@pytest.mark.parametrize(
    "value, locale_string, expected_result",
    (
        (123, "en_GB", "123"),
        (123, "es_ES", "123"),
        (Decimal("123.4"), "en_GB", "123.4"),
        (Decimal("123.4"), "es_US", "123.4"),
        (Decimal("123.40"), "en_GB", "123.40"),
        (Decimal("123.400"), "en_GB", "123.400"),
        (Decimal("123.4000"), "en_GB", "123.4000"),
        (Decimal("123.4000"), "pl_PL", "123,4000"),
        (Decimal("123.40000"), "en_GB", "123.40000"),
        (Decimal("123.40000"), "ja_JP", "123.40000"),
        (Decimal("123434.7678"), "en_GB", "123,434.7678"),
        (Decimal("123434.7678"), "hu_HU", "123 434,7678"),
        (Decimal("123.45678"), "en_GB", "123.45678"),
        (Decimal("2344.6533"), "en_GB", "2,344.6533"),
        (1000, "en_GB", "1,000"),
        (1000, "en_US", "1,000"),
        (10000, "en_GB", "10,000"),
        (10000, "es_ES", "10.000"),
        (100000000, "en_GB", "100,000,000"),
        (0, "en_GB", "0"),
        (0, "de_DE", "0"),
        (Decimal("0.00"), "en_GB", "0.00"),
        (Decimal("0.000"), "en_GB", "0.000"),
        (Decimal("0.000"), "es_ES", "0,000"),
        (Decimal("0.00000"), "en_GB", "0.00000"),
        (Decimal("0.00000"), "es_ES", "0,00000"),
    ),
)
def test_custom_format_decimal(value, locale_string, expected_result):
    result = custom_format_decimal(value, locale_string)

    assert unicodedata.normalize("NFKD", result) == expected_result


@pytest.mark.parametrize(
    "value, measurement_unit, locale_string, length, expected_result",
    (
        (123, "mile", "en_GB", "short", "123 mi"),
        (
            Decimal("0.123"),
            "millimeter",
            "en_GB",
            "short",
            "0.123 mm",
        ),
        (
            Decimal("0.123"),
            "millimeter",
            "es_ES",
            "short",
            "0,123 mm",
        ),
        (123, "centimeter", "en_GB", "short", "123 cm"),
        (123, "centimeter", "pl_PL", "short", "123 cm"),
        (123, "kilometer", "en_GB", "long", "123 kilometres"),
        (3, "kilometer", "en_GB", "long", "3 kilometres"),
        (3, "kilometer", "hu_HU", "long", "3 kilométer"),
        (Decimal("1.2"), "kilometer", "en_GB", "long", "1.2 kilometres"),
        (Decimal("1.20"), "kilometer", "en_GB", "long", "1.20 kilometres"),
        (Decimal("1.200"), "kilometer", "en_GB", "long", "1.200 kilometres"),
        (Decimal("1.2000"), "kilometer", "en_GB", "long", "1.2000 kilometres"),
        (Decimal("1.20000"), "kilometer", "en_GB", "long", "1.20000 kilometres"),
        (Decimal("1.20000"), "kilometer", "de_DE", "long", "1,20000 Kilometer"),
        (Decimal("1.2"), "kilometer", "pl_PL", "long", "1,2 kilometra"),
        (Decimal("1.2345"), "kilometer", "en_GB", "long", "1.2345 kilometres"),
        (Decimal("1.2345"), "kilometer", "es_ES", "long", "1,2345 kilómetros"),
        (123, "mile", "en_GB", "short", "123 mi"),
        (123, "mile", "en_GB", "narrow", "123mi"),
        (123, "mile", "en_US", "narrow", "123mi"),
    ),
)
def test_custom_format_unit(
    value, measurement_unit, locale_string, length, expected_result
):
    result = custom_format_unit(value, measurement_unit, locale_string, length)

    assert result == expected_result


@pytest.mark.parametrize(
    "value, currency, locale_string, decimal_limit, expected_result",
    (
        (123, "GBP", "en_GB", 1, "£123"),
        (Decimal("123.1234"), "GBP", "en_GB", 0, "£123"),
        (Decimal("3000.44545"), "GBP", "en_GB", None, "£3,000.44545"),
        (Decimal("2.1"), "GBP", "en_GB", None, "£2.10"),
        (Decimal("3000"), "GBP", "en_GB", 0, "£3,000"),
        (Decimal("3000"), "JPY", "en_GB", 0, "JP¥3,000"),
        (Decimal("3000"), "JPY", "ja_JP", 0, "¥3,000"),
        (Decimal("123.45"), "GBP", "en_GB", 1, "£123.4"),
        (Decimal("123.45"), "HUF", "hu_HU", 1, "123,4 Ft"),
        (Decimal("2.1"), "GBP", "en_GB", 1, "£2.1"),
        (11, "GBP", "en_GB", 2, "£11.00"),
        (11000, "USD", "en_GB", 2, "US$11,000.00"),
        (11000, "USD", "en_GB", 2, "US$11,000.00"),
        (11000, "PLN", "pl_PL", 2, "11 000,00 zł"),
        (Decimal("11.99"), "GBP", "en_GB", 2, "£11.99"),
        (2, "GBP", "en_GB", 6, "£2.00"),
        (Decimal("2.14564"), "GBP", "en_GB", 6, "£2.14564"),
        (Decimal("1.1"), "GBP", "en_GB", 6, "£1.10"),
        (Decimal("1.10"), "GBP", "en_GB", 6, "£1.10"),
        (Decimal("1.100"), "GBP", "en_GB", 6, "£1.100"),
        (Decimal("1.1000"), "GBP", "en_GB", 6, "£1.1000"),
        (Decimal("3000.445"), "GBP", "en_GB", 6, "£3,000.445"),
    ),
)
def test_custom_format_currency(
    value, currency, locale_string, decimal_limit, expected_result
):
    result = custom_format_currency(value, currency, locale_string, decimal_limit)

    assert unicodedata.normalize("NFKD", result) == expected_result
