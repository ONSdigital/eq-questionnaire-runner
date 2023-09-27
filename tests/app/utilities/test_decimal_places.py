import unicodedata

import pytest

from app.utilities.decimal_places import (
    custom_format_decimal,
    custom_format_unit,
    get_formatted_currency,
)
from tests.app.test_jinja_filters import (
    TEST_FORMAT_CURRENCY_PARAMS,
    TEST_FORMAT_NUMBER_PARAMS,
    TEST_FORMAT_UNIT_PARAMS,
)


@pytest.mark.parametrize(*TEST_FORMAT_NUMBER_PARAMS)
def test_custom_format_decimal(value, locale_string, expected_result):
    result = custom_format_decimal(value, locale_string)

    assert unicodedata.normalize("NFKD", result) == expected_result


@pytest.mark.parametrize(*TEST_FORMAT_UNIT_PARAMS)
def test_custom_format_unit(
    value, measurement_unit, locale_string, length, expected_result
):
    result = custom_format_unit(value, measurement_unit, locale_string, length)

    assert result == expected_result


@pytest.mark.parametrize(*TEST_FORMAT_CURRENCY_PARAMS)
def test_custom_format_currency(
    value, currency, locale_string, decimal_limit, expected_result
):
    result = get_formatted_currency(
        value=value,
        currency=currency,
        locale=locale_string,
        decimal_limit=decimal_limit,
    )

    assert unicodedata.normalize("NFKD", result) == expected_result
