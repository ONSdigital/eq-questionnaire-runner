import pytest
from wtforms.validators import StopValidation

from app.forms.validators import OptionalForm


@pytest.mark.parametrize(
    "day_month_year",
    (
        [[""], [], [""]],
        [[], [""]],
    ),
)
def test_date_validator_day_month_year_invalid_raises_StopValidation(
    day_month_year, mocker, mock_form, mock_field
):
    validator = OptionalForm()

    mock_day = mocker.MagicMock()
    mock_month = mocker.MagicMock()
    mock_year = mocker.MagicMock()

    mock_month.raw_data = day_month_year[-2]
    mock_year.raw_data = day_month_year[-1]

    if len(day_month_year) == 3:
        mock_day.raw_data = day_month_year[-3]
        comp = [mock_day, mock_month, mock_year]

    elif len(day_month_year) == 2:
        comp = [mock_month, mock_year]

    mock_form.__iter__ = mocker.MagicMock(return_value=iter(comp))

    with pytest.raises(StopValidation) as exc:
        validator(mock_form, mock_field)

    assert "" == str(exc.value)


@pytest.mark.parametrize(
    "day_month_year",
    (
        [[""], ["01"], ["2015"]],
        [["01"], [""]],
    ),
)
def test_date_validator_day_month_year(day_month_year, mocker, mock_form, mock_field):
    validator = OptionalForm()

    mock_day = mocker.MagicMock()
    mock_month = mocker.MagicMock()
    mock_year = mocker.MagicMock()

    mock_month.raw_data = day_month_year[-2]
    mock_year.raw_data = day_month_year[-1]

    if len(day_month_year) == 3:
        mock_day.raw_data = day_month_year[-3]
        comp = [mock_day, mock_month, mock_year]

    elif len(day_month_year) == 2:
        comp = [mock_month, mock_year]

    mock_form.__iter__ = mocker.MagicMock(return_value=iter(comp))

    validator(mock_form, mock_field)
