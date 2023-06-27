from decimal import Decimal

import pytest

from app.questionnaire.placeholder_transforms import PlaceholderTransforms
from app.questionnaire.questionnaire_schema import QuestionnaireSchema


@pytest.mark.parametrize(
    "number, currency, expected",
    (
        ("11", "GBP", "£11.00"),
        ("11.99", "GBP", "£11.99"),
        ("11000", "USD", "US$11,000.00"),
        (0, None, "£0.00"),
        (0.00, None, "£0.00"),
    ),
)
def test_format_currency(number, currency, expected, transformer):
    assert transformer().format_currency(number, currency or "GBP") == expected


@pytest.mark.parametrize(
    "number, expected",
    (
        (123, "123"),
        ("123.4", "123.4"),
        ("123.40", "123.4"),
        ("123.45678", "123.45678"),
        ("1000", "1,000"),
        ("10000", "10,000"),
        ("100000000", "100,000,000"),
        (0, "0"),
        (0.00, "0"),
        ("", ""),
        (None, ""),
    ),
)
def test_format_number(number, expected, transformer):
    assert transformer().format_number(number) == expected


@pytest.mark.parametrize(
    "value, expected",
    (
        (123, "123%"),
        ("123.4", "123.4%"),
        ("123.40", "123.40%"),
        ("1000", "1000%"),
        (0, "0%"),
        (0.00, "0.0%"),
        (Decimal("0.123"), "0.123%"),
    ),
)
def test_format_percentage(value, expected, transformer):
    assert transformer().format_percentage(value) == expected


@pytest.mark.parametrize(
    "unit, value, unit_length, expected",
    (
        (
            "millimeter",
            Decimal(0.123),
            "short",
            "0.1229999999999999982236431605997495353221893310546875 mm",
        ),
        ("centimeter", "123", "short", "123 cm"),
        ("kilometer", "123", "long", "123 kilometres"),
        ("mile", "123", "short", "123 mi"),
        ("mile", "123", "narrow", "123mi"),
        ("mile", "123", None, "123 mi"),
        ("mile", "123.456789", None, "123.456789 mi"),
    ),
)
def test_format_unit(unit, value, unit_length, expected, transformer):
    assert transformer().format_unit(unit, value, unit_length) == expected


def test_format_list(transformer):
    transform = transformer()
    names = ["Alice Aardvark", "Bob Berty Brown", "Dave Dixon Davies"]

    format_value = transform.format_list(names)

    expected_result = (
        "<ul>"
        "<li>Alice Aardvark</li>"
        "<li>Bob Berty Brown</li>"
        "<li>Dave Dixon Davies</li>"
        "</ul>"
    )

    assert expected_result == format_value


@pytest.mark.parametrize(
    "name, expected",
    (
        ("Alice Aardvark", "Alice Aardvark’s"),
        ("Dave Dixon Davies", "Dave Dixon Davies’"),
        ("Alice Aardvark's", "Alice Aardvark’s"),
        ("Alice Aardvark’s", "Alice Aardvark’s"),
    ),
)
def test_format_possessive(name, expected, transformer):
    assert transformer().format_possessive(name) == expected


@pytest.mark.parametrize(
    "name, expected",
    (
        ("Alice Aardvark", "Alice Aardvark"),
        ("Dave Dixon Davies", "Dave Dixon Davies"),
        ("Alice Aardvark's", "Alice Aardvark's"),
        ("Alice Aardvark’s", "Alice Aardvark’s"),
    ),
)
def test_format_possessive_non_english_does_nothing(name, expected, transformer):
    assert transformer(language="cy").format_possessive(name) == expected


@pytest.mark.parametrize(
    "date_start, date_end, expected",
    (
        ("2016-06-10", "2019-06-10", "3 years"),
        ("2018-06-10", "2019-06-10", "1 year"),
        ("2010-01-01", "2018-12-31", "8 years"),
        ("2011-01", "2015-04", "4 years"),
        ("2019-06-10", "2019-08-11", "2 months"),
        ("2019-07-10", "2019-08-11", "1 month"),
        ("2019-07-10", "2019-07-11", "1 day"),
        ("now", "now", "0 days"),
        (
            "2021-07-29T10:53:41.511833+00:00",
            "2021-09-29T10:53:41.511833+00:00",
            "2 months",
        ),
        ("2021-09-28", "2021-09-29T10:53:41.511833+00:00", "1 day"),
    ),
)
def test_calculate_difference(date_start, date_end, expected):
    assert (
        PlaceholderTransforms.calculate_date_difference(date_start, date_end)
        == expected
    )


@pytest.mark.parametrize(
    "token, expected",
    (
        ("", "MilkEggsFlourWater"),
        (" ", "Milk Eggs Flour Water"),
        (", ", "Milk, Eggs, Flour, Water"),
    ),
)
def test_concatenate_list(token, expected, transformer):
    list_to_concatenate = ["Milk", "Eggs", "Flour", "Water"]
    assert transformer().concatenate_list(list_to_concatenate, token) == expected


@pytest.mark.parametrize(
    "first, second, expected",
    (
        (1, 2, 3),
        (-2, -1, -3),
        (-2, 1, -1),
        (3, -2, 1),
    ),
)
def test_add_int(first, second, expected, transformer):
    assert transformer().add(first, second) == expected


@pytest.mark.parametrize(
    "first, second, expected",
    (
        ("1.5", "2.5", "4"),
        ("-2.5", "-1.1", "-3.6"),
        ("-2.5", "1.9", "-0.6"),
        ("3.7", "-2.7", "1"),
    ),
)
def test_add_decimal(first, second, expected, transformer):
    assert transformer().add(Decimal(first), Decimal(second)) == Decimal(expected)


@pytest.mark.parametrize(
    "language, number_to_format, determiner, expected",
    (
        ("en", 1, "a_or_an", "a 1st"),
        ("en", 2, "a_or_an", "a 2nd"),
        ("en", 3, "a_or_an", "a 3rd"),
        ("en", 4, "a_or_an", "a 4th"),
        ("en", 8, "a_or_an", "an 8th"),
        ("en", 11, "a_or_an", "an 11th"),
        ("en", 12, "a_or_an", "a 12th"),
        ("en", 13, "a_or_an", "a 13th"),
        ("en", 18, "a_or_an", "an 18th"),
        ("en", 21, "a_or_an", "a 21st"),
        ("en", 22, "a_or_an", "a 22nd"),
        ("en", 23, "a_or_an", "a 23rd"),
        ("en", 111, "a_or_an", "a 111th"),
        ("en", 112, "a_or_an", "a 112th"),
        ("en", 113, "a_or_an", "a 113th"),
        ("en", 1, None, "1st"),
        ("en", 2, None, "2nd"),
        ("en", 3, None, "3rd"),
        ("en", 4, None, "4th"),
        ("en", 21, None, "21st"),
        ("eo", 1, "a_or_an", "a 1st"),
        ("eo", 2, "a_or_an", "a 2nd"),
        ("eo", 3, "a_or_an", "a 3rd"),
        ("eo", 4, "a_or_an", "a 4th"),
        ("eo", 8, "a_or_an", "an 8th"),
        ("eo", 11, "a_or_an", "an 11th"),
        ("eo", 1, None, "1st"),
        ("eo", 2, None, "2nd"),
        ("eo", 3, None, "3rd"),
        ("eo", 4, None, "4th"),
        ("eo", 8, None, "8th"),
        ("eo", 11, None, "11th"),
        ("ga", 1, None, "1ú"),
        ("ga", 2, None, "2ú"),
        ("ga", 5, None, "5ú"),
        ("ga", 7, None, "7ú"),
        ("ga", 21, None, "21ú"),
        ("cy", 1, None, "1af"),
        ("cy", 2, None, "2il"),
        ("cy", 3, None, "3ydd"),
        ("cy", 7, None, "7fed"),
        ("cy", 13, None, "13eg"),
        ("cy", 18, None, "18fed"),
        ("cy", 21, None, "21ain"),
        ("cy", 40, None, "40ain"),
    ),
)
def test_format_ordinal_with_determiner(
    language, number_to_format, determiner, expected, transformer
):
    assert (
        transformer(language).format_ordinal(number_to_format, determiner) == expected
    )


def test_remove_empty_from_list(transformer):
    list_to_filter = [
        None,
        0,
        False,
        "",
        " ",
        [],
        {},
        set(),
        tuple(),
        Decimal("0"),
        "String",
    ]

    assert transformer().remove_empty_from_list(list_to_filter) == [
        0,
        False,
        " ",
        Decimal("0"),
        "String",
    ]


def test_first_non_empty_item(transformer):
    list_to_filter = [
        [],
        {},
        set(),
        tuple(),
        "",
        None,
        0,
        Decimal("0"),
        False,
        " ",
        "String",
    ]

    assert transformer().first_non_empty_item(list_to_filter) == 0


def test_first_non_empty_item_no_valid(transformer):
    list_to_filter = [
        [],
        {},
        set(),
        tuple(),
        "",
        None,
    ]

    assert transformer().first_non_empty_item(list_to_filter) == ""


def test_contains(transformer):
    list_to_check = ["abc123", "fgh789"]

    assert transformer().contains(list_to_check, "abc123")
    assert not transformer().contains(list_to_check, "def456")
    assert not transformer().contains(list_to_check, "abc1234")
    assert not transformer().contains(list_to_check, "abc")


def test_list_has_items(transformer):
    assert transformer().list_has_items(["abc123", "fgh789"])
    assert not transformer().list_has_items([])


@pytest.mark.parametrize(
    "first, middle, last, include_middle_names, expected",
    (
        ("Joe", None, "Bloggs", True, "Joe Bloggs"),
        ("Joe", None, "Bloggs", True, "Joe Bloggs"),
        ("Joe", "Michael", "Bloggs", True, "Joe Michael Bloggs"),
        ("Joe", "Michael", "Bloggs", False, "Joe Bloggs"),
    ),
)
def test_format_name(first, middle, last, include_middle_names, expected, transformer):
    assert (
        transformer().format_name(
            first, middle, last, include_middle_names=include_middle_names
        )
        == expected
    )


@pytest.mark.parametrize(
    "address, subject, reference, expected",
    (
        (
            "test@email.com",
            None,
            None,
            '<a href="mailto:test@email.com">test@email.com</a>',
        ),
        (
            "test@email.com",
            "test subject",
            None,
            '<a href="mailto:test@email.com?subject=test%20subject">test@email.com</a>',
        ),
        (
            "test@email.com",
            "test subject",
            "12345",
            '<a href="mailto:test@email.com?subject=test%20subject%2012345">test@email.com</a>',
        ),
    ),
)
def test_email_link(address, subject, reference, expected, transformer):
    assert (
        transformer().email_link(
            address,
            subject,
            reference,
        )
        == expected
    )


def test_telephone_number_link(transformer):
    assert (
        transformer().telephone_number_link("012345 67890")
        == '<a href="tel:01234567890">012345 67890</a>'
    )


@pytest.mark.parametrize(
    "item_list, expected",
    (
        (["Alice Aardvark", "Bob Berty Brown", "Dave Dixon Davies"], 3),
        ([], 0),
        (None, 0),
    ),
)
def test_list_item_count(item_list, expected, transformer):
    assert transformer().list_item_count(item_list) == expected


@pytest.mark.parametrize(
    "ref_date, weeks_prior, day_range, first_day_of_week, expected",
    [
        # All weekdays as reference date
        ("2021-09-26", -1, 7, "MONDAY", ("2021-09-13", "2021-09-19")),
        ("2021-09-27", -1, 7, "MONDAY", ("2021-09-20", "2021-09-26")),
        ("2021-09-28", -1, 7, "MONDAY", ("2021-09-20", "2021-09-26")),
        ("2021-09-29", -1, 7, "MONDAY", ("2021-09-20", "2021-09-26")),
        ("2021-09-30", -1, 7, "MONDAY", ("2021-09-20", "2021-09-26")),
        ("2021-10-01", -1, 7, "MONDAY", ("2021-09-20", "2021-09-26")),
        ("2021-10-02", -1, 7, "MONDAY", ("2021-09-20", "2021-09-26")),
        ("2021-10-03", -1, 7, "MONDAY", ("2021-09-20", "2021-09-26")),
        ("2021-10-04", -1, 7, "MONDAY", ("2021-09-27", "2021-10-03")),
        # All weekdays as reference, first day of the week is midweek
        ("2021-09-22", -1, 7, "THURSDAY", ("2021-09-09", "2021-09-15")),
        ("2021-09-23", -1, 7, "THURSDAY", ("2021-09-16", "2021-09-22")),
        ("2021-09-24", -1, 7, "THURSDAY", ("2021-09-16", "2021-09-22")),
        ("2021-09-25", -1, 7, "THURSDAY", ("2021-09-16", "2021-09-22")),
        ("2021-09-26", -1, 7, "THURSDAY", ("2021-09-16", "2021-09-22")),
        ("2021-09-27", -1, 7, "THURSDAY", ("2021-09-16", "2021-09-22")),
        ("2021-09-28", -1, 7, "THURSDAY", ("2021-09-16", "2021-09-22")),
        ("2021-09-29", -1, 7, "THURSDAY", ("2021-09-16", "2021-09-22")),
        ("2021-09-30", -1, 7, "THURSDAY", ("2021-09-23", "2021-09-29")),
        # All weekdays equal to first day of the week
        ("2021-09-27", -1, 7, "MONDAY", ("2021-09-20", "2021-09-26")),
        ("2021-09-28", -1, 7, "TUESDAY", ("2021-09-21", "2021-09-27")),
        ("2021-09-29", -1, 7, "WEDNESDAY", ("2021-09-22", "2021-09-28")),
        ("2021-09-30", -1, 7, "THURSDAY", ("2021-09-23", "2021-09-29")),
        ("2021-10-01", -1, 7, "FRIDAY", ("2021-09-24", "2021-09-30")),
        ("2021-10-02", -1, 7, "SATURDAY", ("2021-09-25", "2021-10-01")),
        ("2021-10-03", -1, 7, "SUNDAY", ("2021-09-26", "2021-10-02")),
        # All weekdays equal to last day of the week
        ("2021-09-26", -1, 7, "MONDAY", ("2021-09-13", "2021-09-19")),
        ("2021-09-27", -1, 7, "TUESDAY", ("2021-09-14", "2021-09-20")),
        ("2021-09-28", -1, 7, "WEDNESDAY", ("2021-09-15", "2021-09-21")),
        ("2021-09-29", -1, 7, "THURSDAY", ("2021-09-16", "2021-09-22")),
        ("2021-09-30", -1, 7, "FRIDAY", ("2021-09-17", "2021-09-23")),
        ("2021-10-01", -1, 7, "SATURDAY", ("2021-09-18", "2021-09-24")),
        ("2021-10-02", -1, 7, "SUNDAY", ("2021-09-19", "2021-09-25")),
        # Varying weeks offset
        ("2021-09-27", 0, 7, "MONDAY", ("2021-09-27", "2021-10-03")),
        ("2021-09-27", -1, 7, "MONDAY", ("2021-09-20", "2021-09-26")),
        ("2021-09-27", -2, 7, "MONDAY", ("2021-09-13", "2021-09-19")),
        ("2021-09-27", -4, 7, "MONDAY", ("2021-08-30", "2021-09-05")),
        ("2021-09-27", -52, 7, "MONDAY", ("2020-09-28", "2020-10-04")),
        ("2021-09-27", 1, 7, "MONDAY", ("2021-10-04", "2021-10-10")),
        ("2021-09-27", 2, 7, "MONDAY", ("2021-10-11", "2021-10-17")),
        ("2021-09-27", 4, 7, "MONDAY", ("2021-10-25", "2021-10-31")),
        ("2021-09-27", 52, 7, "MONDAY", ("2022-09-26", "2022-10-02")),
        # Varying days offset
        ("2021-09-27", 0, 1, "MONDAY", ("2021-09-27", "2021-09-27")),
        ("2021-09-27", 0, 10, "MONDAY", ("2021-09-27", "2021-10-06")),
        ("2021-09-27", 0, 14, "MONDAY", ("2021-09-27", "2021-10-10")),
    ],
)
def test_date_range_bounds_all_weekdays_as_reference_date(
    transformer, ref_date, weeks_prior, day_range, first_day_of_week, expected
):
    actual = transformer().date_range_bounds(
        ref_date, weeks_prior, day_range, first_day_of_week
    )
    assert actual == expected


def test_date_range_bounds_kwarg_default_monday(transformer):
    expected = ("2021-09-13", "2021-09-19")
    actual = transformer().date_range_bounds("2021-09-26", -1, 7)
    assert actual == expected


@pytest.mark.parametrize(
    "date_range, expected",
    [
        (
            ("2021-09-01", "2021-09-15"),
            "Wednesday 1 to Wednesday 15 September 2021",
        ),
        (
            ("2021-09-15", "2021-10-15"),
            "Wednesday 15 September to Friday 15 October 2021",
        ),
        (
            ("2021-09-15", "2022-09-15"),
            "Wednesday 15 September 2021 to Thursday 15 September 2022",
        ),
        (
            ("2021-09-15", "2022-10-15"),
            "Wednesday 15 September 2021 to Saturday 15 October 2022",
        ),
    ],
)
def test_format_date_range(transformer, date_range, expected):
    actual = transformer().format_date_range(date_range)
    assert actual == expected


@pytest.mark.parametrize(
    "answer_id, value, expected",
    [
        (
            "mandatory-radio-answer",
            "{business_name} (piped)",
            "ESSENTIAL SERVICES LTD (piped)",
        ),
        ("mandatory-radio-answer", "Meta LTD", "Meta LTD"),
    ],
)
def test_option_label_from_value_with_placeholder_label(
    answer_id,
    value,
    expected,
    placeholder_renderer,
    option_label_from_value_schema,
):
    label_renderer = placeholder_renderer

    placeholder_transform = PlaceholderTransforms(
        language="en", schema=option_label_from_value_schema, renderer=label_renderer
    )
    actual = placeholder_transform.option_label_from_value(value, answer_id)

    assert actual == expected


@pytest.mark.parametrize(
    "trad_as, expected",
    [
        ("Apple", " (Apple)"),
        (None, ""),
        ("", ""),
    ],
)
def test_conditional_trad_as(transformer, trad_as, expected):
    actual = transformer().conditional_trad_as(trad_as)
    assert actual == expected


@pytest.mark.parametrize(
    "invalid_number_to_format",
    [
        (100),
        (200),
    ],
)
def test_get_ordinal_indicator_raises_NotImplementedError(invalid_number_to_format):
    placeholder_transform = PlaceholderTransforms(
        "invalid_language", QuestionnaireSchema, "PlaceholderRenderer"
    )
    with pytest.raises(NotImplementedError):
        placeholder_transform.get_ordinal_indicator(invalid_number_to_format)
