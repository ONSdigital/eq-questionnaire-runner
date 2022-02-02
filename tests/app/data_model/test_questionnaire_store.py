import pytest

from app.data_models import QuestionnaireStore
from app.data_models.answer_store import AnswerStore
from app.data_models.progress_store import ProgressStore
from app.utilities.json import json_dumps, json_loads


@pytest.mark.parametrize(
    "extra_basic_input",
    ({}, {"NOT_A_LEGAL_TOP_LEVEL_KEY": "woop_woop_thats_the_sound_of_the_police"}),
)
def test_questionnaire_store_json_loads(
    questionnaire_store, basic_input, extra_basic_input
):
    basic_input.update(extra_basic_input)
    # Given
    questionnaire_store.input_data = json_dumps(basic_input)
    # When
    store = QuestionnaireStore(questionnaire_store.storage)
    # Then
    assert store.metadata.copy() == basic_input["METADATA"]
    assert store.response_metadata == basic_input["RESPONSE_METADATA"]
    assert store.answer_store == AnswerStore(basic_input["ANSWERS"])
    assert not hasattr(store, "NOT_A_LEGAL_TOP_LEVEL_KEY")
    assert not hasattr(store, "not_a_legal_top_level_key")

    expected_completed_block_ids = basic_input["PROGRESS"][0]["block_ids"][0]

    assert (
        len(store.progress_store.get_completed_block_ids("a-test-section", "abc123"))
        == 1
    )
    assert (
        store.progress_store.get_completed_block_ids("a-test-section", "abc123")[0]
        == expected_completed_block_ids
    )


def test_questionnaire_store_missing_keys(questionnaire_store, basic_input):
    # Given
    del basic_input["PROGRESS"]
    questionnaire_store.input_data = json_dumps(basic_input)
    # When
    store = QuestionnaireStore(questionnaire_store.storage)
    # Then
    assert store.metadata.copy() == basic_input["METADATA"]
    assert store.response_metadata == basic_input["RESPONSE_METADATA"]
    assert store.answer_store == AnswerStore(basic_input["ANSWERS"])
    assert not store.progress_store.serialize()


def test_questionnaire_store_updates_storage(questionnaire_store, basic_input):
    # Given
    store = QuestionnaireStore(questionnaire_store.storage)
    store.set_metadata(basic_input["METADATA"])
    store.answer_store = AnswerStore(basic_input["ANSWERS"])
    store.response_metadata = basic_input["RESPONSE_METADATA"]
    store.progress_store = ProgressStore(basic_input["PROGRESS"])

    # When
    store.save()

    # Then
    assert basic_input == json_loads(questionnaire_store.output_data)


def test_questionnaire_store_errors_on_invalid_object(questionnaire_store, basic_input):
    # Given
    class NotSerializable:
        pass

    non_serializable_metadata = {"test": NotSerializable()}

    store = QuestionnaireStore(questionnaire_store.storage)
    store.set_metadata(non_serializable_metadata)
    store.response_metadata = basic_input["RESPONSE_METADATA"]
    store.answer_store = AnswerStore(basic_input["ANSWERS"])
    store.progress_store = ProgressStore(basic_input["PROGRESS"])

    # When / Then
    with pytest.raises(TypeError):
        store.save()


def test_questionnaire_store_deletes(questionnaire_store, basic_input):
    # Given
    store = QuestionnaireStore(questionnaire_store.storage)
    store.set_metadata(basic_input["METADATA"])
    store.response_metadata = basic_input["RESPONSE_METADATA"]
    store.answer_store = AnswerStore(basic_input["ANSWERS"])
    store.progress_store = ProgressStore(basic_input["PROGRESS"])

    # When
    store.delete()

    # Then
    assert "a-test-section" not in store.progress_store
    assert store.metadata.copy() == {}
    assert len(store.answer_store) == 0
    assert store.response_metadata == {}


def test_questionnaire_store_raises_when_writing_to_metadata(questionnaire_store):
    store = QuestionnaireStore(questionnaire_store.storage)

    with pytest.raises(TypeError):
        store.metadata["no"] = "writing"
