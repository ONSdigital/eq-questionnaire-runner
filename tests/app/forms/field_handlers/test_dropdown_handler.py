from wtforms import SelectField, Form

from app.forms.field_handlers.dropdown_handler import DropdownHandler


def test_get_field():
    dropdown_json = {
        'type': 'Dropdown',
        'id': 'dropdown-with-label-answer',
        'mandatory': False,
        'label': 'Please choose an option',
        'description': 'This is an optional dropdown',
        'options': [
            {'label': 'Liverpool', 'value': 'Liverpool'},
            {'label': 'Chelsea', 'value': 'Chelsea'},
            {'label': 'Rugby is better!', 'value': 'Rugby is better!'},
        ],
    }

    handler = DropdownHandler(dropdown_json)

    expected_choices = [('', 'Select an answer')] + [
        (option['label'], option['value']) for option in dropdown_json['options']
    ]

    class TestForm(Form):
        test_field = handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, SelectField)
    assert form.test_field.label.text == dropdown_json['label']
    assert form.test_field.description == ''
    assert form.test_field.default == ''
    assert form.test_field.choices == expected_choices
