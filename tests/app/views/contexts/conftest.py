import pytest
from mock import MagicMock

from app.data_models import QuestionnaireStore
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
def repeating_blocks_answer_store():
    return AnswerStore(
        [
            {
                "answer_id": "company-or-branch-name",
                "value": "CompanyA",
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "registration-number",
                "value": "123",
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "registration-date",
                "value": "2023-01-01",
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "authorised-trader-uk-radio",
                "value": "Yes",
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "authorised-trader-eu-radio",
                "value": "Yes",
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "company-or-branch-name",
                "value": "CompanyB",
                "list_item_id": "UHPLbX",
            },
            {
                "answer_id": "registration-number",
                "value": "456",
                "list_item_id": "UHPLbX",
            },
            {
                "answer_id": "registration-date",
                "value": "2023-01-01",
                "list_item_id": "UHPLbX",
            },
            {
                "answer_id": "authorised-trader-uk-radio",
                "value": "No",
                "list_item_id": "UHPLbX",
            },
            {
                "answer_id": "authorised-trader-eu-radio",
                "value": "No",
                "list_item_id": "UHPLbX",
            },
        ]
    )


@pytest.fixture
def companies_answer_store():
    return AnswerStore(
        [
            {
                "answer_id": "company-or-branch-name",
                "value": "company a",
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "registration-number",
                "value": 123,
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "authorised-insurer-radio",
                "value": "Yes",
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "company-or-branch-name",
                "value": "company b",
                "list_item_id": "UHPLbX",
            },
            {
                "answer_id": "registration-number",
                "value": 456,
                "list_item_id": "UHPLbX",
            },
            {
                "answer_id": "authorised-insurer-radio",
                "value": "No",
                "list_item_id": "UHPLbX",
            },
        ]
    )


@pytest.fixture
def companies_variants_answer_store_first_variant():
    return AnswerStore(
        [
            {
                "answer_id": "uk-based-answer",
                "value": "Yes",
            },
            {
                "answer_id": "company-or-branch-name",
                "value": "company a",
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "registration-number",
                "value": 123,
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "authorised-insurer-radio",
                "value": "Yes",
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "company-or-branch-name",
                "value": "company b",
                "list_item_id": "UHPLbX",
            },
            {
                "answer_id": "registration-number",
                "value": 456,
                "list_item_id": "UHPLbX",
            },
            {
                "answer_id": "authorised-insurer-radio",
                "value": "No",
                "list_item_id": "UHPLbX",
            },
        ]
    )


@pytest.fixture
def companies_variants_answer_store_second_variant():
    return AnswerStore(
        [
            {
                "answer_id": "uk-based-answer",
                "value": "No",
            },
            {
                "answer_id": "company-or-branch-name",
                "value": "company a",
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "registration-number",
                "value": 123,
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "authorised-insurer-radio",
                "value": "Yes",
                "list_item_id": "PlwgoG",
            },
            {
                "answer_id": "company-or-branch-name",
                "value": "company b",
                "list_item_id": "UHPLbX",
            },
            {
                "answer_id": "registration-number",
                "value": 456,
                "list_item_id": "UHPLbX",
            },
            {
                "answer_id": "authorised-insurer-radio",
                "value": "No",
                "list_item_id": "UHPLbX",
            },
        ]
    )


@pytest.fixture
def people_list_store():
    return ListStore([{"items": ["PlwgoG", "UHPLbX"], "name": "people"}])


@pytest.fixture
def repeating_blocks_list_store():
    return ListStore([{"items": ["PlwgoG", "UHPLbX"], "name": "companies"}])


@pytest.fixture
def response_metadata():
    return {"started_at": "2021-01-01T09:00:00.220038+00:00"}


@pytest.fixture
def fake_session_data():
    return SessionData(
        language_code=None,
    )


@pytest.fixture
def test_calculated_summary_schema():
    return load_schema_from_name("test_calculated_summary")


@pytest.fixture
def test_grand_calculated_summary_schema():
    return load_schema_from_name("test_grand_calculated_summary")


@pytest.fixture
def test_calculated_summary_repeating_and_static_answers_schema():
    return load_schema_from_name(
        "test_new_calculated_summary_repeating_and_static_answers"
    )


@pytest.fixture
def test_calculated_summary_repeating_blocks():
    return load_schema_from_name("test_new_calculated_summary_repeating_blocks")


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
def test_grand_calculated_summary_answers():
    answers = [
        {"value": 10, "answer_id": "q1-a1"},
        {"value": 1, "answer_id": "q1-a2"},
        {"value": 20, "answer_id": "q2-a1"},
        {"value": 2, "answer_id": "q2-a2"},
        {"value": 30, "answer_id": "q3-a1"},
        {"value": 3, "answer_id": "q3-a2"},
        {"value": 40, "answer_id": "q4-a1"},
        {"value": 4, "answer_id": "q4-a2"},
    ]
    return AnswerStore(answers)


@pytest.fixture
def test_calculated_summary_answers_skipped_fourth():
    answers = [
        {"value": 1, "answer_id": "first-number-answer"},
        {"value": 2, "answer_id": "second-number-answer"},
        {"value": 3, "answer_id": "second-number-answer-unit-total"},
        {"value": 4, "answer_id": "second-number-answer-also-in-total"},
        {"value": 5, "answer_id": "third-number-answer"},
        {"value": 6, "answer_id": "third-and-a-half-number-answer-unit-total"},
        {"value": "Yes", "answer_id": "skip-fourth-block-answer"},
        {"value": 9, "answer_id": "fifth-percent-answer"},
        {"value": 10, "answer_id": "fifth-number-answer"},
        {"value": 11, "answer_id": "sixth-percent-answer"},
        {"value": 12, "answer_id": "sixth-number-answer"},
    ]
    return AnswerStore(answers)


@pytest.fixture
def test_section_summary_schema():
    return load_schema_from_name("test_section_summary")


@pytest.fixture
def test_introduction_preview_linear_schema():
    return load_schema_from_name("test_introduction")


@pytest.fixture
def questionnaire_store():
    storage = MagicMock()
    storage.get_user_data = MagicMock(return_value=("{}", "ce_sid", 1, None))
    storage.add_or_update = MagicMock()

    store = QuestionnaireStore(storage)

    store.answer_store = AnswerStore()
    store.metadata = {
        "ru_name": "ESSENTIAL ENTERPRISE LTD.",
        "ref_p_start_date": "2016-02-02",
        "ref_p_end_date": "2016-03-03",
        "display_address": "68 Abingdon Road, Goathill",
        "trad_as": "ESSENTIAL ENTERPRISE LTD.",
        "ru_ref": "12346789012A",
    }

    store.response_metadata = {"started_at": "2018-07-04T14:49:33.448608+00:00"}

    return store
