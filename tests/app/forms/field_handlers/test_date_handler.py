# pylint: disable=unused-argument
from datetime import datetime, timezone

import pytest
from dateutil.relativedelta import relativedelta
from mock import patch
from wtforms import Form

from app.data_models.answer import Answer
from app.data_models.answer_store import AnswerStore
from app.forms import error_messages
from app.forms.field_handlers import DateHandler
from app.forms.fields import date_field
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.rules.utils import parse_datetime
from app.utilities.schema import load_schema_from_name


def test_date_field_created_with_guidance(value_source_resolver, rule_evaluator):
    date_json = {
        "guidance": "Please enter a date",
        "id": "period-to",
        "label": "Period to",
        "mandatory": True,
        "type": "Date",
        "validation": {
            "messages": {
                "INVALID_DATE": "The date entered is not valid.  Please correct your answer.",
                "MANDATORY_DATE": "Please provide an answer to continue.",
            }
        },
    }

    handler = DateHandler(
        date_json, value_source_resolver, rule_evaluator, error_messages
    )

    class TestForm(Form):
        test_field = handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, date_field.DateField)
    assert form.test_field.label.text == date_json["label"]
    assert form.test_field.description == date_json["guidance"]


def test_generate_date_form_validates_single_date_period(
    app, value_source_resolver, rule_evaluator
):
    schema = load_schema_from_name("test_date_validation_single")
    value_source_resolver.schema = schema
    value_source_resolver.metadata = {"ref_p_start_date": "2017-02-20"}

    handler = DateHandler(
        schema.get_answers_by_answer_id("date-range-from")[0],
        value_source_resolver,
        rule_evaluator,
        error_messages,
    )
    form = date_field.get_form_class(handler.validators)

    assert hasattr(form, "day")
    assert hasattr(form, "month")
    assert hasattr(form, "year")


def test_generate_date_form_validates_single_date_period_with_bespoke_message(
    app, value_source_resolver, rule_evaluator
):
    value_source_resolver.schema = load_schema_from_name("test_date_validation_single")
    answer = {
        "id": "date-range-from",
        "mandatory": True,
        "label": "Period from",
        "type": "Date",
        "maximum": {"value": "2017-06-11", "offset_by": {"days": 20}},
        "validation": {"messages": {"SINGLE_DATE_PERIOD_TOO_LATE": "Test Message"}},
    }
    handler = DateHandler(answer, value_source_resolver, rule_evaluator, error_messages)
    form = date_field.get_form_class(handler.validators)

    assert hasattr(form, "day")
    assert hasattr(form, "month")
    assert hasattr(form, "year")


def test_get_referenced_offset_value_for_value(
    app, value_source_resolver, rule_evaluator
):
    answer = {"minimum": {"value": "2017-06-11"}}

    handler = DateHandler(answer, value_source_resolver, rule_evaluator, error_messages)
    minimum_date = handler.get_date_value("minimum")
    minimum_date = handler.transform_date_by_offset(minimum_date, {"days": 10})

    assert minimum_date == parse_datetime("2017-06-21")


def test_get_referenced_offset_value_for_now_value(
    app, value_source_resolver, rule_evaluator
):
    answer = {"minimum": {"value": "now"}}

    handler = DateHandler(answer, value_source_resolver, rule_evaluator, error_messages)
    minimum_date = handler.get_date_value("minimum")
    minimum_date = handler.transform_date_by_offset(minimum_date, {"days": 10})

    assert datetime.date(minimum_date) == (
        datetime.now(tz=timezone.utc).date() + relativedelta(days=10)
    )


def test_get_referenced_offset_value_for_meta(
    app, value_source_resolver, rule_evaluator
):
    value_source_resolver.metadata = {"date": "2018-02-20"}
    answer = {"minimum": {"value": {"identifier": "date", "source": "metadata"}}}

    handler = DateHandler(answer, value_source_resolver, rule_evaluator, error_messages)
    minimum_date = handler.get_date_value("minimum")
    minimum_date = handler.transform_date_by_offset(minimum_date, {"days": -10})

    assert minimum_date == parse_datetime("2018-02-10")


@patch(
    "app.utilities.schema.load_schema_from_name", return_value=QuestionnaireSchema({})
)
def test_get_referenced_offset_value_for_answer_id(
    app, value_source_resolver, rule_evaluator
):
    answer_store = AnswerStore()

    test_answer_id = Answer(answer_id="date", value="2018-03-20")
    answer_store.add_or_update(test_answer_id)
    value_source_resolver.answer_store = answer_store
    answer = {"maximum": {"value": {"identifier": "date", "source": "answers"}}}

    handler = DateHandler(answer, value_source_resolver, rule_evaluator, error_messages)
    maximum_date = handler.get_date_value("maximum")
    maximum_date = handler.transform_date_by_offset(maximum_date, {"months": 1})

    assert maximum_date == parse_datetime("2018-04-20")


@patch(
    "app.questionnaire.questionnaire_schema.QuestionnaireSchema.is_repeating_answer",
    return_value=True,
)
def test_get_referenced_offset_value_with_list_item_id(
    app, value_source_resolver, rule_evaluator
):
    list_item_id = "abcde"

    test_answer_id = Answer(
        answer_id="date", value="2018-03-20", list_item_id=list_item_id
    )

    location = Location(section_id="test", list_item_id=list_item_id)

    answer_store = AnswerStore()

    answer_store.add_or_update(test_answer_id)
    value_source_resolver.answer_store = answer_store
    value_source_resolver.location = location
    value_source_resolver.list_item_id = list_item_id
    answer = {
        "maximum": {
            "value": {"identifier": "date", "source": "answers"},
            "offset_by": {"months": 1},
        }
    }

    handler = DateHandler(answer, value_source_resolver, rule_evaluator, error_messages)
    maximum_date = handler.get_date_value("maximum")

    assert maximum_date == parse_datetime("2018-04-20")


def test_get_referenced_offset_value_with_no_offset(
    app, value_source_resolver, rule_evaluator
):
    answer = {"minimum": {"value": "2017-06-11"}}

    handler = DateHandler(answer, value_source_resolver, rule_evaluator, error_messages)
    minimum_date = handler.get_date_value("minimum")
    minimum_date = handler.transform_date_by_offset(minimum_date, {})

    assert minimum_date == parse_datetime("2017-06-11")


@patch(
    "app.utilities.schema.load_schema_from_name", return_value=QuestionnaireSchema({})
)
def test_minimum_and_maximum_offset_dates(app, value_source_resolver, rule_evaluator):
    value_source_resolver.metadata = {"date": "2018-02-20"}
    answer_store = AnswerStore()

    test_answer_id = Answer(answer_id="date", value="2018-03-20")
    answer_store.add_or_update(test_answer_id)
    value_source_resolver.answer_store = answer_store
    answer = {
        "id": "date_answer",
        "type": "Date",
        "minimum": {
            "value": {"identifier": "date", "source": "metadata"},
            "offset_by": {"days": -10},
        },
        "maximum": {
            "value": {"identifier": "date", "source": "answers"},
            "offset_by": {"years": 1},
        },
    }

    handler = DateHandler(answer, value_source_resolver, rule_evaluator, error_messages)
    minimum_date = handler.get_date_value("minimum")
    maximum_date = handler.get_date_value("maximum")

    assert minimum_date == parse_datetime("2018-02-10")
    assert maximum_date == parse_datetime("2019-03-20")


def test_greater_minimum_date_than_maximum_date(
    app, value_source_resolver, rule_evaluator
):
    answer = {
        "id": "date_answer",
        "type": "Date",
        "minimum": {"value": "2018-02-15", "offset_by": {"days": -10}},
        "maximum": {"value": "2018-01-15", "offset_by": {"days": 10}},
    }

    handler = DateHandler(answer, value_source_resolver, rule_evaluator, error_messages)

    with pytest.raises(Exception) as ite:
        handler.get_date_value("minimum")

        assert (
            str(ite.exception)
            == "The minimum offset date is greater than the maximum offset date for date-answer."
        )


def test_validate_mandatory_date(app, value_source_resolver, rule_evaluator):
    answer = {
        "id": "date-range-from",
        "mandatory": True,
        "label": "Period from",
        "type": "Date",
        "maximum": {"value": "2017-06-11", "offset_by": {"days": 20}},
        "validation": {"messages": {"MANDATORY_DATE": "Test Mandatory Date Message"}},
    }

    handler = DateHandler(answer, value_source_resolver, rule_evaluator, error_messages)
    validator = handler.get_mandatory_validator()

    assert validator.message == "Test Mandatory Date Message"
