import pytest

from app.data_models.data_stores import DataStores
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.value_source_resolver import ValueSourceResolver
from app.utilities.types import Choice, ChoiceWithDetailAnswer


def get_mock_schema():
    return QuestionnaireSchema(
        {
            "questionnaire_flow": {
                "type": "Linear",
                "options": {"summary": {"collapsible": False}},
            }
        }
    )


def get_mock_response_metadata():
    return {"started_at": "2021-01-01T09:00:00.220038+00:00"}


@pytest.fixture
def value_source_resolver():
    resolver = ValueSourceResolver(
        data_stores=DataStores(response_metadata=get_mock_response_metadata()),
        schema=get_mock_schema(),
        location=None,
        list_item_id=None,
        escape_answer_values=False,
        use_default_answer=True,
    )
    return resolver


@pytest.fixture
def rule_evaluator(value_source_resolver):  # pylint: disable=redefined-outer-name
    evaluator = RuleEvaluator(
        value_source_resolver=value_source_resolver,
        data_stores=DataStores(response_metadata=get_mock_response_metadata()),
        schema=get_mock_schema(),
        location=None,
    )

    return evaluator


def static_answer_options_schema():
    return {
        "options": [
            {"label": "Liverpool", "value": "Liverpool"},
            {"label": "Chelsea", "value": "Chelsea"},
            {"label": "Rugby is better!", "value": "Rugby is better!"},
        ]
    }


def static_answer_options_choices():
    return [
        Choice(option["label"], option["value"])
        for option in static_answer_options_schema()["options"]
    ]


def dynamic_answer_options_schema():
    return {
        "dynamic_options": {
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
    }


def dynamic_answer_options_choices():
    return [
        Choice("2020-12-28", "Monday 28 December 2020"),
        Choice("2020-12-29", "Tuesday 29 December 2020"),
        Choice("2020-12-30", "Wednesday 30 December 2020"),
    ]


def dynamic_radio_options_no_static_options():
    return {
        "id": "dynamic-radio",
        "mandatory": False,
        "type": "Radio",
        "dynamic_options": {
            "values": {"source": "answers", "identifier": "checkbox-answer"},
            "transform": {"option-label-from-value": ["self", "checkbox-answer"]},
        },
    }


def static_and_dynamic_answer_options_schema():
    return {**dynamic_answer_options_schema(), **static_answer_options_schema()}


def static_and_dynamic_answer_options_choices():
    return dynamic_answer_options_choices() + static_answer_options_choices()


def to_choices_with_detail_answer_id(choices):
    return [
        ChoiceWithDetailAnswer(choice.value, choice.label, None) for choice in choices
    ]
