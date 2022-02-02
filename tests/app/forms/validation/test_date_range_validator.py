import pytest
from wtforms.validators import ValidationError

from app.forms import error_messages


@pytest.mark.parametrize(
    "date_from, date_to",
    [
        ("2016-01-03", "2016-01-03"),
        ("2018-01-20", "2016-01-20"),
        ("2018-06", "2018-06"),
        ("2018-07", "2018-06"),
    ],
)
def test_invalid_date_range(
    get_date_range_check,
    mock_form,
    mock_period_from,
    mock_period_to,
    date_from,
    date_to,
):
    mock_period_from.data = date_from
    mock_period_to.data = date_to

    date_range_check = get_date_range_check()

    with pytest.raises(ValidationError) as context:
        date_range_check(mock_form, mock_period_from, mock_period_to)

    assert error_messages["INVALID_DATE_RANGE"] == str(context.value)


def test_date_range_with_too_small_period(
    get_date_range_check, mock_form, mock_period_from, mock_period_to
):
    mock_period_from.data = "2016-02-01"
    mock_period_to.data = "2016-02-12"
    period_min = {"days": 20}

    date_range_check = get_date_range_check(period_min=period_min)

    with pytest.raises(ValidationError) as context:
        date_range_check(mock_form, mock_period_from, mock_period_to)

    assert "Enter a reporting period greater than or equal to 20 days" == str(
        context.value
    )


def test_date_range_with_too_large_period(
    get_date_range_check, mock_form, mock_period_from, mock_period_to
):
    mock_period_from.data = "2016-02-11"
    mock_period_to.data = "2016-03-14"
    period_max = {"months": 1}

    date_range_check = get_date_range_check(period_max=period_max)

    with pytest.raises(ValidationError) as context:
        date_range_check(mock_form, mock_period_from, mock_period_to)

    assert "Enter a reporting period less than or equal to 1 month" == str(
        context.value
    )


def test_bespoke_message_playback(
    get_date_range_check, mock_form, mock_period_from, mock_period_to
):
    mock_period_from.data = "2016-02-11"
    mock_period_to.data = "2018-03-19"
    message = {"DATE_PERIOD_TOO_LARGE": "Test %(max)s"}
    period_max = {"years": 2, "months": 1, "days": 3}

    date_range_check = get_date_range_check(messages=message, period_max=period_max)

    with pytest.raises(ValidationError) as context:
        date_range_check(mock_form, mock_period_from, mock_period_to)

    assert "Test 2 years, 1 month, 3 days" == str(context.value)


@pytest.mark.parametrize(
    "period_max, expected_result",
    [
        ({"years": 2, "months": 1, "days": 3}, "2 years, 1 month, 3 days"),
        ({"months": 2, "days": 1}, "2 months, 1 day"),
        ({"days": 3}, "3 days"),
    ],
)
def test_date_range_period_max(
    get_date_range_check,
    mock_form,
    mock_period_from,
    mock_period_to,
    period_max,
    expected_result,
):
    mock_period_from.data = "2016-02-11"
    mock_period_to.data = "2018-03-19"

    date_range_check = get_date_range_check(period_max=period_max)

    with pytest.raises(ValidationError) as context:
        date_range_check(mock_form, mock_period_from, mock_period_to)

    assert f"Enter a reporting period less than or equal to {expected_result}" == str(
        context.value
    )


@pytest.mark.parametrize(
    "period_min, expected_result",
    [
        ({"years": 3, "months": 2}, "3 years, 2 months"),
        ({"years": 3, "days": 2}, "3 years, 2 days"),
        ({"years": 3}, "3 years"),
        ({"months": 3}, "3 months"),
    ],
)
def test_date_range_period_min(
    get_date_range_check,
    mock_form,
    mock_period_from,
    mock_period_to,
    period_min,
    expected_result,
):
    mock_period_from.data = "2016-02-11"
    mock_period_to.data = "2016-03-19"

    date_range_check = get_date_range_check(period_min=period_min)

    with pytest.raises(ValidationError) as context:
        date_range_check(mock_form, mock_period_from, mock_period_to)

    assert (
        f"Enter a reporting period greater than or equal to {expected_result}"
        == str(context.value)
    )


def test_valid_day_month_year_date_range(
    get_date_range_check, mock_form, mock_period_from, mock_period_to
):
    mock_period_from.data = "2016-09-01"
    mock_period_to.data = "2018-01-01"

    date_range_check = get_date_range_check()

    try:
        date_range_check(mock_form, mock_period_from, mock_period_to)
    except ValidationError:
        pytest.fail("Valid day month year date range raised ValidationError")


def test_valid_month_year_date_range(
    get_date_range_check, mock_form, mock_period_from, mock_period_to
):
    mock_period_from.data = "2016-09"
    mock_period_to.data = "2018-01"

    date_range_check = get_date_range_check()

    try:
        date_range_check(mock_form, mock_period_from, mock_period_to)
    except ValidationError:
        pytest.fail("Valid month year date range raised ValidationError")


def test_date_range_and_period_valid(
    get_date_range_check, mock_form, mock_period_from, mock_period_to
):
    mock_period_from.data = "2016-01-01"
    mock_period_to.data = "2017-01-05"
    period_min = {"days": 50}
    period_max = {"years": 1, "months": 1, "days": 5}

    date_range_check = get_date_range_check(
        period_min=period_min, period_max=period_max
    )

    try:
        date_range_check(mock_form, mock_period_from, mock_period_to)
    except ValidationError:
        pytest.fail("Valid date range and period raised ValidationError")
