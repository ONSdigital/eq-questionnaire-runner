from app.forms.field_handlers.year_date_handler import YearDateHandler
from app.forms.fields.year_date_field import YearDateField


def test_year_date_field_created_with_guidance():
    date_json = {
        'guidance': '',
        'id': 'month-year-answer',
        'label': 'Date',
        'mandatory': True,
        'options': [],
        'q_code': '11',
        'type': 'MonthYearDate',
        'validation': {
            'messages': {
                'INVALID_DATE': 'The date entered is not valid.  Please correct your answer.',
                'MANDATORY_DATE': 'Please provide an answer to continue.',
            }
        },
    }

    date_handler = YearDateHandler(date_json)
    unbound_field = date_handler.get_field()

    assert unbound_field.field_class == YearDateField
    assert unbound_field.kwargs['label'] == date_json['label']
    assert unbound_field.kwargs['description'] == date_json['guidance']
