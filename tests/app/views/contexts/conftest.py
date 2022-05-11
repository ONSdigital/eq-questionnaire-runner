import pytest
from mock import MagicMock

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress_store import ProgressStore
from app.data_models.session_data import SessionData
from app.forms.questionnaire_form import QuestionnaireForm
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.utilities.schema import load_schema_from_name


@pytest.fixture
def list_collector_block():
    return {
        "id": "list-collector",
        "type": "ListCollector",
        "for_list": "people",
        "add_block": {
            "id": "add-person",
            "type": "ListAddQuestion",
            "question": {
                "id": "add-question",
                "type": "General",
                "title": "What is the name of the person?",
                "answers": [
                    {
                        "id": "first-name",
                        "label": "First name",
                        "mandatory": True,
                        "type": "TextField",
                    },
                    {
                        "id": "last-name",
                        "label": "Last name",
                        "mandatory": True,
                        "type": "TextField",
                    },
                ],
            },
        },
        "edit_block": {
            "id": "edit-person",
            "type": "ListEditQuestion",
            "question": {
                "id": "edit-question",
                "type": "General",
                "title": "What is the name of the person?",
                "answers": [
                    {
                        "id": "first-name",
                        "label": "First name",
                        "mandatory": True,
                        "type": "TextField",
                    },
                    {
                        "id": "last-name",
                        "label": "Last name",
                        "mandatory": True,
                        "type": "TextField",
                    },
                ],
            },
        },
        "remove_block": {
            "id": "remove-person",
            "type": "ListRemoveQuestion",
            "question": {
                "id": "remove-question",
                "type": "General",
                "title": "Are you sure you want to remove this person?",
                "answers": [
                    {
                        "id": "remove-confirmation",
                        "mandatory": True,
                        "type": "Radio",
                        "options": [
                            {
                                "label": "Yes",
                                "value": "Yes",
                                "action": {"type": "RemoveListItemAndAnswers"},
                            },
                            {"label": "No", "value": "No"},
                        ],
                    }
                ],
            },
        },
        "summary": {
            "item_title": {
                "text": "{person_name}",
                "placeholders": [
                    {
                        "placeholder": "person_name",
                        "transforms": [
                            {
                                "arguments": {
                                    "delimiter": " ",
                                    "list_to_concatenate": [
                                        {
                                            "source": "answers",
                                            "identifier": "first-name",
                                        },
                                        {
                                            "source": "answers",
                                            "identifier": "last-name",
                                        },
                                    ],
                                },
                                "transform": "concatenate_list",
                            }
                        ],
                    }
                ],
            }
        },
        "question": {
            "id": "confirmation-question",
            "type": "General",
            "title": "Does anyone else live here?",
            "answers": [
                {
                    "id": "anyone-else",
                    "mandatory": True,
                    "type": "Radio",
                    "options": [
                        {
                            "label": "Yes",
                            "value": "Yes",
                            "action": {"type": "RedirectToListAddBlock"},
                        },
                        {"label": "No", "value": "No"},
                    ],
                }
            ],
        },
    }


@pytest.fixture
def form():
    mock_form = MagicMock(
        spec=QuestionnaireForm,
        data={"first-name": "Toni", "last-name": "Morrison"},
        errors={},
        question_errors={},
        fields={},
    )
    mock_form.answer_errors.return_value = ""
    return mock_form


@pytest.fixture
def schema():
    return MagicMock(
        QuestionnaireSchema({"questionnaire_flow": {"type": "Hub", "options": {}}})
    )


@pytest.fixture
def answer_store():
    return AnswerStore()


@pytest.fixture
def list_store():
    return ListStore()


@pytest.fixture
def progress_store():
    return ProgressStore()


@pytest.fixture
def people_answer_store():
    return AnswerStore(
        [
            {"answer_id": "first-name", "value": "Toni", "list_item_id": "PlwgoG"},
            {"answer_id": "last-name", "value": "Morrison", "list_item_id": "PlwgoG"},
            {"answer_id": "first-name", "value": "Barry", "list_item_id": "UHPLbX"},
            {"answer_id": "last-name", "value": "Pheloung", "list_item_id": "UHPLbX"},
        ]
    )


@pytest.fixture
def people_list_store():
    return ListStore([{"items": ["PlwgoG", "UHPLbX"], "name": "people"}])


@pytest.fixture
def response_metadata():
    return {"started_at": "2021-01-01T09:00:00.220038+00:00"}


@pytest.fixture
def fake_session_data():
    return SessionData(
        tx_id="tx_id",
        schema_name="some_schema_name",
        period_str="period_str",
        language_code=None,
        launch_language_code=None,
        schema_url=None,
        ru_name="ru_name",
        ru_ref="ru_ref",
        response_id="response_id",
        case_id="case_id",
    )


@pytest.fixture
def test_calculated_summary_schema():
    return load_schema_from_name("test_calculated_summary")


@pytest.fixture
def test_calculated_summary_answers():
    answers = [
        {"value": 1, "answer_id": "first-number-answer"},
        {"value": 2, "answer_id": "second-number-answer"},
        {"value": 3, "answer_id": "second-number-answer-unit-total"},
        {"value": 4, "answer_id": "second-number-answer-also-in-total"},
        {"value": 5, "answer_id": "third-number-answer"},
        {"value": 6, "answer_id": "third-and-a-half-number-answer-unit-total"},
        {"value": "No", "answer_id": "skip-fourth-block-answer"},
        {"value": 7, "answer_id": "fourth-number-answer"},
        {"value": 8, "answer_id": "fourth-and-a-half-number-answer-also-in-total"},
        {"value": 9, "answer_id": "fifth-percent-answer"},
        {"value": 10, "answer_id": "fifth-number-answer"},
        {"value": 11, "answer_id": "sixth-percent-answer"},
        {"value": 12, "answer_id": "sixth-number-answer"},
    ]
    return AnswerStore(answers)


@pytest.fixture
def test_section_summary_schema():
    return load_schema_from_name("test_section_summary")
