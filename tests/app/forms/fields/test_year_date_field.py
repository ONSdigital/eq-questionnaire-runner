from wtforms import validators, Form

from app.forms.fields import year_date_field


def test_generate_year_date_form_creates_empty_form():
    form_class = year_date_field.get_form_class([validators.Optional()])

    assert not hasattr(form_class, "day")
    assert not hasattr(form_class, "month")
    assert hasattr(form_class, "year")


def test_year_date_form_empty_data():
    form = year_date_field.get_form_class([validators.Optional()])

    assert form().data is None


def test_year_date_form_format_data():
    data = {"field": "2000"}

    class TestForm(Form):
        field = year_date_field.YearDateField([validators.Optional()])

    test_form = TestForm(data=data)

    assert test_form.field.data == "2000"
