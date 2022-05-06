import pytest
from mock import MagicMock, Mock
from werkzeug.datastructures import MultiDict

from app.data_models import QuestionnaireStore
from app.data_models.answer_store import AnswerDict, AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress_store import CompletionStatus, ProgressStore
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import AnswerDependent, QuestionnaireSchema
from app.questionnaire.questionnaire_store_updater import QuestionnaireStoreUpdater


# pylint: disable=too-many-locals
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
        existing_answers=[
            {"answer_id": "test1", "value": 1, "list_item_id": "abcdef"},
            {"answer_id": "test2", "value": 2, "list_item_id": "abcdef"},
            {"answer_id": "test3", "value": 3, "list_item_id": "uvwxyz"},
        ]
    )

    mock_questionnaire_store = mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        answer_store=mock_empty_answer_store,
        list_store=mocker.MagicMock(spec=ListStore),
        progress_store=ProgressStore(),
    )

    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, mock_empty_schema, mock_questionnaire_store, mock_router, None
    )
    questionnaire_store_updater.remove_list_item_and_answers("abc", "abcdef")

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
        existing_answers=[
            {"answer_id": "test1", "value": 1, "list_item_id": "abcdef"},
            {"answer_id": "test2", "value": 2, "list_item_id": "abcdef"},
            {"answer_id": "test3", "value": 3, "list_item_id": "xyzabc"},
        ]
    )

    mock_questionnaire_store = mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        answer_store=mock_empty_answer_store,
        list_store=populated_list_store,
        progress_store=ProgressStore(),
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
        answer_store=mock_empty_answer_store,
        list_store=populated_list_store,
        progress_store=ProgressStore(),
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
        answer_store=mock_empty_answer_store,
        list_store=populated_list_store,
        progress_store=mock_empty_progress_store,
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
        answer_store=mock_empty_answer_store,
        list_store=populated_list_store,
        progress_store=mock_empty_progress_store,
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
    mock_router,
    populated_list_store,
    mocker,
):
    mock_questionnaire_store = mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        answer_store=mock_empty_answer_store,
        list_store=populated_list_store,
        progress_store=mock_empty_progress_store,
    )
    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, mock_empty_schema, mock_questionnaire_store, mock_router, None
    )

    assert (
        questionnaire_store_updater.update_relationship_question_completeness(
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
        existing_answers=[
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
        answer_store=mock_empty_answer_store,
        list_store=populated_list_store,
        progress_store=ProgressStore(),
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
            AnswerDependent(
                section_id="breakdown-section",
                block_id="employees-breakdown-block",
                for_list=for_list,
                answer_id=None,
            )
        },
        "total-turnover-answer": {
            AnswerDependent(
                section_id="breakdown-section",
                block_id="turnover-breakdown-block",
                for_list=for_list,
                answer_id=None,
            )
        },
    }


@pytest.mark.parametrize(
    "answer_id, answer_updated, answer_dependencies, expected_output",
    [
        (
            "total-employees-answer",
            True,
            get_answer_dependencies(),
            {("breakdown-section", None): {"employees-breakdown-block"}},
        ),
        (
            "total-turnover-answer",
            True,
            get_answer_dependencies(),
            {("breakdown-section", None): {"turnover-breakdown-block"}},
        ),
        (
            "total-employees-answer",
            True,
            get_answer_dependencies(for_list="people"),
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
    expected_output,
    mock_schema,
):
    location = Location(
        section_id="default-section",
        block_id="default-block",
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
        (  # when the answer dependent has an answer_id, then the dependent answer should be removed from the answer store
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
        (  # When the answer dependent has an answer_id, but the answer dependency value is not changed, then the answer store should not change
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
            AnswerDependent(
                section_id="section",
                block_id="second-block",
                for_list=None,
                answer_id=answer_dependent_answer_id,
            )
        },
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


def test_update_repeating_answers_with_answer_dependents(mock_schema, mock_router):
    # Given repeating dependent answers
    answer_store = AnswerStore(
        [
            AnswerDict(answer_id="first-answer", value="original-answer"),
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
            AnswerDependent(
                section_id="section",
                block_id="second-block",
                for_list="list-name",
                answer_id="second-answer",
            )
        },
    }

    form_data = MultiDict({"first-answer": "answer updated"})

    location = Location(
        section_id="section",
        block_id="first-block",
    )
    current_question = mock_schema.get_block(location.block_id)["question"]
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
    assert answer_store == AnswerStore(
        [AnswerDict(answer_id="first-answer", value="answer updated")]
    )


@pytest.mark.parametrize(
    "section_status, updated_answer_value, is_path_complete, expected_status",
    [
        (  # When an answer is changed which causes the path of a dependent section to be incomplete, Then that sections is update to IN_PROGRESS
            "COMPLETED",
            "answer updated",
            False,
            "IN_PROGRESS",
        ),
        (  # When an answer is changed which causes the path of a dependent section to be complete, Then that sections is update to COMPLETED
            "IN_PROGRESS",
            "answer updated",
            True,
            "COMPLETED",
        ),
        (  # When an answer is not changed, Then a dependent section status should not change
            "IN_PROGRESS",
            "original answer",
            False,
            "IN_PROGRESS",
        ),
        (  # When an answer is not changed, Then a dependent section status should not change
            "COMPLETED",
            "original answer",
            True,
            "COMPLETED",
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
    mock_schema.when_rules_section_dependencies_by_answer = {"first-answer": {"section-2"}}
    mock_router.is_path_complete.return_value = is_path_complete

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
            {
                "section_id": "section-2",
                "block_ids": ["second-block"],
                "status": section_status,
            }
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

    assert progress_store.get_section_status(section_id="section-2") is expected_status


@pytest.mark.parametrize(
    "list_item_1_section_status, list_item_2_section_status, updated_answer_value, "
    "is_list_item_1_path_complete, is_list_item_2_path_complete, expected_list_item_1_status, expected_list_item_2_status",
    [
        (  # When an answer is changed which causes repeating dependent section to be incomplete, Then those repeating sections are updated to IN_PROGRESS
            "COMPLETED",
            "COMPLETED",
            "answer updated",
            False,
            False,
            "IN_PROGRESS",
            "IN_PROGRESS",
        ),
        (  # When an answer is changed which causes repeating dependent section to be complete, Then those repeating sections are updated to COMPLETED
            "IN_PROGRESS",
            "IN_PROGRESS",
            "answer updated",
            True,
            True,
            "COMPLETED",
            "COMPLETED",
        ),
        (  # When an answer is changed which causes repeating section paths to change, Then those repeating sections statuses are updated correctly
            "COMPLETED",
            "IN_PROGRESS",
            "answer updated",
            False,
            True,
            "IN_PROGRESS",
            "COMPLETED",
        ),
        (  # When an answer is not changed, Then a repeating dependent section status should not change
            "COMPLETED",
            "IN_PROGRESS",
            "original answer",
            True,
            False,
            "COMPLETED",
            "IN_PROGRESS",
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
    mock_router.is_path_complete.side_effect = [
        is_list_item_1_path_complete,
        is_list_item_2_path_complete,
    ]
    mock_schema.when_rules_section_dependencies_by_answer = {"first-answer": {"section-2"}}

    answer_store = AnswerStore(
        [
            AnswerDict(answer_id="first-answer", value="original answer"),
            AnswerDict(
                answer_id="second-answer", value="second answer", list_item_id="abc123"
            ),
            AnswerDict(
                answer_id="second-answer", value="second answer", list_item_id="xyz456"
            ),
        ]
    )
    list_store = ListStore([{"items": ["abc123", "xyz456"], "name": "list-name"}])
    form_data = MultiDict({"first-answer": updated_answer_value})
    location = Location(
        section_id="section",
        block_id="first-block",
    )

    progress_store = ProgressStore(
        [
            {
                "section_id": "section-2",
                "block_ids": ["second-block"],
                "status": list_item_1_section_status,
                "list_item_id": "abc123",
            },
            {
                "section_id": "section-2",
                "block_ids": ["second-block"],
                "status": list_item_2_section_status,
                "list_item_id": "xyz456",
            },
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
    questionnaire_store_updater.update_progress_for_dependent_sections()

    assert (
        progress_store.get_section_status(section_id="section-2", list_item_id="abc123")
        is expected_list_item_1_status
    )
    assert (
        progress_store.get_section_status(section_id="section-2", list_item_id="xyz456")
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
):
    answer_store = AnswerStore() if answer_store is None else answer_store
    list_store = ListStore() if list_store is None else list_store
    progress_store = ProgressStore() if progress_store is None else progress_store
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
        answer_store=answer_store,
        list_store=list_store,
        progress_store=progress_store,
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
    dependent_section_status, mock_router
):
    # Given
    current_location = Location(
        section_id="company-summary-section", block_id="total-turnover-block"
    )
    progress_store = ProgressStore(
        [
            {
                "section_id": "company-summary-section",
                "block_ids": ["total-turnover-block", "total-employees-block"],
                "status": "COMPLETED",
            },
            {
                "section_id": "breakdown-section",
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
        router=mock_router,
    )
    dependent_section_key = ("breakdown-section", None)
    dependent_block_id = "turnover-breakdown-block"

    questionnaire_store_updater.dependent_block_id_by_section_key = {
        dependent_section_key: {dependent_block_id}
    }

    assert dependent_block_id in progress_store.get_completed_block_ids(
        *dependent_section_key
    )

    # When
    questionnaire_store_updater.update_progress_for_dependent_sections()

    # Then
    assert dependent_block_id not in progress_store.get_completed_block_ids(
        *dependent_section_key
    )
    assert (
        progress_store.get_section_status(*dependent_section_key)
        == CompletionStatus.IN_PROGRESS
    )


def test_dependent_sections_current_section_status_not_updated(mocker):
    # Given
    current_location = Location(
        section_id="breakdown-section", block_id="total-turnover-block"
    )
    progress_store = ProgressStore(
        [
            {
                "section_id": "breakdown-section",
                "block_ids": [
                    "total-turnover-block",
                    "turnover-breakdown-block",
                ],
                "status": CompletionStatus.COMPLETED,
            },
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
        *dependent_section_key
    )

    # When
    questionnaire_store_updater.update_progress_for_dependent_sections()

    # Then
    assert dependent_block_id not in progress_store.get_completed_block_ids(
        *dependent_section_key
    )
    # Status for current section is handled separately by handle post.
    assert questionnaire_store_updater.update_section_status.call_count == 0


def test_dependent_sections_not_started_skipped(mock_router, mocker):
    # Given
    current_location = Location(
        section_id="company-summary-section", block_id="total-turnover-block"
    )
    progress_store = ProgressStore(
        [
            {
                "section_id": "company-summary-section",
                "block_ids": ["total-turnover-block", "total-employees-block"],
                "status": "COMPLETED",
            }
        ],
    )
    questionnaire_store_updater = get_questionnaire_store_updater(
        current_location=current_location,
        progress_store=progress_store,
        router=mock_router,
    )

    dependent_section_key = ("breakdown-section", None)
    dependent_block_id = "turnover-breakdown-block"

    questionnaire_store_updater.dependent_block_id_by_section_key = {
        dependent_section_key: {dependent_block_id}
    }

    questionnaire_store_updater.remove_completed_location = mocker.Mock()
    questionnaire_store_updater.update_section_status = mocker.Mock()

    # When
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
            {
                "section_id": "company-summary-section",
                "block_ids": ["total-turnover-block", "total-employees-block"],
                "status": "COMPLETED",
            },
            {
                "section_id": "breakdown-section",
                "block_ids": [
                    "turnover-breakdown-block",
                ],
                "status": "IN_PROGRESS",
            },
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
        *dependent_section_key
    )

    # When
    questionnaire_store_updater.update_progress_for_dependent_sections()

    # Then
    assert questionnaire_store_updater.update_section_status.call_count == 0


@pytest.mark.parametrize(
    "dependent_section_status",
    [CompletionStatus.IN_PROGRESS, CompletionStatus.COMPLETED],
)
def test_repeating_dependent_sections_completed_dependant_blocks_removed_and_status_updated(
    dependent_section_status, mock_router
):
    # Given
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
            {
                "section_id": "company-summary-section",
                "block_ids": ["total-turnover-block", "total-employees-block"],
                "status": "COMPLETED",
            },
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
    )

    questionnaire_store_updater.dependent_block_id_by_section_key = {
        ("breakdown-section", list_item): {"turnover-breakdown-block"}
        for list_item in list_store["some-list"]
    }

    # When
    questionnaire_store_updater.update_progress_for_dependent_sections()

    # Then
    for list_item in list_store["some-list"]:
        section_id, list_item_id = "breakdown-section", list_item
        assert "turnover-breakdown-block" not in progress_store.get_completed_block_ids(
            section_id, list_item_id
        )
        assert (
            progress_store.get_section_status(section_id, list_item_id)
            == CompletionStatus.IN_PROGRESS
        )
