from werkzeug.datastructures import MultiDict

from app.data_models import QuestionnaireStore
from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress_store import ProgressStore
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_store_updater import QuestionnaireStoreUpdater


def test_save_answers_with_form_data(
    mock_location,
    schema,
    mock_answer_store,
    questionnaire_store,
):
    answer_id = "answer"
    answer_value = "1000"

    schema.get_answer_ids_for_question.return_value = [answer_id]

    form_data = {answer_id: answer_value}

    current_question = schema.get_block(mock_location.block_id)["question"]
    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, schema, questionnaire_store, current_question
    )
    questionnaire_store_updater.update_answers(form_data)

    assert mock_answer_store.add_or_update.call_count == 1

    created_answer = mock_answer_store.add_or_update.call_args[0][0]
    assert created_answer.__dict__ == {
        "answer_id": answer_id,
        "list_item_id": None,
        "value": answer_value,
    }


def test_save_empty_answer_removes_existing_answer(
    schema,
    mock_answer_store,
    questionnaire_store,
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

    schema.get_answer_ids_for_question.return_value = [answer_id]

    form_data = MultiDict({answer_id: answer_value})

    current_question = schema.get_block(location.block_id)["question"]
    questionnaire_store_updater = QuestionnaireStoreUpdater(
        location, schema, questionnaire_store, current_question
    )
    questionnaire_store_updater.update_answers(form_data)

    assert mock_answer_store.add_or_update.call_count == 1

    created_answer = mock_answer_store.add_or_update.call_args[0][0]
    assert created_answer.__dict__ == {
        "answer_id": answer_id,
        "list_item_id": "abc123",
        "value": answer_value,
    }

    form_data = MultiDict({answer_id: ""})
    questionnaire_store_updater.update_answers(form_data)

    assert mock_answer_store.remove_answer.call_count == 1
    answer_key = mock_answer_store.remove_answer.call_args[0]
    assert answer_key == (answer_id, list_item_id)


def test_default_answers_are_not_saved(
    mock_location,
    schema,
    mock_answer_store,
    questionnaire_store,
):
    answer_id = "answer"
    default_value = 0

    schema.get_answer_ids_for_question.return_value = [answer_id]
    schema.get_answers_by_answer_id.return_value = [{"default": default_value}]

    # No answer given so will use schema defined default
    form_data = MultiDict({answer_id: None})

    current_question = {"answers": [{"id": "answer", "default": default_value}]}
    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, schema, questionnaire_store, current_question
    )
    questionnaire_store_updater.update_answers(form_data)

    assert mock_answer_store.add_or_update.call_count == 0


def test_empty_answers(
    mock_location,
    schema,
    mock_answer_store,
    questionnaire_store,
):
    string_answer_id = "string-answer"
    checkbox_answer_id = "checkbox-answer"
    radio_answer_id = "radio-answer"

    schema.get_answer_ids_for_question.return_value = [
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
        mock_location, schema, questionnaire_store, current_question
    )
    questionnaire_store_updater.update_answers(form_data)

    assert mock_answer_store.add_or_update.call_count == 0


def test_remove_all_answers_with_list_item_id(
    mock_location, schema, mock_answer_store, list_store, questionnaire_store, mocker
):
    mock_answer_store = AnswerStore(
        existing_answers=[
            {"answer_id": "test1", "value": 1, "list_item_id": "abcdef"},
            {"answer_id": "test2", "value": 2, "list_item_id": "abcdef"},
            {"answer_id": "test3", "value": 3, "list_item_id": "uvwxyz"},
        ]
    )

    questionnaire_store = mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        answer_store=mock_answer_store,
        list_store=list_store(spec=ListStore),
        progress_store=ProgressStore(),
    )

    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, schema, questionnaire_store, None
    )
    questionnaire_store_updater.remove_list_item_and_answers("abc", "abcdef")

    assert len(mock_answer_store) == 1
    assert mock_answer_store.get_answer("test3", "uvwxyz")


def test_remove_primary_person(
    mock_location,
    schema,
    mock_answer_store,
    questionnaire_store,
    mock_list_store,
    mocker,
):
    mock_answer_store = AnswerStore(
        existing_answers=[
            {"answer_id": "test1", "value": 1, "list_item_id": "abcdef"},
            {"answer_id": "test2", "value": 2, "list_item_id": "abcdef"},
            {"answer_id": "test3", "value": 3, "list_item_id": "xyzabc"},
        ]
    )

    questionnaire_store = mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        answer_store=mock_answer_store,
        list_store=mock_list_store,
        progress_store=ProgressStore(),
    )

    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, schema, questionnaire_store, None
    )

    questionnaire_store_updater.remove_primary_person("people")


def test_add_primary_person(
    mock_location,
    schema,
    mock_answer_store,
    questionnaire_store,
    mock_list_store,
    mocker,
):

    questionnaire_store = mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        answer_store=mock_answer_store,
        list_store=mock_list_store,
        progress_store=ProgressStore(),
    )

    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, schema, questionnaire_store, None
    )
    questionnaire_store_updater.add_primary_person("people")


def test_remove_completed_relationship_locations_for_list_name(
    mock_location,
    schema,
    mock_answer_store,
    progress_store,
    questionnaire_store,
    mock_list_store,
    mocker,
):
    progress_store.add_completed_location(
        "section",
        Location(section_id="section", block_id="test-relationship-collector"),
    )
    questionnaire_store = mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        answer_store=mock_answer_store,
        list_store=mock_list_store,
        progress_store=progress_store,
    )
    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, schema, questionnaire_store, None
    )

    patch_method = "app.questionnaire.questionnaire_store_updater.QuestionnaireStoreUpdater._get_relationship_collectors_by_list_name"
    patched = mocker.patch(patch_method)
    patched.return_value = [{"id": "test-relationship-collector"}]
    questionnaire_store_updater.remove_completed_relationship_locations_for_list_name(
        "test-relationship-collector"
    )

    completed = progress_store.serialize()
    assert len(completed) == 0


def test_remove_completed_relationship_locations_for_list_name_no_locations(
    mock_location,
    schema,
    mock_answer_store,
    progress_store,
    questionnaire_store,
    mock_list_store,
    mocker,
):
    progress_store.add_completed_location(
        "section",
        Location(section_id="section", block_id="test-relationship-collector"),
    )
    initial_progress_store = progress_store.serialize()
    questionnaire_store = mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        answer_store=mock_answer_store,
        list_store=mock_list_store,
        progress_store=progress_store,
    )
    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, schema, questionnaire_store, None
    )

    patch_method = "app.questionnaire.questionnaire_store_updater.QuestionnaireStoreUpdater._get_relationship_collectors_by_list_name"
    patched = mocker.patch(patch_method)
    patched.return_value = None
    questionnaire_store_updater.remove_completed_relationship_locations_for_list_name(
        "test-relationship-collector"
    )

    assert progress_store.serialize() == initial_progress_store


def test_update_relationship_question_completeness_no_relationship_collectors(
    mock_location,
    schema,
    mock_answer_store,
    progress_store,
    questionnaire_store,
    mock_list_store,
    mocker,
):
    questionnaire_store = mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        answer_store=mock_answer_store,
        list_store=mock_list_store,
        progress_store=progress_store,
    )
    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, schema, questionnaire_store, None
    )

    patch_method = "app.questionnaire.questionnaire_store_updater.QuestionnaireStoreUpdater._get_relationship_collectors_by_list_name"
    patched = mocker.patch(patch_method)
    patched.return_value = None
    assert (
        questionnaire_store_updater.update_relationship_question_completeness(
            "test-relationship-collector"
        )
        is None
    )


def test_update_same_name_items(
    mock_location,
    schema,
    mock_answer_store,
    questionnaire_store,
    mock_list_store,
    mocker,
):
    mock_answer_store = AnswerStore(
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

    questionnaire_store = mocker.MagicMock(
        spec=QuestionnaireStore,
        completed_blocks=[],
        answer_store=mock_answer_store,
        list_store=mock_list_store,
        progress_store=ProgressStore(),
    )

    questionnaire_store_updater = QuestionnaireStoreUpdater(
        mock_location, schema, questionnaire_store, None
    )

    questionnaire_store_updater.update_same_name_items(
        "people", ["first-name", "last-name"]
    )

    assert "abcdef" in mock_list_store["people"].same_name_items
    assert "ghijkl" in mock_list_store["people"].same_name_items
