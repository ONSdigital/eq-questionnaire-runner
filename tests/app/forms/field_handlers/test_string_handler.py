from wtforms import StringField, Form

from app.forms.field_handlers.string_handler import StringHandler


def test_string_field():
    textfield_json = {
        'id': 'job-title-answer',
        'label': 'Job title',
        'mandatory': False,
        'guidance': '<p>Please enter your job title in the space provided.</p>',
        'type': 'TextField',
    }
    string_handler = StringHandler(textfield_json)

    class TestForm(Form):
        test_field = string_handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, StringField)
    assert form.test_field.label.text == textfield_json['label']
    assert form.test_field.description == textfield_json['guidance']
