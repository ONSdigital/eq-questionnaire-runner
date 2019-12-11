import unittest
from unittest.mock import Mock
from wtforms.fields import Field
from app.forms.fields.max_text_area_field import MaxTextAreaField
from app.forms.fields.integer_field_with_separator import IntegerFieldWithSeparator
from app.forms.fields.decimal_field_with_separator import DecimalFieldWithSeparator


class TestMaxTextAreaField(unittest.TestCase):
    def setUp(self):
        self.mock_form = Mock()

    def test_text_area_a_wtforms_field(self):
        text_area = MaxTextAreaField('LabelText', _form=self.mock_form, _name='aName')
        self.assertIsInstance(text_area, Field)

    def test_text_area_supports_maxlength_property(self):
        text_area = MaxTextAreaField(
            'TestLabel', maxlength=20, _form=self.mock_form, _name='aName'
        )
        self.assertIsInstance(text_area, Field)
        self.assertEqual(text_area.maxlength, 20)

    def test_integer_field(self):
        integer_field = IntegerFieldWithSeparator(_form=self.mock_form, _name='aName')
        self.assertIsInstance(integer_field, Field)

        try:
            integer_field.process_formdata(['NonInteger'])
        except IndexError:
            self.fail('Exceptions should not thrown by CustomIntegerField')

    def test_decimal_field(self):
        decimal_field = DecimalFieldWithSeparator(_form=self.mock_form, _name='aName')
        self.assertIsInstance(decimal_field, Field)

        try:
            decimal_field.process_formdata(['NonDecimal'])
        except IndexError:
            self.fail('Exception should not be thrown by CustomDecimalField')
