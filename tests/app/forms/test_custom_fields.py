from decimal import Decimal

import pytest
from wtforms.fields import Field

from app.forms.fields import (
    DecimalFieldWithSeparator,
    IntegerFieldWithSeparator,
    MaxTextAreaField,
)


def test_text_area_a_wtforms_field(mock_form):
    text_area = MaxTextAreaField(
        label="LabelText",
        _form=mock_form,
        name="aName",
        rows=0,
        maxlength=0,
    )
    assert isinstance(text_area, Field)


def test_text_area_supports_maxlength_property(mock_form):
    text_area = MaxTextAreaField(
        label="TestLabel",
        maxlength=20,
        _form=mock_form,
        name="aName",
        rows=0,
    )
    assert isinstance(text_area, Field)
    assert text_area.maxlength == 20


@pytest.mark.usefixtures("gb_locale")
def test_integer_field(mock_form):
    integer_field = IntegerFieldWithSeparator(_form=mock_form, name="aName")
    assert isinstance(integer_field, Field)

    try:
        integer_field.process_formdata(["NonInteger"])
    except IndexError:
        pytest.fail("Exceptions should not thrown by CustomIntegerField")


@pytest.mark.usefixtures("gb_locale")
@pytest.mark.parametrize(
    "number_input, result",
    [
        ("_110", 110),
        ("1_10", 110),
        ("1__10", 110),
        ("1_1,0", 110),
        ("_1_1,0,0", 1100),
        ("1.10", None),
    ],
)
def test_integer_field_inputs(mock_form, number_input, result):
    integer_field = IntegerFieldWithSeparator(_form=mock_form, name="aName")
    integer_field.process_formdata([number_input])

    assert integer_field.data == result


@pytest.mark.usefixtures("gb_locale")
@pytest.mark.parametrize(
    "number_input, result",
    [
        ("1_1,0", Decimal("110")),
        ("1.10", Decimal("1.1")),
        ("_1.1_0", Decimal("1.1")),
        ("_1.1_0,0", Decimal("1.1")),
        ("_1._1,0,0", Decimal("1.1")),
    ],
)
def test_decimal_field_inputs(mock_form, number_input, result):
    decimal_field = DecimalFieldWithSeparator(_form=mock_form, name="aName")
    decimal_field.process_formdata([number_input])

    assert decimal_field.data == result


@pytest.mark.usefixtures("gb_locale")
def test_decimal_field(mock_form):
    decimal_field = DecimalFieldWithSeparator(_form=mock_form, name="aName")
    assert isinstance(decimal_field, Field)

    try:
        decimal_field.process_formdata(["NonDecimal"])
    except IndexError:
        pytest.fail("Exception should not be thrown by CustomDecimalField")
