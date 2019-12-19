from wtforms import FormField

from app.forms.field_handlers.duration_handler import DurationHandler


def test_get_field():
    date_json = {
        'guidance': '',
        'id': 'year-month-answer',
        'label': 'Duration',
        'mandatory': True,
        'options': [],
        'type': 'Duration',
        'units': ['years', 'months']
    }

    text_area_handler = DurationHandler(date_json)
    unbound_field = text_area_handler.get_field()

    assert unbound_field.field_class == FormField
    assert unbound_field.kwargs['label'] == date_json['label']
    assert unbound_field.kwargs['description'] == date_json['guidance']
