from wtforms import Form

from app.forms.fields import date_field
from app.forms.validators import OptionalForm


def test_generate_date_form_creates_empty_form():
    form_class = date_field.get_form_class([OptionalForm()])

    assert hasattr(form_class, "day")
    assert hasattr(form_class, "month")
    assert hasattr(form_class, "year")


def test_date_form_empty_data():
    form = date_field.get_form_class([OptionalForm()])

    assert form().data is None


def test_date_form_format_data():
    data = {"field": "2000-01-01"}

    class TestForm(Form):
        field = date_field.DateField(validators=[OptionalForm()], description="")

    test_form = TestForm(data=data)

    assert test_form.field.data == "2000-01-01"
