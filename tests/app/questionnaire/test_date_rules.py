from datetime import datetime, timezone
import pytest

from app.data_models.answer_store import Answer, AnswerStore
from app.data_models.list_store import ListStore
from app.questionnaire.when_rules import evaluate_date_rule, evaluate_goto


@pytest.mark.parametrize(
    "date,condition,comparison,expected",
    (
        (
            datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
            "equals",
            {"value": "now"},
            True,
        ),
        ("2000-01-01", "equals", {"value": "now"}, False),
        (
            "2020-05-01",
            "equals",
            {
                "value": "2019-03-31",
                "offset_by": {"days": 1, "months": 1, "years": 1},
            },
            True,
        ),
        (
            "2020-02-29",
            "equals",
            {
                "value": "2021-04-01",
                "offset_by": {"days": -1, "months": -1, "years": -1},
            },
            True,
        ),
        (
            "2018-02",
            "not equals",
            {"value": "2018-01"},
            True,
        ),
        (
            "2018-01",
            "not equals",
            {"value": "2018-01"},
            False,
        ),
        (
            "2018-01",
            "not equals",
            {"value": "2018-01"},
            False,
        ),
        (
            "2016-06-11",
            "less than",
            {"meta": "return_by"},
            True,
        ),
        (
            "2016-06-12",
            "less than",
            {"meta": "return_by"},
            False,
        ),
        (
            "2018-02-04",
            "greater than",
            {"id": "compare_date_answer"},
            True,
        ),
        (
            "2018-02-03",
            "greater than",
            {"id": "compare_date_answer"},
            False,
        ),
        (
            "2018-02-03",
            "greater than",
            {"id": "non_existent_answer"},
            False,
        ),
    ),
)
def test_evaluate_date_rule_equals_with_value(
    date, condition, comparison, expected, questionnaire_schema
):
    when = {
        "id": "date-answer",
        "condition": condition,
        "date_comparison": comparison,
    }
    metadata = {"return_by": "2016-06-12"}
    answer_store = AnswerStore({})
    answer_store.add_or_update(
        Answer(answer_id="compare_date_answer", value="2018-02-03")
    )

    assert (
        evaluate_date_rule(when, answer_store, questionnaire_schema, metadata, date)
        is expected
    )


def test_do_not_go_to_next_question_for_date_answer(
    current_location, questionnaire_schema
):
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

    assert not evaluate_goto(
        goto_rule=goto_rule,
        schema=questionnaire_schema,
        metadata={},
        answer_store=answer_store,
        list_store=ListStore(),
        current_location=current_location,
    )
