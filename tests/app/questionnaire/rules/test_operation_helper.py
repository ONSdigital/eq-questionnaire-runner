import pytest

from app.questionnaire.rules.operation_helper import (
    DateOffset,
    resolve_date_from_string,
)


@pytest.mark.parametrize(
    "ref_date,weeks_prior,first_day_of_week,expected",
    [
        # All weekdays as reference date
        ("2021-09-26", -1, "MONDAY", "2021-09-13"),
        ("2021-09-27", -1, "MONDAY", "2021-09-20"),
        ("2021-09-28", -1, "MONDAY", "2021-09-20"),
        ("2021-09-29", -1, "MONDAY", "2021-09-20"),
        ("2021-09-30", -1, "MONDAY", "2021-09-20"),
        ("2021-10-01", -1, "MONDAY", "2021-09-20"),
        ("2021-10-02", -1, "MONDAY", "2021-09-20"),
        ("2021-10-03", -1, "MONDAY", "2021-09-20"),
        ("2021-10-04", -1, "MONDAY", "2021-09-27"),
        # All weekdays as reference, first day of the week is midweek
        ("2021-09-22", -1, "THURSDAY", "2021-09-09"),
        ("2021-09-23", -1, "THURSDAY", "2021-09-16"),
        ("2021-09-24", -1, "THURSDAY", "2021-09-16"),
        ("2021-09-25", -1, "THURSDAY", "2021-09-16"),
        ("2021-09-26", -1, "THURSDAY", "2021-09-16"),
        ("2021-09-27", -1, "THURSDAY", "2021-09-16"),
        ("2021-09-28", -1, "THURSDAY", "2021-09-16"),
        ("2021-09-29", -1, "THURSDAY", "2021-09-16"),
        ("2021-09-30", -1, "THURSDAY", "2021-09-23"),
        # All weekdays equal to first day of the week
        ("2021-09-27", -1, "MONDAY", "2021-09-20"),
        ("2021-09-28", -1, "TUESDAY", "2021-09-21"),
        ("2021-09-29", -1, "WEDNESDAY", "2021-09-22"),
        ("2021-09-30", -1, "THURSDAY", "2021-09-23"),
        ("2021-10-01", -1, "FRIDAY", "2021-09-24"),
        ("2021-10-02", -1, "SATURDAY", "2021-09-25"),
        ("2021-10-03", -1, "SUNDAY", "2021-09-26"),
        # All weekdays equal to last day of the week
        ("2021-09-26", -1, "MONDAY", "2021-09-13"),
        ("2021-09-27", -1, "TUESDAY", "2021-09-14"),
        ("2021-09-28", -1, "WEDNESDAY", "2021-09-15"),
        ("2021-09-29", -1, "THURSDAY", "2021-09-16"),
        ("2021-09-30", -1, "FRIDAY", "2021-09-17"),
        ("2021-10-01", -1, "SATURDAY", "2021-09-18"),
        ("2021-10-02", -1, "SUNDAY", "2021-09-19"),
        # Varying weeks offset
        ("2021-09-27", 0, "MONDAY", "2021-09-27"),
        ("2021-09-27", -1, "MONDAY", "2021-09-20"),
        ("2021-09-27", -2, "MONDAY", "2021-09-13"),
        ("2021-09-27", -4, "MONDAY", "2021-08-30"),
        ("2021-09-27", -52, "MONDAY", "2020-09-28"),
        ("2021-09-27", 1, "MONDAY", "2021-10-04"),
        ("2021-09-27", 2, "MONDAY", "2021-10-11"),
        ("2021-09-27", 4, "MONDAY", "2021-10-25"),
        ("2021-09-27", 52, "MONDAY", "2022-09-26"),
        # Varying days offset
        ("2021-09-27", 0, "MONDAY", "2021-09-27"),
        ("2021-09-27", 0, "MONDAY", "2021-09-27"),
        ("2021-09-27", 0, "MONDAY", "2021-09-27"),
    ],
)
def test_resolve_date_from_string_all_weekdays_as_reference_date(
    ref_date, weeks_prior, first_day_of_week, expected
):
    offset = DateOffset(days=weeks_prior * 7, day_of_week=first_day_of_week)
    offset_by_full_weeks = True
    actual = resolve_date_from_string(ref_date, offset, offset_by_full_weeks)
    assert str(actual) == expected


def test_resolve_date_from_string_kwarg_default_monday():
    expected = "2021-09-13"
    offset = DateOffset(days=-1 * 7, day_of_week="MONDAY")
    actual = resolve_date_from_string("2021-09-26", offset, True)
    assert str(actual) == expected


def test_resolve_date_from_string_wrong_format():
    offset = DateOffset(days=-1 * 7, day_of_week="Monday")
    offset_by_full_weeks = True
    actual = resolve_date_from_string("", offset, offset_by_full_weeks)
    assert not actual


def test_resolve_date_from_string_invalid_offset():
    offset = DateOffset(days=-1, day_of_week="Monday")
    with pytest.raises(ValueError) as excinfo:
        resolve_date_from_string("2021-01-05", offset)
    assert "Negative days offset must be less than or equal to -7" in str(excinfo.value)


def test_resolve_date_from_string_offset_literal_date():
    expected = "2020-12-26"
    offset = DateOffset(days=-7, day_of_week="SATURDAY")
    actual = resolve_date_from_string("2021-01-01", offset)
    assert str(actual) == expected
