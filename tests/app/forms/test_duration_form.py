import pytest

from app.forms import error_messages
from app.forms.duration_form import get_duration_form


def test_init():
    answer_schema = {
        "mandatory": False,
        "units": ["years", "months"],
        "validation": {
            "messages": {
                "INVALID_DURATION": "The duration entered is not valid.  Please correct your answer",
                "MANDATORY_DURATION": "Please provide a duration to continue",
            }
        },
    }
    form_class = get_duration_form(answer_schema, error_messages)
    form = form_class()

    assert form.data is None
    assert (
        form.answer_errors["INVALID_DURATION"]
        == answer_schema["validation"]["messages"]["INVALID_DURATION"]
    )

    assert (
        form.answer_errors["MANDATORY_DURATION"]
        == answer_schema["validation"]["messages"]["MANDATORY_DURATION"]
    )


def test_zero():
    form_class = get_duration_form(
        {"mandatory": False, "units": ["years", "months"]}, error_messages
    )
    form = form_class()
    form.years.raw_data = ["0"]
    form.years.data = 0
    form.months.raw_data = ["0"]
    form.months.data = 0

    assert form.data["years"] == 0
    assert form.data["months"] == 0


@pytest.mark.parametrize(
    "mandatory,years,months,valid,error",
    (
        (False, "5", "4", True, None),
        (True, "5", "4", True, None),
        (False, "", "", True, None),
        (True, "", "", False, "Enter a duration"),
        (False, "5", "", False, "Enter a valid duration"),
        (True, "5", "", False, "Enter a valid duration"),
        (False, "", "4", False, "Enter a valid duration"),
        (True, "", "4", False, "Enter a valid duration"),
        (False, "5", "word", False, "Enter a valid duration"),
        (True, "5", "word", False, "Enter a valid duration"),
        (False, "5", "12", False, "Enter a valid duration"),
        (True, "5", "12", False, "Enter a valid duration"),
        (False, "5", "-1", False, "Enter a valid duration"),
        (True, "5", "-1", False, "Enter a valid duration"),
        (False, "-1", "4", False, "Enter a valid duration"),
        (True, "-1", "4", False, "Enter a valid duration"),
        (False, "5", None, True, None),
        (True, "5", None, True, None),
        (False, "", None, True, None),
        (True, "", None, False, "Enter a duration"),
        (False, "word", None, False, "Enter a valid duration"),
        (True, "word", None, False, "Enter a valid duration"),
        (False, "-1", None, False, "Enter a valid duration"),
        (True, "-1", None, False, "Enter a valid duration"),
        (False, None, "5", True, None),
        (True, None, "5", True, None),
        (False, None, "", True, None),
        (True, None, "", False, "Enter a duration"),
        (False, None, "word", False, "Enter a valid duration"),
        (True, None, "word", False, "Enter a valid duration"),
        (False, None, "-1", False, "Enter a valid duration"),
        (True, None, "-1", False, "Enter a valid duration"),
        (False, None, "12", True, None),
        (True, None, "12", True, None),
    ),
)
def test_validation(mandatory, years, months, valid, error, app):
    units = []
    if years is not None:
        units.append("years")
    if months is not None:
        units.append("months")

    form_class = get_duration_form(
        {"mandatory": mandatory, "units": units}, error_messages
    )

    form = form_class()
    if years is not None:
        form.years.raw_data = [years]
        form.years.data = to_int(years)
    if months is not None:
        form.months.raw_data = [months]
        form.months.data = to_int(months)

    with app.test_request_context("/"):
        assert form.validate() == valid

        if error:
            assert getattr(form, units[0]).errors[0] == error


def to_int(value):
    try:
        return int(value)
    except ValueError:
        return None
