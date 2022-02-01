# pylint: disable=redefined-outer-name
import pytest

from app.data_models import AnswerStore, ListStore
from app.questionnaire.dynamic_answer_options import DynamicAnswerOptions
from app.questionnaire.rules.rule_evaluator import RuleEvaluator


@pytest.fixture
def rule_evaluator(mock_schema, response_metadata):
    evaluator = RuleEvaluator(
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata={},
        response_metadata=response_metadata,
        schema=mock_schema,
        location=None,
    )

    return evaluator


def test_dynamic_answer_options(rule_evaluator):
    dynamic_options = DynamicAnswerOptions(
        {
            "values": {
                "map": [
                    {"format-date": ["self", "yyyy-MM-dd"]},
                    {
                        "date-range": [
                            {
                                "date": [
                                    {
                                        "source": "response_metadata",
                                        "identifier": "started_at",
                                    },
                                    {"day_of_week": "MONDAY"},
                                ]
                            },
                            3,
                        ]
                    },
                ]
            },
            "transform": {"format-date": [{"date": ["self"]}, "EEEE d MMMM yyyy"]},
        },
        rule_evaluator=rule_evaluator,
    )

    expected_output = (
        {"label": "Monday 28 December 2020", "value": "2020-12-28"},
        {"label": "Tuesday 29 December 2020", "value": "2020-12-29"},
        {"label": "Wednesday 30 December 2020", "value": "2020-12-30"},
    )

    assert dynamic_options.evaluate() == expected_output
