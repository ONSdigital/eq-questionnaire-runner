from wtforms import FormField, Form

from app.forms.field_handlers.duration_handler import DurationHandler


def test_get_field():
    date_json = {
        'guidance': '',
        'id': 'year-month-answer',
        'label': 'Duration',
        'mandatory': True,
        'type': 'Duration',
        'units': ['years', 'months'],
    }

    handler = DurationHandler(date_json)

    class TestForm(Form):
        test_field = handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, FormField)
    assert form.test_field.label.text == date_json['label']
    assert form.test_field.description == date_json['guidance']
