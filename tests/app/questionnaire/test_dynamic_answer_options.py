# pylint: disable=redefined-outer-name
import pytest

from app.data_models.answer_store import Answer
from app.data_models.data_stores import DataStores
from app.questionnaire.dynamic_answer_options import DynamicAnswerOptions
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.value_source_resolver import ValueSourceResolver


@pytest.fixture
def rule_evaluator(mock_schema, response_metadata):
    evaluator = RuleEvaluator(
        data_stores=DataStores(response_metadata=response_metadata),
        schema=mock_schema,
        location=None,
    )

    return evaluator


@pytest.fixture
def value_source_resolver(mock_schema, response_metadata):
    evaluator = RuleEvaluator(
        data_stores=DataStores(response_metadata=response_metadata),
        schema=mock_schema,
        location=None,
    )
    resolver = ValueSourceResolver(
        data_stores=DataStores(response_metadata=response_metadata),
        schema=mock_schema,
        location=None,
        list_item_id=None,
        routing_path_block_ids=None,
        use_default_answer=True,
    )

    return resolver


def test_dynamic_answer_options(rule_evaluator, value_source_resolver):
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
        value_source_resolver=value_source_resolver,
    )

    expected_output = (
        {"label": "Monday 28 December 2020", "value": "2020-12-28"},
        {"label": "Tuesday 29 December 2020", "value": "2020-12-29"},
        {"label": "Wednesday 30 December 2020", "value": "2020-12-30"},
    )

    assert dynamic_options.evaluate() == expected_output


@pytest.mark.parametrize(
    "checkbox_answer, expected_output",
    [
        (
            ["Body"],
            ({"label": "Body-label", "value": "Body"},),
        ),
        (
            ["Head", "Body"],
            (
                {"label": "Head-label", "value": "Head"},
                {"label": "Body-label", "value": "Body"},
            ),
        ),
        (None, ()),
    ],
)
def test_dynamic_answer_options_answer_source(
    rule_evaluator,
    value_source_resolver,
    mock_schema,
    mocker,
    checkbox_answer,
    expected_output,
):
    answer_schema = [
        {
            "id": "injury-sustained-answer",
            "mandatory": True,
            "options": [
                {"label": "Head-label", "value": "Head"},
                {"label": "Body-label", "value": "Body"},
            ],
            "type": "Checkbox",
        }
    ]

    mock_schema.get_answers_by_answer_id = mocker.Mock(return_value=answer_schema)
    mock_schema.get_default_answer = mocker.Mock(return_value=None)
    mock_schema.is_answer_dynamic = mocker.Mock(return_value=False)
    mock_schema.is_answer_in_list_collector_repeating_block = mocker.Mock(
        return_value=False
    )

    if checkbox_answer:
        value_source_resolver.data_stores.answer_store.add_or_update(
            Answer(answer_id="injury-sustained-answer", value=checkbox_answer)
        )

    dynamic_options = DynamicAnswerOptions(
        {
            "values": {"source": "answers", "identifier": "injury-sustained-answer"},
            "transform": {
                "option-label-from-value": ["self", "injury-sustained-answer"]
            },
        },
        rule_evaluator=rule_evaluator,
        value_source_resolver=value_source_resolver,
    )

    assert dynamic_options.evaluate() == expected_output
