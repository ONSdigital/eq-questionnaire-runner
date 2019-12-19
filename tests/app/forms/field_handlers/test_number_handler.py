# pylint: disable=unused-argument
from wtforms import Form

from app.forms.field_handlers.number_handler import NumberHandler
from app.forms.fields.decimal_field_with_separator import DecimalFieldWithSeparator
from app.forms.fields.integer_field_with_separator import IntegerFieldWithSeparator
from app.forms.error_messages import error_messages


def get_test_form_class(answer_schema, messages=None):
    handler = NumberHandler(answer_schema, error_messages=messages)

    class TestForm(Form):
        test_field = handler.get_field()

    return TestForm


class DummyPostData(dict):
    def getlist(self, key):
        v = self[key]
        if not isinstance(v, (list, tuple)):
            v = [v]
        return v


def test_integer_field():
    answer_schema = {
        'alias': 'chewies_age',
        'guidance': '',
        'id': 'chewies-age-answer',
        'mandatory': False,
        'label': 'How old is Chewy?',
        'type': 'Number',
        'validation': {
            'messages': {
                'NUMBER_TOO_LARGE': 'No one lives that long, not even Yoda',
                'NUMBER_TOO_SMALL': 'Negative age you can not be.',
                'INVALID_NUMBER': 'Please enter your age.',
            }
        },
    }

    form_class = get_test_form_class(answer_schema)
    form = form_class()

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

    form_class = get_test_form_class(answer_schema)
    form = form_class()

    assert isinstance(form.test_field, DecimalFieldWithSeparator)
    assert form.test_field.label.text == answer_schema['label']
    assert form.test_field.description == answer_schema['guidance']


def test_currency_field():
    answer_schema = {
        'guidance': '',
        'id': 'a04a516d-502d-4068-bbed-a43427c68cd9',
        'mandatory': False,
        'label': '',
        'type': 'Currency',
        'validation': {
            'messages': {
                'NUMBER_TOO_LARGE': 'How much, fool you must be',
                'NUMBER_TOO_SMALL': 'How can it be negative?',
                'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
            }
        },
    }

    form_class = get_test_form_class(answer_schema)
    form = form_class()

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

    form_class = get_test_form_class(answer_schema)
    form = form_class()

    assert isinstance(form.test_field, IntegerFieldWithSeparator)
    assert form.test_field.label.text == answer_schema['label']
    assert form.test_field.description == answer_schema['description']


def test_manual_min(app):
    answer_schema = {
        'min_value': {'value': 10},
        'label': 'Min Test',
        'mandatory': False,
        'validation': {
            'messages': {
                'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                'NUMBER_TOO_SMALL': 'The minimum value allowed is 10. Please correct your answer.',
            }
        },
        'id': 'test-range',
        'type': 'Currency',
    }

    test_form_class = get_test_form_class(answer_schema)
    form = test_form_class(DummyPostData(test_field=['9']))

    form.validate()

    assert (
        form.errors['test_field'][0]
        == answer_schema['validation']['messages']['NUMBER_TOO_SMALL']
    )


def test_manual_max(app):
    answer_schema = {
        'max_value': {'value': 20},
        'label': 'Max Test',
        'mandatory': False,
        'validation': {
            'messages': {
                'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                'NUMBER_TOO_LARGE': 'The maximum value allowed is 20. Please correct your answer.',
            }
        },
        'id': 'test-range',
        'type': 'Currency',
    }

    test_form_class = get_test_form_class(answer_schema)
    form = test_form_class(DummyPostData(test_field=['21']))

    form.validate()

    assert (
        form.errors['test_field'][0]
        == answer_schema['validation']['messages']['NUMBER_TOO_LARGE']
    )


def test_manual_decimal(app):
    answer_schema = {
        'decimal_places': 2,
        'label': 'Range Test 10 to 20',
        'mandatory': False,
        'validation': {
            'messages': {
                'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                'INVALID_DECIMAL': 'Please enter a number to 2 decimal places.',
            }
        },
        'id': 'test-range',
        'type': 'Currency',
    }

    test_form_class = get_test_form_class(answer_schema)
    form = test_form_class(DummyPostData(test_field=['1.234']))
    form.validate()

    assert (
        form.errors['test_field'][0]
        == answer_schema['validation']['messages']['INVALID_DECIMAL']
    )


def test_zero_max(app):
    max_value = 0

    answer_schema = {
        'max_value': {'value': max_value},
        'label': 'Max Test',
        'mandatory': False,
        'id': 'test-range',
        'type': 'Currency',
    }
    error_message = error_messages['NUMBER_TOO_LARGE'] % dict(max=max_value)

    test_form_class = get_test_form_class(answer_schema, messages=error_messages)
    form = test_form_class(DummyPostData(test_field=['1']))
    form.validate()

    assert form.errors['test_field'][0] == error_message


def test_zero_min(app):
    min_value = 0

    answer_schema = {
        'max_value': {'value': min_value},
        'label': 'Max Test',
        'mandatory': False,
        'id': 'test-range',
        'type': 'Currency',
    }
    error_message = error_messages['NUMBER_TOO_SMALL'] % dict(min=min_value)

    test_form_class = get_test_form_class(answer_schema, messages=error_messages)
    form = test_form_class(DummyPostData(test_field=['-1']))
    form.validate()

    assert form.errors['test_field'][0] == error_message


def test_value_range(app):
    answer_schema = {
        'min_value': {'value': 10},
        'max_value': {'value': 20},
        'label': 'Range Test 10 to 20',
        'mandatory': False,
        'validation': {
            'messages': {
                'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                'NUMBER_TOO_SMALL': 'The minimum value allowed is 10. Please correct your answer.',
                'NUMBER_TOO_LARGE': 'The maximum value allowed is 20. Please correct your answer.',
            }
        },
        'id': 'test-range',
        'type': 'Currency',
    }

    test_form_class = get_test_form_class(answer_schema)
    form = test_form_class(DummyPostData(test_field=['9']))
    form.validate()

    assert (
        form.errors['test_field'][0]
        == answer_schema['validation']['messages']['NUMBER_TOO_SMALL']
    )


def test_manual_min_exclusive(app):
    answer_schema = {
        'min_value': {'value': 10, 'exclusive': True},
        'label': 'Min Test',
        'mandatory': False,
        'validation': {
            'messages': {
                'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                'NUMBER_TOO_SMALL_EXCLUSIVE': 'The minimum value allowed is 10. Please correct your answer.',
            }
        },
        'id': 'test-range',
        'type': 'Currency',
    }

    test_form_class = get_test_form_class(answer_schema)

    form = test_form_class(DummyPostData(test_field=['10']))
    form.validate()

    assert (
        form.errors['test_field'][0]
        == answer_schema['validation']['messages']['NUMBER_TOO_SMALL_EXCLUSIVE']
    )


def test_manual_max_exclusive(app):
    answer_schema = {
        'max_value': {'value': 20, 'exclusive': True},
        'label': 'Max Test',
        'mandatory': False,
        'validation': {
            'messages': {
                'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                'NUMBER_TOO_LARGE_EXCLUSIVE': 'The maximum value allowed is 20. Please correct your answer.',
            }
        },
        'id': 'test-range',
        'type': 'Currency',
    }

    test_form_class = get_test_form_class(answer_schema)

    form = test_form_class(DummyPostData(test_field=['20']))
    form.validate()

    assert (
        form.errors['test_field'][0]
        == answer_schema['validation']['messages']['NUMBER_TOO_LARGE_EXCLUSIVE']
    )


def test_default_range():
    answer = {
        'decimal_places': 2,
        'label': 'Range Test 10 to 20',
        'mandatory': False,
        'validation': {
            'messages': {
                'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                'NUMBER_TOO_SMALL': 'The minimum value allowed is 10. Please correct your answer.',
                'NUMBER_TOO_LARGE': 'The maximum value allowed is 20. Please correct your answer.',
            }
        },
        'id': 'test-range',
        'type': 'Currency',
    }
    handler = NumberHandler(answer)
    field_references = handler.get_field_references()

    assert field_references['max_value'] == NumberHandler.MAX_NUMBER
    assert field_references['min_value'] == 0
