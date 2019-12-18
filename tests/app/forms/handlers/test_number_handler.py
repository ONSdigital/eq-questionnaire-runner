from wtforms import Form

from app.forms.field_handlers.number_handler import NumberHandler
from app.forms.fields.decimal_field_with_separator import DecimalFieldWithSeparator
from app.forms.fields.integer_field_with_separator import IntegerFieldWithSeparator


def get_test_form(answer_schema):
    handler = NumberHandler(answer_schema)

    class TestForm(Form):
        test_field = handler.get_field()

    return TestForm()


def test_integer_field():
    answer_schema = {
        'alias': 'chewies_age',
        'guidance': '',
        'id': 'chewies-age-answer',
        'mandatory': False,
        'label': 'How old is Chewy?',
        'q_code': '1',
        'type': 'Number',
        'validation': {
            'messages': {
                'NUMBER_TOO_LARGE': 'No one lives that long, not even Yoda',
                'NUMBER_TOO_SMALL': 'Negative age you can not be.',
                'INVALID_NUMBER': 'Please enter your age.',
            }
        },
    }

    form = get_test_form(answer_schema)

    assert isinstance(form.test_field, IntegerFieldWithSeparator)
    assert form.test_field.label.text == answer_schema['label']
    assert form.test_field.description == answer_schema['guidance']


def test_decimal_field():
    answer_schema = {
        'guidance': '',
        'id': 'lightsaber-cost-answer',
        'label': 'How hot is a lightsaber in degrees C?',
        'mandatory': False,
        'type': 'Number',
        'decimal_places': 2,
        'validation': {
            'messages': {
                'NUMBER_TOO_LARGE': 'Thats hotter then the sun, Jar Jar Binks you must be',
                'NUMBER_TOO_SMALL': 'How can it be negative?',
                'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
            }
        },
    }

    form = get_test_form(answer_schema)

    assert isinstance(form.test_field, DecimalFieldWithSeparator)
    assert form.test_field.label.text == answer_schema['label']
    assert form.test_field.description == answer_schema['guidance']


def test_currency_field():
    answer_schema = {
        'guidance': '',
        'id': 'a04a516d-502d-4068-bbed-a43427c68cd9',
        'mandatory': False,
        'label': '',
        'q_code': '2',
        'type': 'Currency',
        'validation': {
            'messages': {
                'NUMBER_TOO_LARGE': 'How much, fool you must be',
                'NUMBER_TOO_SMALL': 'How can it be negative?',
                'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
            }
        },
    }

    form = get_test_form(answer_schema)

    assert isinstance(form.test_field, IntegerFieldWithSeparator)
    assert form.test_field.label.text == answer_schema['label']
    assert form.test_field.description == answer_schema['guidance']


def test_percentage_field():
    answer_schema = {
        'description': '',
        'id': 'percentage-turnover-2016-market-new-answer',
        'label': 'New to the market in 2014-2016',
        'mandatory': False,
        'q_code': '0810',
        'type': 'Percentage',
        'max_value': {'value': 100},
        'validation': {
            'messages': {
                'NUMBER_TOO_LARGE': 'How much, fool you must be',
                'NUMBER_TOO_SMALL': 'How can it be negative?',
                'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
            }
        },
    }

    form = get_test_form(answer_schema)

    assert isinstance(form.test_field, IntegerFieldWithSeparator)
    assert form.test_field.label.text == answer_schema['label']
    assert form.test_field.description == answer_schema['description']
