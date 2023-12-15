import pytest

from app.data_models.answer_store import AnswerStore
from app.data_models.metadata_proxy import MetadataProxy
from app.data_models.progress_store import ProgressStore
from app.data_models.questionnaire_store import QuestionnaireStore
from app.data_models.supplementary_data_store import SupplementaryDataStore
from app.questionnaire.location import SectionKey
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
    data_stores = store.data_stores
    # Then
    assert data_stores.metadata == MetadataProxy.from_dict(basic_input["METADATA"])
    assert data_stores.response_metadata == basic_input["RESPONSE_METADATA"]
    assert data_stores.answer_store == AnswerStore(basic_input["ANSWERS"])
    assert not hasattr(store, "NOT_A_LEGAL_TOP_LEVEL_KEY")
    assert not hasattr(store, "not_a_legal_top_level_key")

    expected_completed_block_ids = basic_input["PROGRESS"][0]["block_ids"][0]

    assert (
        len(
            data_stores.progress_store.get_completed_block_ids(
                SectionKey("a-test-section", "abc123")
            )
        )
        == 1
    )
    assert (
        data_stores.progress_store.get_completed_block_ids(
            SectionKey("a-test-section", "abc123")
        )[0]
        == expected_completed_block_ids
    )


def test_questionnaire_store_missing_keys(questionnaire_store, basic_input):
    # Given
    del basic_input["PROGRESS"]
    questionnaire_store.input_data = json_dumps(basic_input)
    # When
    store = QuestionnaireStore(questionnaire_store.storage)
    data_stores = store.data_stores
    # Then
    assert data_stores.metadata == MetadataProxy.from_dict(basic_input["METADATA"])
    assert data_stores.response_metadata == basic_input["RESPONSE_METADATA"]
    assert data_stores.answer_store == AnswerStore(basic_input["ANSWERS"])
    assert not data_stores.progress_store.serialize()


def test_questionnaire_store_updates_storage(questionnaire_store, basic_input):
    # Given
    store = QuestionnaireStore(questionnaire_store.storage)
    data_stores = store.data_stores
    store.set_metadata(basic_input["METADATA"])
    data_stores.answer_store = AnswerStore(basic_input["ANSWERS"])
    data_stores.response_metadata = basic_input["RESPONSE_METADATA"]
    data_stores.progress_store = ProgressStore(basic_input["PROGRESS"])
    store.supplementary_data_store = SupplementaryDataStore.deserialize(
        basic_input["SUPPLEMENTARY_DATA"]
    )

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
    data_stores = store.data_stores
    data_stores.response_metadata = basic_input["RESPONSE_METADATA"]
    data_stores.answer_store = AnswerStore(basic_input["ANSWERS"])
    data_stores.progress_store = ProgressStore(basic_input["PROGRESS"])

    # When / Then
    with pytest.raises(TypeError):
        store.save()


def test_questionnaire_store_deletes(questionnaire_store, basic_input):
    # Given
    store = QuestionnaireStore(questionnaire_store.storage)
    store.set_metadata(basic_input["METADATA"])
    data_stores = store.data_stores
    data_stores.response_metadata = basic_input["RESPONSE_METADATA"]
    data_stores.answer_store = AnswerStore(basic_input["ANSWERS"])
    data_stores.progress_store = ProgressStore(basic_input["PROGRESS"])

    # When
    store.delete()

    # Then
    assert "a-test-section" not in data_stores.progress_store
    assert len(data_stores.answer_store) == 0
    assert data_stores.response_metadata == {}


def test_questionnaire_store_raises_when_writing_to_metadata(questionnaire_store):
    store = QuestionnaireStore(questionnaire_store.storage)

    with pytest.raises(TypeError):
        store.data_stores.metadata["no"] = "writing"
