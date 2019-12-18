from wtforms import FormField

from app.forms.field_handlers.duration_handler import DurationHandler


def test_get_field():
    date_json = {
        'guidance': '',
        'id': 'year-month-answer',
        'label': 'Duration',
        'mandatory': True,
        'options': [],
        'q_code': '11',
        'type': 'Duration',
        'units': ['years', 'months'],
        'validation': {
            'messages': {
                'INVALID_DURATION': 'The duration entered is not valid.  Please correct your answer.',
                'MANDATORY_DURATION': 'Please provide a duration to continue.',
            }
        },
    }

    text_area_handler = DurationHandler(date_json)
    unbound_field = text_area_handler.get_field()

    assert unbound_field.field_class == FormField
    assert unbound_field.kwargs['label'] == date_json['label']
    assert unbound_field.kwargs['description'] == date_json['guidance']
