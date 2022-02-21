import pytest
from wtforms.fields import Field

from app.forms.fields import (
    DecimalFieldWithSeparator,
    IntegerFieldWithSeparator,
    MaxTextAreaField,
)


def test_text_area_a_wtforms_field(mock_form):
    text_area = MaxTextAreaField("LabelText", _form=mock_form, name="aName")
    assert isinstance(text_area, Field)


def test_text_area_supports_maxlength_property(mock_form):
    text_area = MaxTextAreaField(
        "TestLabel", maxlength=20, _form=mock_form, name="aName"
    )
    assert isinstance(text_area, Field)
    assert text_area.maxlength == 20


def test_integer_field(mock_form):
    integer_field = IntegerFieldWithSeparator(_form=mock_form, name="aName")
    assert isinstance(integer_field, Field)

    try:
        integer_field.process_formdata(["NonInteger"])
    except IndexError:
        pytest.fail("Exceptions should not thrown by CustomIntegerField")


def test_decimal_field(mock_form):
    decimal_field = DecimalFieldWithSeparator(_form=mock_form, name="aName")
    assert isinstance(decimal_field, Field)

    try:
        decimal_field.process_formdata(["NonDecimal"])
    except IndexError:
        pytest.fail("Exception should not be thrown by CustomDecimalField")
