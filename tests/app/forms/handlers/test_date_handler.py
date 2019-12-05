# pylint: disable=unused-argument
from datetime import datetime
from mock import patch

import pytest
from dateutil.relativedelta import relativedelta
from wtforms import Form

from app.data_model.answer import Answer
from app.data_model.answer_store import AnswerStore
from app.forms.date_form import DateFormType, get_form
from app.forms.handlers.date_handler import DateHandler
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.rules import convert_to_datetime
from app.utilities.schema import load_schema_from_name


def test_generate_date_form_creates_empty_form(app):
    schema = load_schema_from_name('test_dates')
    handler = DateHandler(
        schema.get_answers_by_answer_id('single-date-answer')[0], schema.error_messages
    )
    form = get_form(DateFormType.YearMonthDay, handler.validators)

    assert hasattr(form, 'day')
    assert hasattr(form, 'month')
    assert hasattr(form, 'year')


def test_generate_month_year_date_form_creates_empty_form(app):
    schema = load_schema_from_name('test_dates')
    handler = DateHandler(
        schema.get_answers_by_answer_id('month-year-answer')[0], schema.error_messages
    )
    form = get_form(DateFormType.YearMonth, handler.validators)

    assert not hasattr(form, 'day')
    assert hasattr(form, 'month')
    assert hasattr(form, 'year')


def test_generate_year_date_form_creates_empty_form(app):
    schema = load_schema_from_name('test_dates')
    error_messages = schema.error_messages
    handler = DateHandler(
        schema.get_answers_by_answer_id('year-date-answer')[0], error_messages
    )
    form = get_form(DateFormType.Year, handler.validators)

    assert not hasattr(form, 'day')
    assert not hasattr(form, 'month')
    assert hasattr(form, 'year')


def test_date_form_empty_data(app):
    schema = load_schema_from_name('test_dates')
    error_messages = schema.error_messages

    handler = DateHandler(
        schema.get_answers_by_answer_id('single-date-answer')[0], error_messages
    )
    form = get_form(DateFormType.YearMonthDay, handler.validators)

    assert form().data is None


def test_month_year_date_form_empty_data(app):
    schema = load_schema_from_name('test_dates')
    error_messages = schema.error_messages

    handler = DateHandler(
        schema.get_answers_by_answer_id('month-year-answer')[0], error_messages
    )
    form = get_form(DateFormType.YearMonth, handler.validators)

    assert form().data is None


def test_year_date_form_empty_data(app):
    schema = load_schema_from_name('test_dates')
    error_messages = schema.error_messages

    handler = DateHandler(
        schema.get_answers_by_answer_id('year-date-answer')[0], error_messages
    )
    form = get_form(DateFormType.Year, handler.validators)

    assert form().data is None


def test_date_form_format_data(app):
    schema = load_schema_from_name('test_dates')
    error_messages = schema.error_messages

    data = {'field': '2000-01-01'}

    handler = DateHandler(
        schema.get_answers_by_answer_id('single-date-answer')[0], error_messages
    )

    class TestForm(Form):
        field = handler.get_field()

    test_form = TestForm(data=data)

    assert test_form.field.data == '2000-01-01'


def test_month_year_date_form_format_data(app):
    schema = load_schema_from_name('test_dates')
    error_messages = schema.error_messages

    data = {'field': '2000-01'}

    handler = DateHandler(
        schema.get_answers_by_answer_id('month-year-answer')[0], error_messages
    )

    class TestForm(Form):
        field = handler.get_field()

    test_form = TestForm(data=data)

    assert test_form.field.data == '2000-01'


def test_year_date_form_format_data(app):
    schema = load_schema_from_name('test_dates')
    error_messages = schema.error_messages

    data = {'field': '2000'}

    handler = DateHandler(
        schema.get_answers_by_answer_id('year-date-answer')[0], error_messages
    )

    class TestForm(Form):
        field = handler.get_field()

    test_form = TestForm(data=data)

    assert test_form.field.data == '2000'


def test_generate_date_form_validates_single_date_period(app):
    schema = load_schema_from_name('test_date_validation_single')
    test_metadata = {'ref_p_start_date': '2017-02-20'}
    handler = DateHandler(
        schema.get_answers_by_answer_id('date-range-from')[0],
        schema.error_messages,
        metadata=test_metadata,
    )
    form = get_form(DateFormType.YearMonthDay, handler.validators)

    assert hasattr(form, 'day')
    assert hasattr(form, 'month')
    assert hasattr(form, 'year')


def test_generate_date_form_validates_single_date_period_with_bespoke_message(app):
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
    handler = DateHandler(answer, error_messages)
    form = get_form(DateFormType.YearMonthDay, handler.validators)

    assert hasattr(form, 'day')
    assert hasattr(form, 'month')
    assert hasattr(form, 'year')


def test_get_referenced_offset_value_for_value(app):
    answer = {'minimum': {'value': '2017-06-11'}}

    handler = DateHandler(answer)
    minimum_date, _ = handler.get_date_limits()
    minimum_date = handler.transform_date_by_offset(minimum_date, {'days': 10})

    assert minimum_date == convert_to_datetime('2017-06-21')


def test_get_referenced_offset_value_for_now_value(app):
    answer = {'minimum': {'value': 'now'}}

    handler = DateHandler(answer)
    minimum_date, _ = handler.get_date_limits()
    minimum_date = handler.transform_date_by_offset(minimum_date, {'days': 10})

    assert datetime.date(minimum_date) == (
        datetime.now().date() + relativedelta(days=10)
    )


def test_get_referenced_offset_value_for_meta(app):
    test_metadata = {'date': '2018-02-20'}
    answer = {'minimum': {'meta': 'date'}}

    handler = DateHandler(answer, metadata=test_metadata)
    minimum_date, _ = handler.get_date_limits()
    minimum_date = handler.transform_date_by_offset(minimum_date, {'days': -10})

    assert minimum_date == convert_to_datetime('2018-02-10')


@patch(
    'app.utilities.schema.load_schema_from_name', return_value=QuestionnaireSchema({})
)
def test_get_referenced_offset_value_for_answer_id(app):
    answer_store = AnswerStore()

    test_answer_id = Answer(answer_id='date', value='2018-03-20')
    answer_store.add_or_update(test_answer_id)

    answer = {'maximum': {'answer_id': 'date'}}

    handler = DateHandler(answer, answer_store=answer_store)
    _, maximum_date = handler.get_date_limits()
    maximum_date = handler.transform_date_by_offset(maximum_date, {'months': 1})

    assert maximum_date == convert_to_datetime('2018-04-20')


# pylint: disable=unused-argument
@patch(
    'app.utilities.schema.load_schema_from_name', return_value=QuestionnaireSchema({})
)
@patch(
    'app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_list_item_id_for_answer_id',
    return_value='abcde',
)
def test_get_referenced_offset_value_with_list_item_id(app, schema_mock):
    list_item_id = 'abcde'
    answer_store = AnswerStore()

    test_answer_id = Answer(
        answer_id='date', value='2018-03-20', list_item_id=list_item_id
    )

    location = Location(section_id='test', list_item_id=list_item_id)

    answer_store.add_or_update(test_answer_id)

    answer = {'maximum': {'answer_id': 'date', 'offset_by': {'months': 1}}}

    handler = DateHandler(answer, answer_store=answer_store, location=location)
    _, maximum_date = handler.get_date_limits()

    assert maximum_date == convert_to_datetime('2018-04-20')


def test_get_referenced_offset_value_with_no_offset(app):
    answer = {'minimum': {'value': '2017-06-11'}}

    handler = DateHandler(answer)
    minimum_date, _ = handler.get_date_limits()
    minimum_date = handler.transform_date_by_offset(minimum_date, {})

    assert minimum_date == convert_to_datetime('2017-06-11')


@patch(
    'app.utilities.schema.load_schema_from_name', return_value=QuestionnaireSchema({})
)
def test_minimum_and_maximum_offset_dates(app):
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

    handler = DateHandler(answer, answer_store=store, metadata=test_metadata)
    offset_dates = handler.get_date_limits()

    assert offset_dates == (
        convert_to_datetime('2018-02-10'),
        convert_to_datetime('2019-03-20'),
    )


def test_greater_minimum_date_than_maximum_date(app):
    answer = {
        'id': 'date_answer',
        'type': 'Date',
        'minimum': {'value': '2018-02-15', 'offset_by': {'days': -10}},
        'maximum': {'value': '2018-01-15', 'offset_by': {'days': 10}},
    }

    handler = DateHandler(answer)

    with pytest.raises(Exception) as ite:
        handler.get_date_limits()

        assert (
            str(ite.exception)
            == 'The minimum offset date is greater than the maximum offset date for date-answer.'
        )


def test_validate_mandatory_date(app):
    schema = load_schema_from_name('test_date_validation_single')
    error_messages = schema.error_messages
    answer = {
        'id': 'date-range-from',
        'mandatory': True,
        'label': 'Period from',
        'type': 'Date',
        'maximum': {'value': '2017-06-11', 'offset_by': {'days': 20}},
        'validation': {'messages': {'MANDATORY_DATE': 'Test Mandatory Date Message'}},
    }

    handler = DateHandler(answer, error_messages)
    validator = handler.get_mandatory_validator('MANDATORY_DATE')

    assert validator[0].message == 'Test Mandatory Date Message'
