from datetime import datetime, timezone

from app.data_models.answer_store import Answer, AnswerStore
from app.data_models.list_store import ListStore
from app.questionnaire.location import Location
from app.questionnaire.when_rules import evaluate_date_rule, evaluate_goto


def test_evaluate_date_rule_equals_with_value_now(questionnaire_schema):
    when = {
        "id": "date-answer",
        "condition": "equals",
        "date_comparison": {"value": "now"},
    }

    answer_value = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    result = evaluate_date_rule(when, None, questionnaire_schema, None, answer_value)
    assert result

    answer_value = "2000-01-01"
    result = evaluate_date_rule(when, None, questionnaire_schema, None, answer_value)
    assert not result


def test_evaluate_date_rule_equals_with_with_offset(questionnaire_schema):
    when = {
        "id": "date-answer",
        "condition": "equals",
        "date_comparison": {
            "value": "2019-03-31",
            "offset_by": {"days": 1, "months": 1, "years": 1},
        },
    }

    answer_value = "2020-05-01"
    result = evaluate_date_rule(when, None, questionnaire_schema, None, answer_value)
    assert result

    when = {
        "id": "date-answer",
        "condition": "equals",
        "date_comparison": {
            "value": "2021-04-01",
            "offset_by": {"days": -1, "months": -1, "years": -1},
        },
    }

    answer_value = "2020-02-29"
    result = evaluate_date_rule(when, None, questionnaire_schema, None, answer_value)
    assert result


def test_evaluate_date_rule_not_equals_with_value_year_month(questionnaire_schema):
    when = {
        "id": "date-answer",
        "condition": "not equals",
        "date_comparison": {"value": "2018-01"},
    }

    answer_value = "2018-02"
    result = evaluate_date_rule(when, None, questionnaire_schema, None, answer_value)
    assert result

    answer_value = "2018-01"
    result = evaluate_date_rule(when, None, questionnaire_schema, None, answer_value)
    assert not result


def test_evaluate_date_rule_less_than_meta(questionnaire_schema):
    metadata = {"return_by": "2016-06-12"}
    when = {
        "id": "date-answer",
        "condition": "less than",
        "date_comparison": {"meta": "return_by"},
    }

    answer_value = "2016-06-11"
    result = evaluate_date_rule(
        when, None, questionnaire_schema, metadata, answer_value
    )
    assert result

    answer_value = "2016-06-12"
    result = evaluate_date_rule(
        when, None, questionnaire_schema, metadata, answer_value
    )
    assert not result


def test_evaluate_date_rule_greater_than_with_id(questionnaire_schema):
    when = {
        "id": "date-answer",
        "condition": "greater than",
        "date_comparison": {"id": "compare_date_answer"},
    }

    answer_store = AnswerStore({})
    answer_store.add_or_update(
        Answer(answer_id="compare_date_answer", value="2018-02-03")
    )

    answer_value = "2018-02-04"
    result = evaluate_date_rule(
        when, answer_store, questionnaire_schema, None, answer_value
    )
    assert result

    answer_value = "2018-02-03"
    result = evaluate_date_rule(
        when, answer_store, questionnaire_schema, None, answer_value
    )
    assert not result


def test_evaluate_date_rule_invalid(questionnaire_schema):
    when = {
        "id": "date-answer",
        "condition": "greater than",
        "date_comparison": {"id": "compare_date_answer"},
    }
    answer_store = AnswerStore({})
    result = evaluate_date_rule(when, answer_store, questionnaire_schema, None, None)

    assert not result


def test_do_not_go_to_next_question_for_date_answer(questionnaire_schema):
    goto_rule = {
        "id": "next-question",
        "when": [
            {
                "id": "date-answer",
                "condition": "equals",
                "date_comparison": {"value": "2018-01"},
            }
        ],
    }

    answer_store = AnswerStore({})
    answer_store.add_or_update(Answer(answer_id="date-answer", value="2018-02-01"))

    current_location = Location(section_id="some-section", block_id="some-block")

    assert not evaluate_goto(
        goto_rule=goto_rule,
        schema=questionnaire_schema,
        metadata={},
        answer_store=answer_store,
        list_store=ListStore(),
        current_location=current_location,
    )
