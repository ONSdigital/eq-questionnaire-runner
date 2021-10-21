import pytest

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.value_source_resolver import ValueSourceResolver


@pytest.fixture
def value_source_resolver():
    schema = QuestionnaireSchema(
        {
            "questionnaire_flow": {
                "type": "Linear",
                "options": {"summary": {"collapsible": False}},
            }
        }
    )
    resolver = ValueSourceResolver(
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata={},
        response_metadata={},
        schema=schema,
        location=None,
        list_item_id=None,
        escape_answer_values=False,
    )

    return resolver


@pytest.fixture
def dropdown_answer_schema():
    return {
        "type": "Dropdown",
        "id": "dropdown-with-label-answer",
        "mandatory": False,
        "label": "Please choose an option",
        "description": "This is an optional dropdown",
        "options": [
            {"label": "Liverpool", "value": "Liverpool"},
            {"label": "Chelsea", "value": "Chelsea"},
            {"label": "Rugby is better!", "value": "Rugby is better!"},
        ],
    }
