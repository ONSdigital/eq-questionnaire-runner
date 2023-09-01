import pytest
from wtforms.validators import ValidationError

from app.forms import error_messages
from app.forms.validators import SumCheck, format_playback_value


@pytest.mark.parametrize(
    "conditions, calculation_total, target_total, error_type",
    (
        (["equals"], 10, 11.5, "TOTAL_SUM_NOT_EQUALS"),
        (["less than", "equals"], 20, 11.5, "TOTAL_SUM_NOT_LESS_THAN_OR_EQUALS"),
        (["less than"], 11.99, 11.5, "TOTAL_SUM_NOT_LESS_THAN"),
        (["greater than"], 11.99, 12.5, "TOTAL_SUM_NOT_GREATER_THAN"),
        (
            ["greater than", "equals"],
            11.99,
            12.5,
            "TOTAL_SUM_NOT_GREATER_THAN_OR_EQUALS",
        ),
    ),
)
@pytest.mark.usefixtures("gb_locale")
def test_sum_check_invalid_raises_ValidationError(
    conditions, calculation_total, target_total, error_type, mock_form
):
    validator = SumCheck()

    with pytest.raises(ValidationError) as exc:
        validator(mock_form, conditions, calculation_total, target_total)

    assert error_messages[error_type] % {
        "total": format_playback_value(target_total)
    } == str(exc.value)


@pytest.mark.usefixtures("gb_locale")
def test_currency_playback(mock_form):
    validator = SumCheck(currency="EUR")

    conditions = ["equals"]
    calculation_total = 10
    target_total = 11.5

    with pytest.raises(ValidationError) as exc:
        validator(mock_form, conditions, calculation_total, target_total)

    assert error_messages["TOTAL_SUM_NOT_EQUALS"] % {
        "total": format_playback_value(
            value=target_total, currency="EUR", decimal_limit=1
        ),
    } == str(exc.value)


@pytest.mark.usefixtures("gb_locale")
def test_bespoke_message_playback(mock_form):
    message = {"TOTAL_SUM_NOT_EQUALS": "Test %(total)s"}
    validator = SumCheck(messages=message)

    conditions = ["equals"]
    calculation_total = 10
    target_total = 11.5

    with pytest.raises(ValidationError) as exc:
        validator(mock_form, conditions, calculation_total, target_total)

    assert f"Test {target_total}" == str(exc.value)


@pytest.mark.usefixtures("gb_locale")
def test_invalid_multiple_conditions(mock_form):
    validator = SumCheck()

    conditions = ["less than", "greater than"]
    calculation_total = 10
    target_total = 11.5

    with pytest.raises(Exception) as exc:
        validator(mock_form, conditions, calculation_total, target_total)

    assert (
        "There are multiple conditions, but equals is not one of them. We only support <= and >="
        == str(exc.value)
    )


# pylint: disable=protected-access
def test_is_valid_raises_NotImplementedError():
    condition = "invalid_condition"
    total, target_total = 10.5, 10.5
    with pytest.raises(NotImplementedError):
        SumCheck._is_valid(condition, total, target_total)
