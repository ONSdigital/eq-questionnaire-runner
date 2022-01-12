from decimal import Decimal

import pytest

from app.questionnaire.placeholder_transforms import PlaceholderTransforms


def test_format_currency(transformer):
    transform = transformer()
    assert transform.format_currency("11", "GBP") == "£11.00"
    assert transform.format_currency("11.99", "GBP") == "£11.99"
    assert transform.format_currency("11000", "USD") == "US$11,000.00"
    assert transform.format_currency(0) == "£0.00"
    assert transform.format_currency(0.00) == "£0.00"


def test_format_number(transformer):
    transform = transformer()
    assert transform.format_number(123) == "123"
    assert transform.format_number("123.4") == "123.4"
    assert transform.format_number("123.40") == "123.4"
    assert transform.format_number("1000") == "1,000"
    assert transform.format_number("10000") == "10,000"
    assert transform.format_number("100000000") == "100,000,000"
    assert transform.format_number(0) == "0"
    assert transform.format_number(0.00) == "0"
    assert transform.format_number("") == ""
    assert transform.format_number(None) == ""


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


def test_format_possessive(transformer):
    transform = transformer()
    assert transform.format_possessive("Alice Aardvark") == "Alice Aardvark’s"
    assert transform.format_possessive("Dave Dixon Davies") == "Dave Dixon Davies’"
    assert transform.format_possessive("Alice Aardvark's") == "Alice Aardvark’s"
    assert transform.format_possessive("Alice Aardvark’s") == "Alice Aardvark’s"


def test_format_possessive_non_english_does_nothing(transformer):
    welsh_transform = transformer(language="cy")

    assert welsh_transform.format_possessive("Alice Aardvark") == "Alice Aardvark"
    assert welsh_transform.format_possessive("Dave Dixon Davies") == "Dave Dixon Davies"
    assert welsh_transform.format_possessive("Alice Aardvark's") == "Alice Aardvark's"
    assert welsh_transform.format_possessive("Alice Aardvark’s") == "Alice Aardvark’s"


def test_calculate_difference():
    assert (
        PlaceholderTransforms.calculate_date_difference("2016-06-10", "2019-06-10")
        == "3 years"
    )
    assert (
        PlaceholderTransforms.calculate_date_difference("2018-06-10", "2019-06-10")
        == "1 year"
    )
    assert (
        PlaceholderTransforms.calculate_date_difference("2010-01-01", "2018-12-31")
        == "8 years"
    )
    assert (
        PlaceholderTransforms.calculate_date_difference("2011-01", "2015-04")
        == "4 years"
    )
    assert (
        PlaceholderTransforms.calculate_date_difference("2019-06-10", "2019-08-11")
        == "2 months"
    )
    assert (
        PlaceholderTransforms.calculate_date_difference("2019-07-10", "2019-08-11")
        == "1 month"
    )
    assert (
        PlaceholderTransforms.calculate_date_difference("2019-07-10", "2019-07-11")
        == "1 day"
    )
    assert PlaceholderTransforms.calculate_date_difference("now", "now") == "0 days"
    assert (
        PlaceholderTransforms.calculate_date_difference(
            "2021-07-29T10:53:41.511833+00:00", "2021-09-29T10:53:41.511833+00:00"
        )
        == "2 months"
    )
    assert (
        PlaceholderTransforms.calculate_date_difference(
            "2021-09-28", "2021-09-29T10:53:41.511833+00:00"
        )
        == "1 day"
    )


def test_concatenate_list(transformer):
    transform = transformer()
    list_to_concatenate = ["Milk", "Eggs", "Flour", "Water"]

    assert transform.concatenate_list(list_to_concatenate, "") == "MilkEggsFlourWater"
    assert (
        transform.concatenate_list(list_to_concatenate, " ") == "Milk Eggs Flour Water"
    )
    assert (
        transform.concatenate_list(list_to_concatenate, ", ")
        == "Milk, Eggs, Flour, Water"
    )


def test_add_int(transformer):
    transform = transformer()
    assert transform.add(int(1), int(2)) == int(3)


def test_add_decimal(transformer):
    transform = transformer()
    assert transform.add(Decimal("1.11"), Decimal("2.22")) == Decimal("3.33")


def test_format_ordinal_with_determiner(transformer):
    transform = transformer()
    assert transform.format_ordinal(1, "a_or_an") == "a 1st"
    assert transform.format_ordinal(2, "a_or_an") == "a 2nd"
    assert transform.format_ordinal(3, "a_or_an") == "a 3rd"
    assert transform.format_ordinal(4, "a_or_an") == "a 4th"
    assert transform.format_ordinal(8, "a_or_an") == "an 8th"
    assert transform.format_ordinal(11, "a_or_an") == "an 11th"
    assert transform.format_ordinal(12, "a_or_an") == "a 12th"
    assert transform.format_ordinal(13, "a_or_an") == "a 13th"
    assert transform.format_ordinal(18, "a_or_an") == "an 18th"
    assert transform.format_ordinal(21, "a_or_an") == "a 21st"
    assert transform.format_ordinal(22, "a_or_an") == "a 22nd"
    assert transform.format_ordinal(23, "a_or_an") == "a 23rd"
    assert transform.format_ordinal(111, "a_or_an") == "a 111th"
    assert transform.format_ordinal(112, "a_or_an") == "a 112th"
    assert transform.format_ordinal(113, "a_or_an") == "a 113th"


def test_format_ordinal_without_determiner(transformer):
    transform = transformer()
    assert transform.format_ordinal(1) == "1st"
    assert transform.format_ordinal(2) == "2nd"
    assert transform.format_ordinal(3) == "3rd"
    assert transform.format_ordinal(4) == "4th"
    assert transform.format_ordinal(21) == "21st"


def test_format_ordinal_with_determiner_ulster_scots(transformer):
    ulster_scots_transform = transformer(language="eo")
    assert ulster_scots_transform.format_ordinal(1, "a_or_an") == "a 1st"
    assert ulster_scots_transform.format_ordinal(2, "a_or_an") == "a 2nd"
    assert ulster_scots_transform.format_ordinal(3, "a_or_an") == "a 3rd"
    assert ulster_scots_transform.format_ordinal(4, "a_or_an") == "a 4th"
    assert ulster_scots_transform.format_ordinal(8, "a_or_an") == "an 8th"
    assert ulster_scots_transform.format_ordinal(11, "a_or_an") == "an 11th"


def test_format_ordinal_without_determiner_ulster_scots(transformer):
    ulster_scots_transform = transformer(language="eo")
    assert ulster_scots_transform.format_ordinal(1) == "1st"
    assert ulster_scots_transform.format_ordinal(2) == "2nd"
    assert ulster_scots_transform.format_ordinal(3) == "3rd"
    assert ulster_scots_transform.format_ordinal(4) == "4th"
    assert ulster_scots_transform.format_ordinal(21) == "21st"


def test_format_ordinal_gaelic(transformer):
    gaelic_transform = transformer(language="ga")
    assert gaelic_transform.format_ordinal(1) == "1ú"
    assert gaelic_transform.format_ordinal(2) == "2ú"
    assert gaelic_transform.format_ordinal(5) == "5ú"
    assert gaelic_transform.format_ordinal(7) == "7ú"
    assert gaelic_transform.format_ordinal(21) == "21ú"


def test_format_ordinal_welsh(transformer):
    welsh_transform = transformer(language="cy")
    assert welsh_transform.format_ordinal(1) == "1af"
    assert welsh_transform.format_ordinal(2) == "2il"
    assert welsh_transform.format_ordinal(3) == "3ydd"
    assert welsh_transform.format_ordinal(7) == "7fed"
    assert welsh_transform.format_ordinal(13) == "13eg"
    assert welsh_transform.format_ordinal(18) == "18fed"
    assert welsh_transform.format_ordinal(21) == "21ain"
    assert welsh_transform.format_ordinal(40) == "40ain"


def test_remove_empty_from_list(transformer):
    transform = transformer()
    list_to_filter = [None, 0, False, "", "String"]

    assert transform.remove_empty_from_list(list_to_filter) == [
        0,
        False,
        "String",
    ]


def test_first_non_empty_item(transformer):
    transform = transformer()
    list_to_filter = [None, 0, False, "", "String"]

    assert transform.first_non_empty_item(list_to_filter) == 0


def test_first_non_empty_item_no_valid(transformer):
    transform = transformer()
    list_to_filter = [None, None]

    assert transform.first_non_empty_item(list_to_filter) == ""


def test_contains(transformer):
    transform = transformer()
    list_to_check = ["abc123", "fgh789"]

    assert transform.contains(list_to_check, "abc123")
    assert not transform.contains(list_to_check, "def456")


def test_list_has_items(transformer):
    transform = transformer()
    assert transform.list_has_items(["abc123", "fgh789"])
    assert not transform.list_has_items([])


def test_format_name(transformer):
    transform = transformer()
    assert transform.format_name("Joe", None, "Bloggs") == "Joe Bloggs"
    assert (
        transform.format_name("Joe", None, "Bloggs", include_middle_names=True)
        == "Joe Bloggs"
    )
    assert transform.format_name("Joe", "Michael", "Bloggs") == "Joe Bloggs"
    assert (
        transform.format_name("Joe", "Michael", "Bloggs", include_middle_names=True)
        == "Joe Michael Bloggs"
    )


def test_email_link(transformer):
    transform = transformer()
    assert (
        transform.email_link("test@email.com")
        == '<a href="mailto:test@email.com">test@email.com</a>'
    )


def test_email_link_with_subject(transformer):
    transform = transformer()
    assert (
        transform.email_link("test@email.com", "test subject")
        == '<a href="mailto:test@email.com?subject=test%20subject">test@email.com</a>'
    )


def test_email_link_with_subject_and_reference(transformer):
    transform = transformer()
    assert (
        transform.email_link("test@email.com", "test subject", "12345")
        == '<a href="mailto:test@email.com?subject=test%20subject%2012345">test@email.com</a>'
    )


def test_telephone_number_link(transformer):
    transform = transformer()
    assert (
        transform.telephone_number_link("012345 67890")
        == '<a href="tel:01234567890">012345 67890</a>'
    )


def test_list_item_count(transformer):
    transform = transformer()
    assert (
        transform.list_item_count(
            ["Alice Aardvark", "Bob Berty Brown", "Dave Dixon Davies"]
        )
        == 3
    )
    assert transform.list_item_count([]) == 0
    assert transform.list_item_count(None) == 0


@pytest.mark.parametrize(
    "ref_date,weeks_prior,day_range,first_day_of_week,expected",
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
    placeholder_transform, ref_date, weeks_prior, day_range, first_day_of_week, expected
):
    actual = placeholder_transform.date_range_bounds(
        ref_date, weeks_prior, day_range, first_day_of_week
    )
    assert actual == expected


def test_date_range_bounds_kwarg_default_monday(placeholder_transform):
    expected = ("2021-09-13", "2021-09-19")
    actual = placeholder_transform.date_range_bounds("2021-09-26", -1, 7)
    assert actual == expected


@pytest.mark.parametrize(
    "date_range,expected",
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
def test_format_date_range(placeholder_transform, date_range, expected):
    actual = placeholder_transform.format_date_range(date_range)
    assert actual == expected


@pytest.mark.parametrize(
    "answer_id,value,expected",
    [
        ("mandatory-radio-answer", "{body_part} (piped)", "Body (piped)"),
        ("mandatory-checkbox-answer", "Body", "Body"),
    ],
)
def test_option_label_from_value_with_placeholder_label(
    placeholder_transform,
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
