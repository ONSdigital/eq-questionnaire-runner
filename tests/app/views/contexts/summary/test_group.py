import pytest

from app.questionnaire.location import Location
from app.views.contexts.summary.group import Group
from app.data_model.answer_store import AnswerStore
from app.data_model.list_store import ListStore


@pytest.fixture(name="schema")
def fixture_schema():
    return {
        "blocks": [
            {
                "type": "Question",
                "id": "number-question-one",
                "question": {
                    "answers": [
                        {
                            "id": "answer-one",
                            "mandatory": False,
                            "type": "Number",
                            "label": "Leave blank",
                            "default": 0,
                        }
                    ],
                    "id": "question",
                    "title": "Don't enter an answer. A default value will be used",
                    "type": "General",
                },
            },
            {
                "type": "Question",
                "id": "number-question-two",
                "question": {
                    "answers": [
                        {
                            "id": "answer-two",
                            "mandatory": False,
                            "type": "Number",
                            "label": "Enter a Value",
                        }
                    ],
                    "id": "question2",
                    "title": "Enter an answer. It will be shown on the summary page",
                    "type": "General",
                },
            },
            {"type": "Summary", "id": "summary"},
        ],
        "id": "group",
        "title": "group-test",
    }


@pytest.fixture(name="path")
def fixture_path():
    return ["number-question-one", "number-question-two"]
