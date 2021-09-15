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
    value_source_resolver = ValueSourceResolver(
        answer_store=AnswerStore(),
        list_store=ListStore(),
        metadata={},
        schema=schema,
        location=None,
        list_item_id=None,
        escape_answer_values=False,
    )

    return value_source_resolver
