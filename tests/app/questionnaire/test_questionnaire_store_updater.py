from collections import defaultdict

import pytest
from mock import MagicMock, Mock
from mock.mock import call
from ordered_set import OrderedSet
from werkzeug.datastructures import MultiDict

from app.data_models import CompletionStatus, QuestionnaireStore, SupplementaryDataStore
from app.data_models.answer_store import AnswerDict, AnswerStore
from app.data_models.data_stores import DataStores
from app.data_models.list_store import ListStore
from app.data_models.progress import ProgressDict
from app.data_models.progress_store import ProgressStore
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import Dependent, QuestionnaireSchema
from app.questionnaire.questionnaire_store_updater import QuestionnaireStoreUpdater
from app.utilities.schema import load_schema_from_name
from app.utilities.types import DependentSection, SectionKey


# pylint: disable=too-many-locals, too-many-lines
def test_save_answers_with_form_data(
    mock_location,
    mock_empty_schema,
    mock_empty_answer_store,
    mock_questionnaire_store,
    mock_router,
):
    answer_id = "answer"
    answer_value = "1000"

    mock_empty_schema.get_answer_ids_for_question.return_value = [answer_id]
    mock_empty_schema.get_answers_for_question_by_id.return_value = {answer_id: {}}

    form_data = {answer_id: answer_value}

    current_question = mock_empty_schema.get_block(mock_location.block_id)["question"]
    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location,
        mock_empty_schema,
        mock_questionnaire_store,
        mock_router,
        current_question,
    )
    questionnaire_store_updater.update_answers(form_data)

    assert mock_empty_answer_store.add_or_update.call_count == 1

    created_answer = mock_empty_answer_store.add_or_update.call_args[0][0]
    assert created_answer.__dict__ == {
        "answer_id": answer_id,
        "list_item_id": None,
        "value": answer_value,
    }


def test_update_dynamic_answers(
    mock_location,
    mock_empty_schema,
    mock_questionnaire_store,
    mock_router,
):
    mock_empty_schema.get_answer_ids_for_question.return_value = [
        "percentage-of-shopping-vhECeh"
    ]
    mock_empty_schema.answer_dependencies = {
        "supermarket-name": {
            Dependent(
                section_id="section",
                block_id="dynamic-answer",
                for_list="supermarkets",
                answer_id="percentage-of-shopping",
            )
        }
    }

    mock_empty_schema.get_answers_for_question_by_id.return_value = {
        "percentage-of-shopping": {}
    }

    mock_questionnaire_store.data_stores.answer_store = AnswerStore(
        [
            {"answer_id": "any-supermarket-answer", "value": "Yes"},
            {
                "answer_id": "supermarket-name",
                "value": "Tesco",
                "list_item_id": "tUJzGV",
            },
            {
                "answer_id": "supermarket-name",
                "value": "Aldi",
                "list_item_id": "vhECeh",
            },
            {"answer_id": "list-collector-answer", "value": "No"},
            {
                "answer_id": "percentage-of-shopping",
                "value": 12,
                "list_item_id": "tUJzGV",
            },
        ]
    )

    form_data = {"percentage-of-shopping": 21}

    current_question = mock_empty_schema.get_block(mock_location.block_id)["question"]

    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location,
        mock_empty_schema,
        mock_questionnaire_store,
        mock_router,
        current_question,
    )
    questionnaire_store_updater._list_store = (  # pylint: disable=protected-access
        ListStore([{"items": ["tUJzGV", "vhECeh"], "name": "supermarkets"}])
    )
    questionnaire_store_updater.update_answers(form_data, list_item_id="vhECeh")

    assert mock_questionnaire_store.data_stores.answer_store == AnswerStore(
        [
            {"answer_id": "any-supermarket-answer", "value": "Yes"},
            {
                "answer_id": "supermarket-name",
                "value": "Tesco",
                "list_item_id": "tUJzGV",
            },
            {
                "answer_id": "supermarket-name",
                "value": "Aldi",
                "list_item_id": "vhECeh",
            },
            {"answer_id": "list-collector-answer", "value": "No"},
            {
                "answer_id": "percentage-of-shopping",
                "value": 12,
                "list_item_id": "tUJzGV",
            },
            {
                "answer_id": "percentage-of-shopping",
                "value": 21,
                "list_item_id": "vhECeh",
            },
        ]
    )


def test_save_empty_answer_removes_existing_answer(
    mock_empty_schema, mock_empty_answer_store, mock_questionnaire_store, mock_router
):
    answer_id = "answer"
    answer_value = "1000"
    list_item_id = "abc123"

    location = Location(
        section_id="section-foo",
        block_id="block-bar",
        list_name="people",
        list_item_id=list_item_id,
    )

    mock_empty_schema.get_answer_ids_for_question.return_value = [answer_id]

    mock_empty_schema.get_answers_for_question_by_id.return_value = {answer_id: {}}

    form_data = MultiDict({answer_id: answer_value})

    current_question = mock_empty_schema.get_block(location.block_id)["question"]
    questionnaire_store_updater = QuestionnaireStoreUpdater(
        location,
        mock_empty_schema,
        mock_questionnaire_store,
        mock_router,
        current_question,
    )
    questionnaire_store_updater.update_answers(form_data)

    assert mock_empty_answer_store.add_or_update.call_count == 1

    created_answer = mock_empty_answer_store.add_or_update.call_args[0][0]
    assert created_answer.__dict__ == {
        "answer_id": answer_id,
        "list_item_id": "abc123",
        "value": answer_value,
    }

    form_data = MultiDict({answer_id: ""})
    questionnaire_store_updater.update_answers(form_data)

    assert mock_empty_answer_store.remove_answer.call_count == 1
    used_answer_id = mock_empty_answer_store.remove_answer.call_args[0][0]
    used_list_item_id = mock_empty_answer_store.remove_answer.call_args[1][
        "list_item_id"
    ]
    assert (used_answer_id, used_list_item_id) == (answer_id, list_item_id)


def test_default_answers_are_not_saved(
    mock_location,
    mock_empty_schema,
    mock_empty_answer_store,
    mock_questionnaire_store,
    mock_router,
):
    answer_id = "answer"
    default_value = 0

    mock_empty_schema.get_answer_ids_for_question.return_value = [answer_id]
    mock_empty_schema.get_answers_by_answer_id.return_value = [
        {"default": default_value}
    ]
    mock_empty_schema.get_answers_for_question_by_id.return_value = {answer_id: {}}

    # No answer given so will use schema defined default
    form_data = MultiDict({answer_id: None})

    current_question = {"answers": [{"id": "answer", "default": default_value}]}
    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location,
        mock_empty_schema,
        mock_questionnaire_store,
        mock_router,
        current_question,
    )
    questionnaire_store_updater.update_answers(form_data)

    assert mock_empty_answer_store.add_or_update.call_count == 0


def test_empty_answers(
    mock_location,
    mock_empty_schema,
    mock_empty_answer_store,
    mock_questionnaire_store,
    mock_router,
):
    string_answer_id = "string-answer"
    checkbox_answer_id = "checkbox-answer"
    radio_answer_id = "radio-answer"

    mock_empty_schema.get_answer_ids_for_question.return_value = [
        string_answer_id,
        checkbox_answer_id,
        radio_answer_id,
    ]
    mock_empty_schema.get_answers_for_question_by_id.return_value = {
        string_answer_id: {},
        checkbox_answer_id: {},
        radio_answer_id: {},
    }

    form_data = {
        string_answer_id: "",
        checkbox_answer_id: [],
        radio_answer_id: None,
    }

    current_question = {
        "answers": [
            {"id": "string-answer"},
            {"id": "checkbox-answer"},
            {"id": "radio-answer"},
        ]
    }
    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location,
        mock_empty_schema,
        mock_questionnaire_store,
        mock_router,
        current_question,
    )
    questionnaire_store_updater.update_answers(form_data)

    assert mock_empty_answer_store.add_or_update.call_count == 0


def test_remove_all_answers_with_list_item_id(
    mock_location,
    mock_empty_schema,
    mock_router,
    mocker,
):
    mock_empty_answer_store = AnswerStore(
        answers=[
            {"answer_id": "test1", "value": 1, "list_item_id": "abcdef"},
            {"answer_id": "test2", "value": 2, "list_item_id": "abcdef"},
            {"answer_id": "test3", "value": 3, "list_item_id": "uvwxyz"},
        ]
    )

    mock_questionnaire_store = mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        data_stores=DataStores(
            answer_store=mock_empty_answer_store,
            list_store=mocker.MagicMock(spec=ListStore),
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        ),
    )

    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, mock_empty_schema, mock_questionnaire_store, mock_router, None
    )
    questionnaire_store_updater.remove_list_item_data("abc", "abcdef")

    assert len(mock_empty_answer_store) == 1
    assert mock_empty_answer_store.get_answer("test3", "uvwxyz")


def test_remove_primary_person(
    mock_location,
    mock_empty_schema,
    mock_router,
    populated_list_store,
    mocker,
):
    mock_empty_answer_store = AnswerStore(
        answers=[
            {"answer_id": "test1", "value": 1, "list_item_id": "abcdef"},
            {"answer_id": "test2", "value": 2, "list_item_id": "abcdef"},
            {"answer_id": "test3", "value": 3, "list_item_id": "xyzabc"},
        ]
    )

    mock_questionnaire_store = mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        data_stores=DataStores(
            answer_store=mock_empty_answer_store,
            list_store=populated_list_store,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        ),
    )

    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, mock_empty_schema, mock_questionnaire_store, mock_router, None
    )

    questionnaire_store_updater.remove_primary_person("people")


def test_add_primary_person(
    mock_location,
    mock_empty_schema,
    mock_empty_answer_store,
    mock_router,
    populated_list_store,
    mocker,
):
    mock_questionnaire_store = mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        data_stores=DataStores(
            answer_store=mock_empty_answer_store,
            list_store=populated_list_store,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        ),
    )

    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, mock_empty_schema, mock_questionnaire_store, mock_router, None
    )
    questionnaire_store_updater.add_primary_person("people")


def test_remove_completed_relationship_locations_for_list_name(
    mock_location,
    mock_empty_schema,
    mock_empty_answer_store,
    mock_empty_progress_store,
    mock_empty_supplementary_data_store,
    mock_router,
    populated_list_store,
    mocker,
):
    mock_empty_progress_store.add_completed_location(
        "section",
        Location(section_id="section", block_id="test-relationship-collector"),
    )
    mock_questionnaire_store = mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        data_stores=DataStores(
            answer_store=mock_empty_answer_store,
            list_store=populated_list_store,
            progress_store=mock_empty_progress_store,
            supplementary_data_store=mock_empty_supplementary_data_store,
        ),
    )
    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, mock_empty_schema, mock_questionnaire_store, mock_router, None
    )

    patch_method = "app.questionnaire.questionnaire_store_updater.QuestionnaireStoreUpdater._get_relationship_collectors_by_list_name"
    patched = mocker.patch(patch_method)
    patched.return_value = [{"id": "test-relationship-collector"}]
    questionnaire_store_updater.remove_completed_relationship_locations_for_list_name(
        "test-relationship-collector"
    )

    completed = mock_empty_progress_store.serialize()
    assert len(completed) == 0


@pytest.mark.usefixtures(
    "questionnaire_store_get_relationship_collectors_by_list_name_patch"
)
def test_remove_completed_relationship_locations_for_list_name_no_locations(
    mock_location,
    mock_empty_schema,
    mock_empty_answer_store,
    mock_empty_progress_store,
    mock_empty_supplementary_data_store,
    mock_router,
    populated_list_store,
    mocker,
):
    mock_empty_progress_store.add_completed_location(
        "section",
        Location(section_id="section", block_id="test-relationship-collector"),
    )
    initial_progress_store = mock_empty_progress_store.serialize()
    mock_questionnaire_store = mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        data_stores=DataStores(
            answer_store=mock_empty_answer_store,
            list_store=populated_list_store,
            progress_store=mock_empty_progress_store,
            supplementary_data_store=mock_empty_supplementary_data_store,
        ),
    )
    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, mock_empty_schema, mock_questionnaire_store, mock_router, None
    )

    questionnaire_store_updater.remove_completed_relationship_locations_for_list_name(
        "test-relationship-collector"
    )

    assert mock_empty_progress_store.serialize() == initial_progress_store


@pytest.mark.usefixtures(
    "questionnaire_store_get_relationship_collectors_by_list_name_patch"
)
def test_update_relationship_question_completeness_no_relationship_collectors(
    mock_location,
    mock_empty_schema,
    mock_empty_answer_store,
    mock_empty_progress_store,
    mock_empty_supplementary_data_store,
    mock_router,
    populated_list_store,
    mocker,
):
    mock_questionnaire_store = mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        data_stores=DataStores(
            answer_store=mock_empty_answer_store,
            list_store=populated_list_store,
            progress_store=mock_empty_progress_store,
            supplementary_data_store=mock_empty_supplementary_data_store,
        ),
    )
    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, mock_empty_schema, mock_questionnaire_store, mock_router, None
    )

    assert (
        questionnaire_store_updater._update_relationship_question_completeness(  # pylint: disable=protected-access
            "test-relationship-collector"
        )
        is None
    )


def test_update_same_name_items(
    mock_location,
    mock_empty_schema,
    mock_router,
    populated_list_store,
    mocker,
):
    mock_empty_answer_store = AnswerStore(
        answers=[
            {"answer_id": "first-name", "value": "Joe", "list_item_id": "abcdef"},
            {
                "answer_id": "middle-name",
                "value": "Brian",
                "list_item_id": "abcdef",
            },
            {"answer_id": "last-name", "value": "Bloggs", "list_item_id": "abcdef"},
            {"answer_id": "first-name", "value": "Joe", "list_item_id": "ghijkl"},
            {
                "answer_id": "middle-name",
                "value": "Roger",
                "list_item_id": "ghijkl",
            },
            {"answer_id": "last-name", "value": "Bloggs", "list_item_id": "ghijkl"},
            {
                "answer_id": "first-name",
                "value": "Martha",
                "list_item_id": "xyzabc",
            },
            {"answer_id": "last-name", "value": "Bloggs", "list_item_id": "xyzabc"},
        ]
    )

    mock_questionnaire_store = mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        data_stores=DataStores(
            answer_store=mock_empty_answer_store,
            list_store=populated_list_store,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        ),
    )

    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, mock_empty_schema, mock_questionnaire_store, mock_router, None
    )

    questionnaire_store_updater.update_same_name_items(
        "people", ["first-name", "last-name"]
    )

    assert "abcdef" in populated_list_store["people"].same_name_items
    assert "ghijkl" in populated_list_store["people"].same_name_items


def get_answer_dependencies(for_list=None):
    return {
        "total-employees-answer": {
            Dependent(
                section_id="breakdown-section",
                block_id="employees-breakdown-block",
                for_list=for_list,
                answer_id=None,
            )
        },
        "total-turnover-answer": {
            Dependent(
                section_id="breakdown-section",
                block_id="turnover-breakdown-block",
                for_list=for_list,
                answer_id=None,
            )
        },
    }


@pytest.mark.parametrize(
    "answer_id, answer_updated, answer_dependencies, is_repeating, expected_output",
    [
        (
            "total-employees-answer",
            True,
            get_answer_dependencies(),
            False,
            {("breakdown-section", None): {"employees-breakdown-block"}},
        ),
        (
            "total-turnover-answer",
            True,
            get_answer_dependencies(),
            False,
            {("breakdown-section", None): {"turnover-breakdown-block"}},
        ),
        (
            "total-employees-answer",
            True,
            get_answer_dependencies(for_list="people"),
            True,
            {("breakdown-section", "person-1"): {"employees-breakdown-block"}},
        ),
        (
            "total-turnover-answer",
            True,
            get_answer_dependencies(for_list="people"),
            True,
            {("breakdown-section", "person-1"): {"turnover-breakdown-block"}},
        ),
        (
            "total-employees-answer",
            True,
            get_answer_dependencies(for_list="people"),
            False,
            {
                ("breakdown-section", "person-1"): {"employees-breakdown-block"},
                ("breakdown-section", "person-2"): {"employees-breakdown-block"},
                ("breakdown-section", "person-3"): {"employees-breakdown-block"},
            },
        ),
        (
            "total-turnover-answer",
            True,
            get_answer_dependencies(for_list="people"),
            False,
            {
                ("breakdown-section", "person-1"): {"turnover-breakdown-block"},
                ("breakdown-section", "person-2"): {"turnover-breakdown-block"},
                ("breakdown-section", "person-3"): {"turnover-breakdown-block"},
            },
        ),
        (
            "total-employees-answer",
            False,
            get_answer_dependencies(),
            False,
            {},
        ),
    ],
)
def test_update_answers_captures_answer_dependencies(
    mock_empty_answer_store,
    mock_router,
    answer_id,
    answer_updated,
    answer_dependencies,
    is_repeating,
    expected_output,
    mock_schema,
):
    location = Location(
        section_id="default-section", block_id="default-block", list_item_id="person-1"
    )

    list_store = ListStore(
        [
            {
                "items": ["person-1", "person-2", "person-3"],
                "name": "people",
            }
        ]
    )

    mock_schema.get_answer_ids_for_question.return_value = [answer_id]
    mock_schema.answer_dependencies = answer_dependencies
    mock_schema.is_answer_in_repeating_section.return_value = is_repeating
    mock_schema.get_answers_for_question_by_id.return_value = {
        "total-employees-answer": {},
        "total-turnover-answer": {},
    }

    mock_empty_answer_store.add_or_update.return_value = answer_updated
    form_data = MultiDict({answer_id: "some-value"})

    current_question = mock_schema.get_block(location.block_id)["question"]
    questionnaire_store_updater = get_questionnaire_store_updater(
        schema=mock_schema,
        answer_store=mock_empty_answer_store,
        list_store=list_store,
        router=mock_router,
        current_location=location,
        current_question=current_question,
    )

    questionnaire_store_updater.update_answers(form_data)

    assert (
        questionnaire_store_updater.dependent_block_id_by_section_key == expected_output
    )


@pytest.mark.parametrize(
    "answer_dependent_answer_id, updated_answer_value, expected_output",
    [
        (
            # when the answer dependent has an answer_id, then the dependent answer should be removed from the answer store
            "second-answer",
            "answer updated",
            AnswerStore(
                [
                    AnswerDict(answer_id="first-answer", value="answer updated"),
                ]
            ),
        ),
        (  # when the answer dependent does not have an answer_id, then no answers should be removed from the store
            None,
            "answer updated",
            AnswerStore(
                [
                    AnswerDict(answer_id="first-answer", value="answer updated"),
                    AnswerDict(answer_id="second-answer", value="second answer"),
                ]
            ),
        ),
        (
            # When the answer dependent has an answer_id, but the answer dependency value is not changed, then the answer store should not change
            "second-answer",
            "original answer",
            AnswerStore(
                [
                    AnswerDict(answer_id="first-answer", value="original answer"),
                    AnswerDict(answer_id="second-answer", value="second answer"),
                ]
            ),
        ),
    ],
)
def test_update_answers_with_answer_dependents(
    mock_schema,
    mock_router,
    answer_dependent_answer_id,
    updated_answer_value,
    expected_output,
):
    answer_store = AnswerStore(
        [
            AnswerDict(answer_id="first-answer", value="original answer"),
            AnswerDict(
                answer_id="second-answer",
                value="second answer",
            ),
        ]
    )

    mock_schema.get_answer_ids_for_question.return_value = ["first-answer"]
    mock_schema.answer_dependencies = {
        "first-answer": {
            Dependent(
                section_id="section",
                block_id="second-block",
                for_list=None,
                answer_id=answer_dependent_answer_id,
            )
        },
    }
    mock_schema.get_answers_for_question_by_id.return_value = {
        "first-answer": {},
        "second-answer": {},
    }

    form_data = MultiDict({"first-answer": updated_answer_value})

    location = Location(
        section_id="section",
        block_id="first-block",
    )
    current_question = mock_schema.get_block(location.block_id)["question"]
    questionnaire_store_updater = get_questionnaire_store_updater(
        schema=mock_schema,
        answer_store=answer_store,
        list_store=ListStore(),
        router=mock_router,
        current_location=location,
        current_question=current_question,
    )
    questionnaire_store_updater.update_answers(form_data)

    assert answer_store == expected_output


@pytest.mark.parametrize(
    "is_repeating, expected_output",
    [
        (
            False,
            AnswerStore(
                [
                    AnswerDict(
                        answer_id="first-answer",
                        value="answer updated",
                        list_item_id="abc123",
                    ),
                ]
            ),
        ),
        (
            True,
            AnswerStore(
                [
                    AnswerDict(
                        answer_id="first-answer",
                        value="answer updated",
                        list_item_id="abc123",
                    ),
                    AnswerDict(
                        answer_id="second-answer",
                        value="second answer",
                        list_item_id="xyz456",
                    ),
                ]
            ),
        ),
    ],
)
def test_update_repeating_answers_with_answer_dependents(
    mock_schema, mock_router, is_repeating, expected_output
):
    # Given repeating dependent answers
    answer_store = AnswerStore(
        [
            AnswerDict(
                answer_id="first-answer", value="original-answer", list_item_id="abc123"
            ),
            AnswerDict(
                answer_id="second-answer", value="second answer", list_item_id="abc123"
            ),
            AnswerDict(
                answer_id="second-answer", value="second answer", list_item_id="xyz456"
            ),
        ]
    )
    list_store = ListStore([{"items": ["abc123", "xyz456"], "name": "list-name"}])

    mock_schema.get_answer_ids_for_question.return_value = ["first-answer"]
    mock_schema.answer_dependencies = {
        "first-answer": {
            Dependent(
                section_id="section",
                block_id="second-block",
                for_list="list-name",
                answer_id="second-answer",
            )
        },
    }
    mock_schema.get_answers_for_question_by_id.return_value = {
        "first-answer": {},
        "second-answer": {},
    }

    form_data = MultiDict({"first-answer": "answer updated"})

    location = Location(
        section_id="section", block_id="first-block", list_item_id="abc123"
    )
    current_question = mock_schema.get_block(location.block_id)["question"]

    mock_schema.is_answer_in_repeating_section.return_value = is_repeating
    questionnaire_store_updater = get_questionnaire_store_updater(
        schema=mock_schema,
        answer_store=answer_store,
        list_store=list_store,
        router=mock_router,
        current_location=location,
        current_question=current_question,
    )

    # when the questionnaire store is updated
    questionnaire_store_updater.update_answers(form_data)

    # Then all repeating dependent answers should be removed from the answer store
    assert answer_store == expected_output


@pytest.mark.parametrize(
    "section_status, updated_answer_value, is_path_complete, expected_status",
    [
        (
            # When an answer is changed which causes the path of a dependent section to be incomplete, Then that sections is update to IN_PROGRESS
            CompletionStatus.COMPLETED,
            "answer updated",
            False,
            CompletionStatus.IN_PROGRESS,
        ),
        (
            # When an answer is changed which causes the path of a dependent section to be complete, Then that sections is update to COMPLETED
            CompletionStatus.IN_PROGRESS,
            "answer updated",
            True,
            CompletionStatus.COMPLETED,
        ),
        (  # When an answer is not changed, Then a dependent section status should not change
            CompletionStatus.IN_PROGRESS,
            "original answer",
            False,
            CompletionStatus.IN_PROGRESS,
        ),
        (  # When an answer is not changed, Then a dependent section status should not change
            CompletionStatus.COMPLETED,
            "original answer",
            True,
            CompletionStatus.COMPLETED,
        ),
    ],
)
def test_answer_id_section_dependents(
    section_status,
    updated_answer_value,
    is_path_complete,
    expected_status,
    mock_schema,
    mock_router,
):
    mock_schema.get_answer_ids_for_question.return_value = ["first-answer"]
    mock_schema.get_repeating_list_for_section.return_value = None
    mock_schema.when_rules_section_dependencies_by_answer = {
        "first-answer": {"section-2"}
    }
    mock_schema.get_section_ids.return_value = ["section-1", "section-2"]
    mock_router.is_path_complete.return_value = is_path_complete
    mock_schema.get_answers_for_question_by_id.return_value = {
        "first-answer": {},
        "second-answer": {},
    }

    answer_store = AnswerStore(
        [
            AnswerDict(answer_id="first-answer", value="original answer"),
            AnswerDict(answer_id="second-answer", value="second answer"),
        ]
    )
    form_data = MultiDict({"first-answer": updated_answer_value})
    location = Location(
        section_id="section",
        block_id="first-block",
    )
    progress_store = ProgressStore(
        [
            ProgressDict(
                section_id="section-2",
                block_ids=["second-block"],
                status=section_status,
            )
        ],
    )
    current_question = mock_schema.get_block(location.block_id)["question"]
    questionnaire_store_updater = get_questionnaire_store_updater(
        schema=mock_schema,
        answer_store=answer_store,
        progress_store=progress_store,
        router=mock_router,
        current_location=location,
        current_question=current_question,
    )
    questionnaire_store_updater.update_answers(form_data)
    questionnaire_store_updater.update_progress_for_dependent_sections()

    assert progress_store.get_section_status(SectionKey("section-2")) is expected_status


@pytest.mark.parametrize(
    "list_item_1_section_status, list_item_2_section_status, updated_answer_value, "
    "is_list_item_1_path_complete, is_list_item_2_path_complete, expected_list_item_1_status, expected_list_item_2_status",
    [
        (
            # When an answer is changed which causes repeating dependent section to be incomplete, Then those repeating sections are updated to IN_PROGRESS
            CompletionStatus.COMPLETED,
            CompletionStatus.COMPLETED,
            "answer updated",
            False,
            False,
            CompletionStatus.IN_PROGRESS,
            CompletionStatus.IN_PROGRESS,
        ),
        (
            # When an answer is changed which causes repeating dependent section to be complete, Then those repeating sections are updated to COMPLETED
            CompletionStatus.IN_PROGRESS,
            CompletionStatus.IN_PROGRESS,
            "answer updated",
            True,
            True,
            CompletionStatus.COMPLETED,
            CompletionStatus.COMPLETED,
        ),
        (
            # When an answer is changed which causes repeating section paths to change, Then those repeating sections statuses are updated correctly
            CompletionStatus.COMPLETED,
            CompletionStatus.IN_PROGRESS,
            "answer updated",
            False,
            True,
            CompletionStatus.IN_PROGRESS,
            CompletionStatus.COMPLETED,
        ),
        (  # When an answer is not changed, Then a repeating dependent section status should not change
            CompletionStatus.COMPLETED,
            CompletionStatus.IN_PROGRESS,
            "original answer",
            True,
            False,
            CompletionStatus.COMPLETED,
            CompletionStatus.IN_PROGRESS,
        ),
    ],
)
def test_answer_id_section_dependents_repeating(
    list_item_1_section_status,
    list_item_2_section_status,
    updated_answer_value,
    is_list_item_1_path_complete,
    is_list_item_2_path_complete,
    expected_list_item_1_status,
    expected_list_item_2_status,
    mock_schema,
    mock_router,
):
    mock_schema.get_repeating_list_for_section.return_value = "list-name"
    mock_schema.get_answer_ids_for_question.return_value = ["first-answer"]
    mock_schema.when_rules_section_dependencies_by_answer = {
        "first-answer": {"section-2"}
    }
    mock_schema.get_section_ids.return_value = ["section-1", "section-2"]
    mock_schema.get_answers_for_question_by_id.return_value = {
        "first-answer": {},
        "second-answer": {},
    }

    answer_store = AnswerStore(
        [
            AnswerDict(answer_id="first-answer", value="original answer"),
            AnswerDict(
                answer_id="second-answer",
                value="second answer",
                list_item_id="list-item-id-1",
            ),
            AnswerDict(
                answer_id="second-answer",
                value="second answer",
                list_item_id="list-item-id-2",
            ),
        ]
    )
    list_store = ListStore(
        [{"items": ["list-item-id-1", "list-item-id-2"], "name": "list-name"}]
    )
    form_data = MultiDict({"first-answer": updated_answer_value})
    location = Location(
        section_id="section",
        block_id="first-block",
    )

    progress_store = ProgressStore(
        [
            ProgressDict(
                section_id="section-2",
                block_ids=["second-block"],
                status=list_item_1_section_status,
                list_item_id="list-item-id-1",
            ),
            ProgressDict(
                section_id="section-2",
                block_ids=["second-block"],
                status=list_item_2_section_status,
                list_item_id="list-item-id-2",
            ),
        ],
    )
    current_question = mock_schema.get_block(location.block_id)["question"]
    questionnaire_store_updater = get_questionnaire_store_updater(
        schema=mock_schema,
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
        router=mock_router,
        current_location=location,
        current_question=current_question,
    )
    questionnaire_store_updater.update_answers(form_data)

    # This test case is dependent on the order that the dependent_sections set is iterated over,
    # however as python sets are unordered we need to check that the first item is equal to our expected
    # list_item_id so that we can set the correct side effect as per the test case
    first_item = next(iter(questionnaire_store_updater.dependent_sections), None)
    effects = [is_list_item_1_path_complete, is_list_item_2_path_complete]
    if first_item and first_item.list_item_id != "list-item-id-1":
        effects = [is_list_item_2_path_complete, is_list_item_1_path_complete]
    mock_router.is_path_complete.side_effect = effects

    questionnaire_store_updater.update_progress_for_dependent_sections()

    assert (
        progress_store.get_section_status(SectionKey("section-2", "list-item-id-1"))
        is expected_list_item_1_status
    )
    assert (
        progress_store.get_section_status(SectionKey("section-2", "list-item-id-2"))
        is expected_list_item_2_status
    )


def get_questionnaire_store_updater(
    *,
    current_location=None,
    schema=None,
    answer_store=None,
    list_store=None,
    progress_store=None,
    router=None,
    current_question=None,
    supplementary_data_store=None,
):
    answer_store = AnswerStore() if answer_store is None else answer_store
    list_store = ListStore() if list_store is None else list_store
    progress_store = ProgressStore() if progress_store is None else progress_store
    supplementary_data_store = supplementary_data_store or SupplementaryDataStore()

    mock_schema = (
        MagicMock(
            QuestionnaireSchema({"questionnaire_flow": {"type": "Hub", "options": {}}})
        )
        if schema is None
        else schema
    )
    current_location = (
        Mock(spec=Location) if current_location is None else current_location
    )

    mock_questionnaire_store = MagicMock(
        spec=QuestionnaireStore,
        data_stores=DataStores(
            answer_store=answer_store,
            list_store=list_store,
            progress_store=progress_store,
            supplementary_data_store=supplementary_data_store,
        ),
    )
    current_question = current_question or {}

    return QuestionnaireStoreUpdater(
        current_location,
        mock_schema,
        mock_questionnaire_store,
        router,
        current_question,
    )


@pytest.mark.parametrize(
    "dependent_section_status",
    [CompletionStatus.IN_PROGRESS, CompletionStatus.COMPLETED],
)
def test_dependent_sections_completed_dependant_blocks_removed_and_status_updated(
    mocker, dependent_section_status, mock_router
):
    # Given
    current_location = Location(
        section_id="company-summary-section", block_id="breakdown-section"
    )
    progress_store = ProgressStore(
        [
            ProgressDict(
                section_id="company-summary-section",
                block_ids=["total-turnover-block", "total-employees-block"],
                status=CompletionStatus.COMPLETED,
            ),
            ProgressDict(
                section_id="breakdown-section",
                block_ids=[
                    "turnover-breakdown-block",
                ],
                status=dependent_section_status,
            ),
        ],
    )

    questionnaire_store_updater = get_questionnaire_store_updater(
        current_location=current_location,
        progress_store=progress_store,
        router=mock_router,
    )
    dependent_section_key = SectionKey("breakdown-section", None)
    dependent_block_id = "turnover-breakdown-block"

    questionnaire_store_updater.dependent_block_id_by_section_key = {
        dependent_section_key: {dependent_block_id}
    }

    assert dependent_block_id in progress_store.get_completed_block_ids(
        section_key=SectionKey(*dependent_section_key)
    )

    mocker.patch(
        "app.questionnaire.questionnaire_store_updater.QuestionnaireStoreUpdater._get_chronological_section_dependents",
        return_value=[
            DependentSection(
                section_id="breakdown-section", list_item_id=None, is_complete=False
            )
        ],
    )
    # When
    questionnaire_store_updater.remove_dependent_blocks_and_capture_dependent_sections()
    questionnaire_store_updater.update_progress_for_dependent_sections()

    # Then
    assert dependent_block_id not in progress_store.get_completed_block_ids(
        section_key=SectionKey(*dependent_section_key)
    )
    assert (
        progress_store.get_section_status(
            section_key=SectionKey(*dependent_section_key)
        )
        == CompletionStatus.IN_PROGRESS
    )


def test_dependent_sections_current_section_status_not_updated(mocker):
    # Given
    current_location = Location(
        section_id="breakdown-section", block_id="total-turnover-block"
    )
    progress_store = ProgressStore(
        [
            ProgressDict(
                section_id="breakdown-section",
                block_ids=[
                    "total-turnover-block",
                    "turnover-breakdown-block",
                ],
                status=CompletionStatus.COMPLETED,
            ),
        ],
    )
    questionnaire_store_updater = get_questionnaire_store_updater(
        current_location=current_location, progress_store=progress_store
    )
    dependent_section_key = ("breakdown-section", None)
    dependent_block_id = "turnover-breakdown-block"

    questionnaire_store_updater.dependent_block_id_by_section_key = {
        dependent_section_key: {dependent_block_id}
    }

    questionnaire_store_updater.update_section_status = mocker.Mock()
    assert dependent_block_id in progress_store.get_completed_block_ids(
        section_key=SectionKey(*dependent_section_key)
    )

    # When
    questionnaire_store_updater.remove_dependent_blocks_and_capture_dependent_sections()
    questionnaire_store_updater.update_progress_for_dependent_sections()

    # Then
    assert dependent_block_id not in progress_store.get_completed_block_ids(
        section_key=SectionKey(*dependent_section_key)
    )
    # Status for current section is handled separately by handle post.
    assert questionnaire_store_updater.update_section_status.call_count == 0


def test_dependent_sections_not_started_skipped(mock_router, mocker):
    # Given
    schema = load_schema_from_name(
        "test_validation_sum_against_total_hub_with_dependent_section"
    )
    current_location = Location(
        section_id="company-summary-section", block_id="total-turnover-block"
    )
    progress_store = ProgressStore(
        [
            ProgressDict(
                section_id="company-summary-section",
                block_ids=["total-turnover-block", "total-employees-block"],
                status=CompletionStatus.COMPLETED,
            )
        ],
    )
    questionnaire_store_updater = get_questionnaire_store_updater(
        current_location=current_location,
        progress_store=progress_store,
        router=mock_router,
        schema=schema,
    )

    dependent_section_key = ("breakdown-section", None)
    dependent_block_id = "turnover-breakdown-block"

    questionnaire_store_updater.dependent_block_id_by_section_key = {
        dependent_section_key: {dependent_block_id}
    }

    questionnaire_store_updater.remove_completed_location = mocker.Mock()
    questionnaire_store_updater.update_section_status = mocker.Mock()

    # When
    questionnaire_store_updater.remove_dependent_blocks_and_capture_dependent_sections()
    questionnaire_store_updater.update_progress_for_dependent_sections()

    # Then
    assert questionnaire_store_updater.remove_completed_location.call_count == 0
    assert questionnaire_store_updater.update_section_status.call_count == 0


def test_dependent_sections_started_but_blocks_incomplete(mock_router, mocker):
    # Given
    current_location = Location(
        section_id="company-summary-section", block_id="total-employees-block"
    )
    progress_store = ProgressStore(
        [
            ProgressDict(
                section_id="company-summary-section",
                block_ids=["total-turnover-block", "total-employees-block"],
                status=CompletionStatus.COMPLETED,
            ),
            ProgressDict(
                section_id="breakdown-section",
                block_ids=[
                    "turnover-breakdown-block",
                ],
                status=CompletionStatus.IN_PROGRESS,
            ),
        ],
    )
    questionnaire_store_updater = get_questionnaire_store_updater(
        current_location=current_location,
        progress_store=progress_store,
        router=mock_router,
    )

    dependent_section_key = ("breakdown-section", None)
    dependent_block_id = "total-employees-block"

    questionnaire_store_updater.dependent_block_id_by_section_key = {
        dependent_section_key: {dependent_block_id}
    }
    questionnaire_store_updater.update_section_status = mocker.Mock()

    assert dependent_block_id not in progress_store.get_completed_block_ids(
        section_key=SectionKey(*dependent_section_key)
    )

    # When
    questionnaire_store_updater.remove_dependent_blocks_and_capture_dependent_sections()
    questionnaire_store_updater.update_progress_for_dependent_sections()

    # Then
    assert questionnaire_store_updater.update_section_status.call_count == 0


@pytest.mark.parametrize(
    "dependent_section_status",
    [CompletionStatus.IN_PROGRESS, CompletionStatus.COMPLETED],
)
def test_repeating_dependent_sections_completed_dependant_blocks_removed_and_status_updated(
    mocker, dependent_section_status, mock_router
):
    schema = load_schema_from_name(
        "test_validation_sum_against_total_hub_with_dependent_section"
    )
    current_location = Location(
        section_id="company-summary-section", block_id="total-turnover-block"
    )
    list_store = ListStore(
        [
            {
                "items": ["item-1", "item-2"],
                "name": "some-list",
            }
        ]
    )
    progress_store = ProgressStore(
        [
            ProgressDict(
                section_id="company-summary-section",
                block_ids=["total-turnover-block", "total-employees-block"],
                status=CompletionStatus.COMPLETED,
            ),
            {
                "section_id": "breakdown-section",
                "list_item_id": "item-1",
                "block_ids": [
                    "turnover-breakdown-block",
                ],
                "status": dependent_section_status,
            },
            {
                "section_id": "breakdown-section",
                "list_item_id": "item-2",
                "block_ids": [
                    "turnover-breakdown-block",
                ],
                "status": dependent_section_status,
            },
        ],
    )
    questionnaire_store_updater = get_questionnaire_store_updater(
        current_location=current_location,
        progress_store=progress_store,
        list_store=list_store,
        router=mock_router,
        schema=schema,
    )

    questionnaire_store_updater.dependent_block_id_by_section_key = {
        SectionKey("breakdown-section", list_item): {"turnover-breakdown-block"}
        for list_item in list_store["some-list"]
    }
    questionnaire_store_updater.dependent_sections.add(
        DependentSection(
            section_id="breakdown-section", list_item_id="item-1", is_complete=None
        )
    )

    mocker.patch(
        "app.questionnaire.questionnaire_store_updater.QuestionnaireStoreUpdater._get_chronological_section_dependents",
        return_value=[
            DependentSection(
                section_id="breakdown-section", list_item_id=None, is_complete=None
            )
        ],
    )
    # When
    questionnaire_store_updater.remove_dependent_blocks_and_capture_dependent_sections()
    questionnaire_store_updater.update_progress_for_dependent_sections()

    # Then
    for list_item in list_store["some-list"]:
        section_id, list_item_id = "breakdown-section", list_item
        assert "turnover-breakdown-block" not in progress_store.get_completed_block_ids(
            SectionKey(section_id, list_item_id)
        )
        assert (
            progress_store.get_section_status(SectionKey(section_id, list_item_id))
            == CompletionStatus.IN_PROGRESS
        )
        assert questionnaire_store_updater.dependent_sections == {
            DependentSection(
                section_id=section_id, list_item_id="item-1", is_complete=False
            ),
            DependentSection(
                section_id=section_id, list_item_id="item-2", is_complete=False
            ),
        }


@pytest.mark.parametrize(
    "dependent_section_status",
    [CompletionStatus.IN_PROGRESS, CompletionStatus.COMPLETED],
)
def test_dependent_sections_added_dependant_block_removed(
    dependent_section_status, mock_router
):
    # Given
    current_location = Location(
        section_id="company-summary-section", block_id="total-turnover-block"
    )
    progress_store = ProgressStore(
        [
            ProgressDict(
                section_id="company-summary-section",
                block_ids=["total-turnover-block", "total-employees-block"],
                status=CompletionStatus.COMPLETED,
            ),
            ProgressDict(
                section_id="breakdown-section",
                block_ids=[
                    "turnover-breakdown-block",
                ],
                status=dependent_section_status,
            ),
        ],
    )
    questionnaire_store_updater = get_questionnaire_store_updater(
        current_location=current_location,
        progress_store=progress_store,
        router=mock_router,
    )
    dependent_section_key = SectionKey("breakdown-section", None)
    dependent_block_id = "turnover-breakdown-block"

    questionnaire_store_updater.dependent_block_id_by_section_key = {
        dependent_section_key: {dependent_block_id}
    }

    assert dependent_block_id in progress_store.get_completed_block_ids(
        section_key=SectionKey(*dependent_section_key)
    )
    assert questionnaire_store_updater.dependent_sections == set()

    # When
    questionnaire_store_updater.remove_dependent_blocks_and_capture_dependent_sections()

    # Then
    assert dependent_block_id not in progress_store.get_completed_block_ids(
        section_key=SectionKey(*dependent_section_key)
    )
    assert questionnaire_store_updater.dependent_sections == {
        DependentSection(
            section_id="breakdown-section", list_item_id=None, is_complete=False
        )
    }


@pytest.mark.parametrize(
    "status_unchanged_section_ids, expected_routing_path_calls",
    [
        (
            # s1.s1 -> s1.s2 -> s2.s3 -> s3.s4 -> s3.s5 -> s3.s7 -> s2.s6
            [],
            [
                call(SectionKey("section-1")),
                call(SectionKey("section-2")),
                call(SectionKey("section-3")),
                call(SectionKey("section-4")),
                call(SectionKey("section-5")),
                call(SectionKey("section-7")),
                call(SectionKey("section-6")),
            ],
        ),
        (
            # s1 -> s1.s2 -> s1.s3 -> s3.s4 -> s3.s5 -> s3.s7
            ["section-2"],
            [
                call(SectionKey("section-1")),
                call(SectionKey("section-2")),
                call(SectionKey("section-3")),
                call(SectionKey("section-4")),
                call(SectionKey("section-5")),
                call(SectionKey("section-7")),
            ],
        ),
        (
            # s1 -> s1.s2 -> s2.s3 -> s2.s4 -> s2.s5 -> s2.s6
            ["section-3"],
            [
                call(SectionKey("section-1")),
                call(SectionKey("section-2")),
                call(SectionKey("section-3")),
                call(SectionKey("section-4")),
                call(SectionKey("section-5")),
                call(SectionKey("section-6")),
            ],
        ),
    ],
)
def test_questionnaire_store_updater_dependency_capture(
    mocker,
    mock_router,
    mock_schema,
    status_unchanged_section_ids,
    expected_routing_path_calls,
):
    """
    This test is intended to ensure that the order in which dependencies are captured and evaluated is correct.
    We should only call the routing path for a given section once and need to ensure that only the necessary paths are evaluated
    i.e. only sections in which the status has changed should be evaluated.
    """
    current_location = Location(section_id="section-1", block_id="block-2")
    mock_dependencies = defaultdict(OrderedSet) | {
        "section-1": OrderedSet(["section-2", "section-3"]),
        "section-2": OrderedSet(["section-3", "section-4", "section-5", "section-6"]),
        "section-3": OrderedSet(["section-4", "section-5", "section-7"]),
    }
    mock_schema.when_rules_section_dependencies_by_section_for_progress_value_source = (
        mock_dependencies
    )
    mock_schema.get_repeating_list_for_section.return_value = False
    mock_router.is_path_complete.return_value = (
        False  # This will result in new status being IN=PROGRESS
    )
    progress_store = ProgressStore(
        [
            {
                "section_id": f"section-{idx}",
                "block_ids": ["block-1", "block-2"],
                "status": (
                    CompletionStatus.IN_PROGRESS
                    if f"section-{idx}" in status_unchanged_section_ids
                    else CompletionStatus.COMPLETED
                ),
            }
            for idx in range(1, 8)
        ],
    )
    questionnaire_store_updater = get_questionnaire_store_updater(
        current_location=current_location,
        progress_store=progress_store,
        router=mock_router,
        schema=mock_schema,
    )
    mocker.patch(
        "app.questionnaire.questionnaire_store_updater.QuestionnaireStoreUpdater._get_chronological_section_dependents",
        return_value=[
            DependentSection(
                section_id="section-1", list_item_id=None, is_complete=None
            ),
            DependentSection(
                section_id="section-2", list_item_id=None, is_complete=None
            ),
        ],
    )
    questionnaire_store_updater.update_progress_for_dependent_sections()
    assert mock_router.routing_path.call_args_list == expected_routing_path_calls
