from wtforms import Form

from app.forms.field_handlers.number_handler import NumberHandler
from app.forms.fields.decimal_field_with_separator import DecimalFieldWithSeparator
from app.forms.fields.integer_field_with_separator import IntegerFieldWithSeparator


def test_integer_field():
    integer_json = {
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

    handler = NumberHandler(integer_json)

    class TestForm(Form):
        test_field = handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, IntegerFieldWithSeparator)
    assert form.test_field.label.text == integer_json['label']
    assert form.test_field.description == integer_json['guidance']


def test_decimal_field():
    decimal_json = {
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

    handler = NumberHandler(decimal_json)

    class TestForm(Form):
        test_field = handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, DecimalFieldWithSeparator)
    assert form.test_field.label.text == decimal_json['label']
    assert form.test_field.description == decimal_json['guidance']


def test_currency_field():
    currency_json = {
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

    handler = NumberHandler(currency_json)

    class TestForm(Form):
        test_field = handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, IntegerFieldWithSeparator)
    assert form.test_field.label.text == currency_json['label']
    assert form.test_field.description == currency_json['guidance']


def test_percentage_field():
    percentage_json = {
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

    handler = NumberHandler(percentage_json)

    class TestForm(Form):
        test_field = handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, IntegerFieldWithSeparator)
    assert form.test_field.label.text == percentage_json['label']
    assert form.test_field.description == percentage_json['description']
