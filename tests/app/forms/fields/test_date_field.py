from wtforms import validators, Form

from app.forms.fields import date_field


def test_generate_date_form_creates_empty_form():
    form_class = date_field.get_form_class([validators.Optional()])

    assert hasattr(form_class, "day")
    assert hasattr(form_class, "month")
    assert hasattr(form_class, "year")


def test_date_form_empty_data():
    form = date_field.get_form_class([validators.Optional()])

    assert form().data is None


def test_date_form_format_data():
    data = {"field": "2000-01-01"}

    class TestForm(Form):
        field = date_field.DateField([validators.Optional()])

    test_form = TestForm(data=data)

    assert test_form.field.data == "2000-01-01"
