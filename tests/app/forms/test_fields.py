from wtforms import StringField, FormField, SelectField

from app.data_model.answer_store import AnswerStore
from app.forms.fields.max_text_area_field import MaxTextAreaField
from app.forms.fields.multiple_select_field_with_detail_answer import (
    MultipleSelectFieldWithDetailAnswer,
)
from app.forms.fields.select_field_with_detail_answer import SelectFieldWithDetailAnswer
from app.forms.fields.integer_field_with_separator import IntegerFieldWithSeparator
from app.forms.fields.decimal_field_with_separator import DecimalFieldWithSeparator

from app.forms.fields.date_field import DateField
from app.forms.field_factory import get_field
from app.forms.field_handlers.select_handler import SelectHandler
from app.forms.error_messages import error_messages
from tests.app.app_context_test_case import AppContextTestCase


# pylint: disable=no-member, too-many-public-methods
class TestFields(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self.answer_store = AnswerStore()
        self.metadata = {
            'user_id': '789473423',
            'schema_name': '0000',
            'collection_exercise_sid': 'test-sid',
            'period_id': '2016-02-01',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-02-02',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '432423423423',
            'ru_name': 'Apple',
            'return_by': '2016-07-07',
            'case_id': '1234567890',
            'case_ref': '1000000000000001',
        }

    def tearDown(self):
        super().tearDown()
        self.answer_store.clear()
        self.metadata.clear()

    def test_string_field(self):
        textfield_json = {
            'id': 'job-title-answer',
            'label': 'Job title',
            'mandatory': False,
            'guidance': '<p>Please enter your job title in the space provided.</p>',
            'type': 'TextField',
        }
        unbound_field = get_field(
            textfield_json, error_messages, self.answer_store, self.metadata
        )

        self.assertEqual(unbound_field.field_class, StringField)
        self.assertEqual(unbound_field.kwargs['label'], textfield_json['label'])
        self.assertEqual(
            unbound_field.kwargs['description'], textfield_json['guidance']
        )

    def test_text_area_field(self):
        textarea_json = {
            'guidance': '',
            'id': 'answer',
            'label': 'Enter your comments',
            'mandatory': False,
            'q_code': '0',
            'type': 'TextArea',
        }

        unbound_field = get_field(
            textarea_json, error_messages, self.answer_store, self.metadata
        )

        self.assertEqual(unbound_field.field_class, MaxTextAreaField)
        self.assertEqual(unbound_field.kwargs['label'], textarea_json['label'])
        self.assertEqual(unbound_field.kwargs['description'], textarea_json['guidance'])

    def test_date_field(self):
        date_json = {
            'guidance': 'Please enter a date',
            'id': 'period-to',
            'label': 'Period to',
            'mandatory': True,
            'type': 'Date',
            'validation': {
                'messages': {
                    'INVALID_DATE': 'The date entered is not valid.  Please correct your answer.',
                    'MANDATORY': 'Please provide an answer to continue.',
                }
            },
        }

        with self.app_request_context('/'):
            unbound_field = get_field(
                date_json, error_messages, self.answer_store, self.metadata
            )

        self.assertEqual(unbound_field.field_class, DateField)
        self.assertEqual(unbound_field.kwargs['label'], date_json['label'])
        self.assertEqual(unbound_field.kwargs['description'], date_json['guidance'])

    def test_month_year_date_field(self):
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
                    'MANDATORY': 'Please provide an answer to continue.',
                }
            },
        }

        with self.app_request_context('/'):
            unbound_field = get_field(
                date_json, error_messages, self.answer_store, self.metadata
            )

        self.assertEqual(unbound_field.field_class, DateField)
        self.assertEqual(unbound_field.kwargs['label'], date_json['label'])
        self.assertEqual(unbound_field.kwargs['description'], date_json['guidance'])

    def test_year_date_field(self):
        date_json = {
            'guidance': '',
            'id': 'month-year-answer',
            'label': 'Date',
            'mandatory': True,
            'options': [],
            'q_code': '11',
            'type': 'YearDate',
            'validation': {
                'messages': {
                    'INVALID_DATE': 'The date entered is not valid.  Please correct your answer.',
                    'MANDATORY': 'Please provide an answer to continue.',
                }
            },
        }

        with self.app_request_context('/'):
            unbound_field = get_field(
                date_json, error_messages, self.answer_store, self.metadata
            )

        self.assertEqual(unbound_field.field_class, DateField)
        self.assertEqual(unbound_field.kwargs['label'], date_json['label'])
        self.assertEqual(unbound_field.kwargs['description'], date_json['guidance'])

    def test_duration_field(self):
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

        with self.app_request_context('/'):
            unbound_field = get_field(
                date_json, error_messages, self.answer_store, self.metadata
            )

        self.assertEqual(unbound_field.field_class, FormField)
        self.assertEqual(unbound_field.kwargs['label'], date_json['label'])
        self.assertEqual(unbound_field.kwargs['description'], date_json['guidance'])

    def test_radio_field(self):
        radio_json = {
            'guidance': '',
            'id': 'choose-your-side-answer',
            'label': 'Choose a side',
            'mandatory': True,
            'options': [
                {
                    'label': 'Light Side',
                    'value': 'Light Side',
                    'description': 'The light side of the Force',
                },
                {
                    'label': 'Dark Side',
                    'value': 'Dark Side',
                    'description': 'The dark side of the Force',
                },
                {'label': 'I prefer Star Trek', 'value': 'I prefer Star Trek'},
                {'label': 'Other', 'value': 'Other'},
            ],
            'q_code': '20',
            'type': 'Radio',
        }

        unbound_field = get_field(
            radio_json, error_messages, self.answer_store, self.metadata
        )

        expected_choices = [
            (option['label'], option['value'], None) for option in radio_json['options']
        ]

        self.assertEqual(unbound_field.field_class, SelectFieldWithDetailAnswer)
        self.assertTrue(
            unbound_field.kwargs['coerce'], SelectHandler.coerce_str_unless_none
        )
        self.assertEqual(unbound_field.kwargs['label'], radio_json['label'])
        self.assertEqual(unbound_field.kwargs['description'], radio_json['guidance'])
        self.assertEqual(unbound_field.kwargs['choices'], expected_choices)

    def test_dropdown_field(self):
        dropdown_json = {
            'type': 'Dropdown',
            'id': 'dropdown-mandatory-with-label-answer',
            'mandatory': True,
            'label': 'Please choose an option',
            'description': 'This is a mandatory dropdown, therefore you must select a value!.',
            'options': [
                {'label': 'Liverpool', 'value': 'Liverpool'},
                {'label': 'Chelsea', 'value': 'Chelsea'},
                {'label': 'Rugby is better!', 'value': 'Rugby is better!'},
            ],
        }

        with self.app_request_context('/'):
            unbound_field = get_field(
                dropdown_json, error_messages, self.answer_store, self.metadata
            )

        expected_choices = [('', 'Select an answer')] + [
            (option['label'], option['value']) for option in dropdown_json['options']
        ]

        self.assertEqual(unbound_field.field_class, SelectField)
        self.assertEqual(unbound_field.kwargs['label'], dropdown_json['label'])
        self.assertEqual(unbound_field.kwargs['description'], '')
        self.assertEqual(unbound_field.kwargs['default'], '')
        self.assertEqual(unbound_field.kwargs['choices'], expected_choices)

    def test__coerce_str_unless_none(self):
        self.assertEqual(SelectHandler.coerce_str_unless_none(1), '1')
        self.assertEqual(SelectHandler.coerce_str_unless_none('bob'), 'bob')
        self.assertEqual(SelectHandler.coerce_str_unless_none(12323245), '12323245')
        self.assertEqual(SelectHandler.coerce_str_unless_none('9887766'), '9887766')
        self.assertEqual(SelectHandler.coerce_str_unless_none('None'), 'None')
        self.assertEqual(SelectHandler.coerce_str_unless_none(None), None)

    def test_checkbox_field(self):
        checkbox_json = {
            'guidance': '',
            'id': 'opening-crawler-answer',
            'label': '',
            'mandatory': False,
            'options': [
                {'label': 'Luke Skywalker', 'value': 'Luke Skywalker'},
                {'label': 'Han Solo', 'value': 'Han Solo'},
                {'label': 'The Emperor', 'value': 'The Emperor'},
                {'label': 'R2D2', 'value': 'R2D2'},
                {'label': 'Senator Amidala', 'value': 'Senator Amidala'},
                {'label': 'Yoda', 'value': 'Yoda'},
            ],
            'q_code': '7',
            'type': 'Checkbox',
        }

        unbound_field = get_field(
            checkbox_json, error_messages, self.answer_store, self.metadata
        )

        expected_choices = [
            (option['value'], option['label'], None)
            for option in checkbox_json['options']
        ]

        self.assertEqual(unbound_field.field_class, MultipleSelectFieldWithDetailAnswer)
        self.assertEqual(unbound_field.kwargs['label'], checkbox_json['label'])
        self.assertEqual(unbound_field.kwargs['description'], checkbox_json['guidance'])
        self.assertEqual(unbound_field.kwargs['choices'], expected_choices)
        self.assertEqual(len(unbound_field.kwargs['validators']), 1)

    def test_integer_field(self):
        integer_json = {
            'alias': 'chewies_age',
            'guidance': '',
            'id': 'chewies-age-answer',
            'label': 'How old is Chewy?',
            'mandatory': True,
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

        unbound_field = get_field(
            integer_json, error_messages, self.answer_store, self.metadata
        )

        self.assertEqual(unbound_field.field_class, IntegerFieldWithSeparator)
        self.assertEqual(unbound_field.kwargs['label'], integer_json['label'])
        self.assertEqual(unbound_field.kwargs['description'], integer_json['guidance'])

    def test_decimal_field(self):
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

        unbound_field = get_field(
            decimal_json, error_messages, self.answer_store, self.metadata
        )

        self.assertEqual(unbound_field.field_class, DecimalFieldWithSeparator)
        self.assertEqual(unbound_field.kwargs['label'], decimal_json['label'])
        self.assertEqual(unbound_field.kwargs['description'], decimal_json['guidance'])

    def test_currency_field(self):
        currency_json = {
            'guidance': '',
            'id': 'a04a516d-502d-4068-bbed-a43427c68cd9',
            'label': '',
            'mandatory': True,
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

        unbound_field = get_field(
            currency_json, error_messages, self.answer_store, self.metadata
        )

        self.assertEqual(unbound_field.field_class, IntegerFieldWithSeparator)
        self.assertEqual(unbound_field.kwargs['label'], currency_json['label'])
        self.assertEqual(unbound_field.kwargs['description'], currency_json['guidance'])

    def test_percentage_field(self):
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

        unbound_field = get_field(
            percentage_json, error_messages, self.answer_store, self.metadata
        )

        self.assertEqual(unbound_field.field_class, IntegerFieldWithSeparator)
        self.assertEqual(unbound_field.kwargs['label'], percentage_json['label'])
        self.assertEqual(
            unbound_field.kwargs['description'], percentage_json['description']
        )

    def test_invalid_field_type_raises_on_invalid(self):
        # Given
        invalid_field_type = 'Football'
        # When / Then
        with self.assertRaises(KeyError):
            get_field(
                {'type': invalid_field_type},
                error_messages,
                self.answer_store,
                self.metadata,
            )
