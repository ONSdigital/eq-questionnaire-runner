import pytest

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.forms.field_handlers.select_handlers import Choice, ChoiceWithDetailAnswer
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.value_source_resolver import ValueSourceResolver


def get_mock_schema():
    return QuestionnaireSchema(
        {
            "questionnaire_flow": {
                "type": "Linear",
                "options": {"summary": {"collapsible": False}},
            }
        }
    )


def get_mock_answer_store():
    return AnswerStore()


def get_mock_list_store():
    return ListStore()


def get_mock_metadata():
    return {}


def get_mock_response_metadata():
    return {"started_at": "2021-01-01T09:00:00.220038+00:00"}


def get_mock_location():
    return None


def get_mock_list_item_id():
    return None


def escape_answer_values():
    return False


@pytest.fixture
def rule_evaluator():
    evaluator = RuleEvaluator(
        answer_store=get_mock_answer_store(),
        list_store=get_mock_list_store(),
        metadata=get_mock_metadata(),
        response_metadata=get_mock_response_metadata(),
        schema=get_mock_schema(),
        location=get_mock_location(),
    )

    return evaluator


@pytest.fixture
def value_source_resolver():
    resolver = ValueSourceResolver(
        answer_store=get_mock_answer_store(),
        list_store=get_mock_list_store(),
        metadata=get_mock_metadata(),
        response_metadata=get_mock_response_metadata(),
        schema=get_mock_schema(),
        location=get_mock_location(),
        list_item_id=get_mock_list_item_id(),
        escape_answer_values=escape_answer_values(),
    )

    return resolver


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


def static_and_dynamic_answer_options_schema():
    return {**dynamic_answer_options_schema(), **static_answer_options_schema()}


def static_and_dynamic_answer_options_choices():
    return dynamic_answer_options_choices() + static_answer_options_choices()


def to_choices_with_detail_answer_id(choices):
    return [
        ChoiceWithDetailAnswer(choice.value, choice.label, None) for choice in choices
    ]
