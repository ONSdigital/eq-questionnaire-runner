from datetime import datetime

from dateutil.relativedelta import relativedelta
from mock import patch
from wtforms import Form

from app.data_model.answer_store import AnswerStore, Answer
from app.forms.date_form import (
    transform_date_by_offset,
    get_date_limits,
    validate_mandatory_date,
    get_form,
    DateFormType,
    DateField,
    get_referenced_date,
    get_date_form_validators,
)
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.rules import convert_to_datetime
from app.utilities.schema import load_schema_from_name
from tests.app.app_context_test_case import AppContextTestCase


class TestDateForm(AppContextTestCase):
    def test_generate_date_form_creates_empty_form(self):
        schema = load_schema_from_name('test_dates')
        error_messages = schema.error_messages

        with self.app_request_context('/'):
            validators = get_date_form_validators(
                DateFormType.YearMonthDay,
                schema.get_answers_by_answer_id('single-date-answer')[0],
                None,
                None,
                error_messages=error_messages,
            )
            form = get_form(DateFormType.YearMonthDay, validators)

        self.assertTrue(hasattr(form, 'day'))
        self.assertTrue(hasattr(form, 'month'))
        self.assertTrue(hasattr(form, 'year'))

    def test_generate_month_year_date_form_creates_empty_form(self):
        schema = load_schema_from_name('test_dates')
        error_messages = schema.error_messages

        with self.app_request_context('/'):
            validators = get_date_form_validators(
                DateFormType.YearMonth,
                schema.get_answers_by_answer_id('month-year-answer')[0],
                None,
                None,
                error_messages=error_messages,
            )
            form = get_form(DateFormType.YearMonth, validators)

        self.assertFalse(hasattr(form, 'day'))
        self.assertTrue(hasattr(form, 'month'))
        self.assertTrue(hasattr(form, 'year'))

    def test_generate_year_date_form_creates_empty_form(self):
        schema = load_schema_from_name('test_dates')
        error_messages = schema.error_messages

        validators = get_date_form_validators(
            DateFormType.Year,
            schema.get_answers_by_answer_id('year-date-answer')[0],
            None,
            None,
            error_messages=error_messages,
        )
        form = get_form(DateFormType.Year, validators)

        self.assertFalse(hasattr(form, 'day'))
        self.assertFalse(hasattr(form, 'month'))
        self.assertTrue(hasattr(form, 'year'))

    def test_date_form_empty_data(self):
        schema = load_schema_from_name('test_dates')
        error_messages = schema.error_messages

        with self.app_request_context('/'):
            validators = get_date_form_validators(
                DateFormType.YearMonthDay,
                schema.get_answers_by_answer_id('single-date-answer')[0],
                None,
                None,
                error_messages=error_messages,
            )
            form = get_form(DateFormType.YearMonthDay, validators)

        self.assertIsNone(form().data)

    def test_month_year_date_form_empty_data(self):
        schema = load_schema_from_name('test_dates')
        error_messages = schema.error_messages

        with self.app_request_context('/'):
            validators = get_date_form_validators(
                DateFormType.YearMonth,
                schema.get_answers_by_answer_id('month-year-answer')[0],
                None,
                None,
                error_messages=error_messages,
            )
            form = get_form(DateFormType.YearMonth, validators)

        self.assertIsNone(form().data)

    def test_year_date_form_empty_data(self):
        schema = load_schema_from_name('test_dates')
        error_messages = schema.error_messages

        validators = get_date_form_validators(
            DateFormType.Year,
            schema.get_answers_by_answer_id('year-date-answer')[0],
            None,
            None,
            error_messages=error_messages,
        )
        form = get_form(DateFormType.Year, validators)

        self.assertIsNone(form().data)

    def test_date_form_format_data(self):
        schema = load_schema_from_name('test_dates')
        error_messages = schema.error_messages

        data = {'field': '2000-01-01'}

        with self.app_request_context('/'):

            class TestForm(Form):
                field = DateField(
                    DateFormType.YearMonthDay,
                    None,
                    None,
                    schema.get_answers_by_answer_id('single-date-answer')[0],
                    error_messages,
                )

            test_form = TestForm(data=data)

        self.assertEqual(test_form.field.data, '2000-01-01')

    def test_month_year_date_form_format_data(self):
        schema = load_schema_from_name('test_dates')
        error_messages = schema.error_messages

        data = {'field': '2000-01'}

        with self.app_request_context('/'):

            class TestForm(Form):
                field = DateField(
                    DateFormType.YearMonth,
                    None,
                    None,
                    schema.get_answers_by_answer_id('month-year-answer')[0],
                    error_messages,
                )

            test_form = TestForm(data=data)

        self.assertEqual(test_form.field.data, '2000-01')

    def test_year_date_form_format_data(self):
        schema = load_schema_from_name('test_dates')
        error_messages = schema.error_messages

        data = {'field': '2000'}

        class TestForm(Form):
            field = DateField(
                DateFormType.Year,
                None,
                None,
                schema.get_answers_by_answer_id('year-date-answer')[0],
                error_messages,
            )

        test_form = TestForm(data=data)

        self.assertEqual(test_form.field.data, '2000')

    def test_generate_date_form_validates_single_date_period(self):
        schema = load_schema_from_name('test_date_validation_single')
        error_messages = schema.error_messages
        test_metadata = {'ref_p_start_date': '2017-02-20'}

        answer = schema.get_answers_by_answer_id('date-range-from')[0]

        minimum_date, maximum_date = get_date_limits(
            answer, AnswerStore(), test_metadata
        )

        with self.app_request_context('/'):
            validators = get_date_form_validators(
                DateFormType.YearMonthDay,
                answer,
                minimum_date,
                maximum_date,
                error_messages=error_messages,
            )
            form = get_form(DateFormType.YearMonthDay, validators)

        self.assertTrue(hasattr(form, 'day'))
        self.assertTrue(hasattr(form, 'month'))
        self.assertTrue(hasattr(form, 'year'))

    def test_generate_date_form_validates_single_date_period_with_bespoke_message(self):
        schema = load_schema_from_name('test_date_validation_single')
        error_messages = schema.error_messages
        answer = {
            'id': 'date-range-from',
            'mandatory': True,
            'label': 'Period from',
            'type': 'Date',
            'maximum': {'value': '2017-06-11', 'offset_by': {'days': 20}},
            'validation': {'messages': {'SINGLE_DATE_PERIOD_TOO_LATE': 'Test Message'}},
        }

        with patch(
            'app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_answers_by_answer_id',
            return_value=[answer],
        ), self.app_request_context('/'):
            minimum_date, maximum_date = get_date_limits(answer, AnswerStore(), {})
            validators = get_date_form_validators(
                DateFormType.YearMonthDay,
                answer,
                minimum_date,
                maximum_date,
                error_messages=error_messages,
            )
            form = get_form(DateFormType.YearMonthDay, validators)

            self.assertTrue(hasattr(form, 'day'))
            self.assertTrue(hasattr(form, 'month'))
            self.assertTrue(hasattr(form, 'year'))

    def test_get_referenced_offset_value_for_value(self):
        answer_minimum = {'value': '2017-06-11'}

        minimum_date = get_referenced_date(answer_minimum, AnswerStore(), {})
        minimum_date = transform_date_by_offset(minimum_date, {'days': 10})

        self.assertEqual(minimum_date, convert_to_datetime('2017-06-21'))

    def test_get_referenced_offset_value_for_now_value(self):
        answer_minimum = {'value': 'now'}

        value = get_referenced_date(answer_minimum, AnswerStore(), {})
        value = transform_date_by_offset(value, {'days': 10})

        self.assertEqual(
            datetime.date(value), (datetime.now().date() + relativedelta(days=10))
        )

    def test_get_referenced_offset_value_for_meta(self):
        test_metadata = {'date': '2018-02-20'}
        answer_minimum = {'meta': 'date'}

        minimum_date = get_referenced_date(answer_minimum, AnswerStore(), test_metadata)
        minimum_date = transform_date_by_offset(minimum_date, {'days': -10})

        self.assertEqual(minimum_date, convert_to_datetime('2018-02-10'))

    # pylint: disable=unused-argument
    @patch(
        'app.forms.date_form.load_schema_from_metadata',
        return_value=QuestionnaireSchema({}),
    )
    def test_get_referenced_offset_value_for_answer_id(self, schema_mock):
        store = AnswerStore()

        test_answer_id = Answer(answer_id='date', value='2018-03-20')
        store.add_or_update(test_answer_id)

        answer_maximum = {'answer_id': 'date'}

        value = get_referenced_date(answer_maximum, store, {})
        value = transform_date_by_offset(value, {'months': 1})

        self.assertEqual(value, convert_to_datetime('2018-04-20'))

    def test_get_referenced_offset_value_with_no_offset(self):
        answer_minimum = {'value': '2017-06-11'}

        value = get_referenced_date(answer_minimum, AnswerStore(), {})
        value = transform_date_by_offset(value, {})

        self.assertEqual(value, convert_to_datetime('2017-06-11'))

    # pylint: disable=unused-argument
    @patch(
        'app.forms.date_form.load_schema_from_metadata',
        return_value=QuestionnaireSchema({}),
    )
    def test_minimum_and_maximum_offset_dates(self, mock1):
        test_metadata = {'date': '2018-02-20'}
        store = AnswerStore()

        test_answer_id = Answer(answer_id='date', value='2018-03-20')
        store.add_or_update(test_answer_id)

        answer = {
            'id': 'date_answer',
            'type': 'Date',
            'minimum': {'meta': 'date', 'offset_by': {'days': -10}},
            'maximum': {'answer_id': 'date', 'offset_by': {'years': 1}},
        }

        offset_dates = get_date_limits(answer, store, metadata=test_metadata)

        self.assertEqual(
            offset_dates,
            (convert_to_datetime('2018-02-10'), convert_to_datetime('2019-03-20')),
        )

    def test_greater_minimum_date_than_maximum_date(self):
        answer = {
            'id': 'date_answer',
            'type': 'Date',
            'minimum': {'value': '2018-02-15', 'offset_by': {'days': -10}},
            'maximum': {'value': '2018-01-15', 'offset_by': {'days': 10}},
        }

        with self.assertRaises(Exception) as ite:
            get_date_limits(answer, AnswerStore(), {})
            self.assertEqual(
                'The minimum offset date is greater than the maximum offset date for date-answer.',
                str(ite.exception),
            )

    def test_validate_mandatory_date(self):
        schema = load_schema_from_name('test_date_validation_single')
        error_messages = schema.error_messages
        answer = {
            'id': 'date-range-from',
            'mandatory': True,
            'label': 'Period from',
            'type': 'Date',
            'maximum': {'value': '2017-06-11', 'offset_by': {'days': 20}},
            'validation': {
                'messages': {'MANDATORY_DATE': 'Test Mandatory Date Message'}
            },
        }
        validator = validate_mandatory_date(error_messages, answer)
        self.assertEqual(validator[0].message, 'Test Mandatory Date Message')
