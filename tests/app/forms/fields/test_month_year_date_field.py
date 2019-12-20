from wtforms import validators, Form

from app.forms.fields import month_year_date_field


def test_generate_month_year_date_form_creates_empty_form():
    form_class = month_year_date_field.get_form_class([validators.Optional()])

    assert not hasattr(form_class, "day")
    assert hasattr(form_class, "month")
    assert hasattr(form_class, "year")


def test_month_year_date_form_empty_data():
    form = month_year_date_field.get_form_class([validators.Optional()])

    assert form().data is None


def test_month_year_date_form_format_data():
    data = {"field": "2000-01"}

    class TestForm(Form):
        field = month_year_date_field.MonthYearDateField([validators.Optional()])

    test_form = TestForm(data=data)

    assert test_form.field.data == "2000-01"
