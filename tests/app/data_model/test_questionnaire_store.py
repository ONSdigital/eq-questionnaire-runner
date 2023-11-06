import pytest

from app.data_models import QuestionnaireStore
from app.data_models.answer_store import AnswerStore
from app.data_models.metadata_proxy import MetadataProxy
from app.data_models.progress_store import ProgressStore
from app.data_models.supplementary_data_store import SupplementaryDataStore
from app.questionnaire.location import SectionKey
from app.utilities.json import json_dumps, json_loads
from app.utilities.make_immutable import make_immutable


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
    assert store.stores.metadata == MetadataProxy.from_dict(basic_input["METADATA"])
    assert store.stores.response_metadata == basic_input["RESPONSE_METADATA"]
    assert store.stores.answer_store == AnswerStore(basic_input["ANSWERS"])
    assert not hasattr(store, "NOT_A_LEGAL_TOP_LEVEL_KEY")
    assert not hasattr(store, "not_a_legal_top_level_key")

    expected_completed_block_ids = basic_input["PROGRESS"][0]["block_ids"][0]

    assert (
        len(
            store.stores.progress_store.get_completed_block_ids(
                SectionKey("a-test-section", "abc123")
            )
        )
        == 1
    )
    assert (
        store.stores.progress_store.get_completed_block_ids(
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
    # Then
    assert store.stores.metadata == MetadataProxy.from_dict(basic_input["METADATA"])
    assert store.stores.response_metadata == basic_input["RESPONSE_METADATA"]
    assert store.stores.answer_store == AnswerStore(basic_input["ANSWERS"])
    assert not store.stores.progress_store.serialize()


def test_questionnaire_store_updates_storage(questionnaire_store, basic_input):
    # Given
    store = QuestionnaireStore(questionnaire_store.storage)
    store.set_metadata(basic_input["METADATA"])
    store.stores.answer_store = AnswerStore(basic_input["ANSWERS"])
    store.stores.response_metadata = basic_input["RESPONSE_METADATA"]
    store.stores.progress_store = ProgressStore(basic_input["PROGRESS"])
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
    store.stores.response_metadata = basic_input["RESPONSE_METADATA"]
    store.stores.answer_store = AnswerStore(basic_input["ANSWERS"])
    store.stores.progress_store = ProgressStore(basic_input["PROGRESS"])

    # When / Then
    with pytest.raises(TypeError):
        store.save()


def test_questionnaire_store_deletes(questionnaire_store, basic_input):
    # Given
    store = QuestionnaireStore(questionnaire_store.storage)
    store.set_metadata(basic_input["METADATA"])
    store.stores.response_metadata = basic_input["RESPONSE_METADATA"]
    store.stores.answer_store = AnswerStore(basic_input["ANSWERS"])
    store.stores.progress_store = ProgressStore(basic_input["PROGRESS"])

    # When
    store.delete()

    # Then
    assert "a-test-section" not in store.stores.progress_store
    assert len(store.stores.answer_store) == 0
    assert store.stores.response_metadata == {}


def test_questionnaire_store_raises_when_writing_to_metadata(questionnaire_store):
    store = QuestionnaireStore(questionnaire_store.storage)

    with pytest.raises(TypeError):
        store.stores.metadata["no"] = "writing"


class TestQuestionnaireStoreWithSupplementaryData:
    store: QuestionnaireStore

    def assert_list_store_data(self, list_name: str, list_item_ids: list[str]):
        """Helper function to check that ListStore contains the given list with matching list_item_ids"""
        lists = [list_model.name for list_model in self.store.stores.list_store]
        assert list_name in lists
        assert self.store.stores.list_store[list_name].items == list_item_ids

    def test_adding_new_supplementary_data(
        self, questionnaire_store, supplementary_data
    ):
        """Tests that adding supplementary data adds supplementary list items to the list store
        this test doesn't mock list item ids, and checks that they match those in list_mappings
        """
        self.store = QuestionnaireStore(questionnaire_store.storage)
        self.store.set_supplementary_data(supplementary_data)
        assert "products" in self.store.stores.supplementary_data_store.list_lookup
        supplementary_list_item_ids = list(
            self.store.stores.supplementary_data_store.list_lookup["products"].values()
        )
        # check list mapping ids match list store ids
        self.assert_list_store_data("products", supplementary_list_item_ids)

    def test_updating_supplementary_data(
        self, questionnaire_store_with_supplementary_data, supplementary_data
    ):
        """Test that overwriting supplementary data with additional lists/items adds them to the list store
        without duplicating any existing data"""
        self.store = questionnaire_store_with_supplementary_data

        supplementary_data["items"]["supermarkets"] = [{"identifier": "54321"}]
        supplementary_data["items"]["products"].append({"identifier": "12345"})
        self.store.set_supplementary_data(supplementary_data)

        assert (
            self.store.stores.supplementary_data_store.list_mappings
            == make_immutable(
                {
                    "products": [
                        {"identifier": 89929001, "list_item_id": "item-1"},
                        {"identifier": "201630601", "list_item_id": "item-2"},
                        {"identifier": "12345", "list_item_id": "item-3"},
                    ],
                    "supermarkets": [
                        {"identifier": "54321", "list_item_id": "item-4"},
                    ],
                }
            )
        )

        self.assert_list_store_data("products", ["item-1", "item-2", "item-3"])
        self.assert_list_store_data("supermarkets", ["item-4"])

    def test_removing_some_supplementary_data(
        self, questionnaire_store_with_supplementary_data, supplementary_data
    ):
        """Tests that if you overwrite existing supplementary data with data that is missing list item ids
        or lists, that the list store is updated to remove that data"""
        self.store = questionnaire_store_with_supplementary_data

        del supplementary_data["items"]["products"][0]
        self.store.set_supplementary_data(supplementary_data)

        # products item-1 should be gone
        self.assert_list_store_data("products", ["item-2"])

    def test_removing_all_supplementary_data(
        self, questionnaire_store_with_supplementary_data
    ):
        """Checks that removing all supplementary data clears out the list store"""
        self.store = questionnaire_store_with_supplementary_data
        self.store.set_supplementary_data({})
        assert len(list(self.store.stores.list_store)) == 0

    def test_removing_supplementary_lists_with_answers(
        self, questionnaire_store_with_supplementary_data, supplementary_data
    ):
        """Tests that if you overwrite supplementary data,
        related answers for old list/list_item_ids are removed from the answer store"""
        self.store = questionnaire_store_with_supplementary_data

        # add some answers for the supplementary list items
        self.store.stores.answer_store = AnswerStore(
            [
                {
                    "answer_id": "product-sales-answer",
                    "value": "100",
                    "list_item_id": "item-1",
                },
                {
                    "answer_id": "product-sales-answer",
                    "value": "200",
                    "list_item_id": "item-2",
                },
            ]
        )

        # delete the first product and update supplementary data
        del supplementary_data["items"]["products"][0]
        self.store.set_supplementary_data(supplementary_data)

        # item-1 should be gone
        self.assert_list_store_data("products", ["item-2"])
        # the answer for it should be too
        answers = list(self.store.stores.answer_store.answer_map.keys())
        assert len(answers) == 1
        assert answers[0] == ("product-sales-answer", "item-2")

        # remove all answers
        self.store.set_supplementary_data({})
        assert not self.store.stores.answer_store.answer_map

    def test_removing_supplementary_data_ignores_non_supplementary_data(
        self, questionnaire_store_with_supplementary_data
    ):
        """Tests that removing supplementary data does not affect other lists and answers"""
        self.store = questionnaire_store_with_supplementary_data
        # unrelated
        self.store.stores.answer_store = AnswerStore(
            [
                {
                    "answer_id": "unrelated-answer",
                    "value": "100",
                    "list_item_id": "JxSW21",
                },
                {
                    "answer_id": "sales",
                    "value": "200",
                },
            ]
        )
        self.store.stores.list_store.add_list_item("supermarkets")
        self.assert_list_store_data("products", ["item-1", "item-2"])
        self.assert_list_store_data("supermarkets", ["item-3"])

        self.store.set_supplementary_data({})
        self.assert_list_store_data("supermarkets", ["item-3"])
        answers = list(self.store.stores.answer_store.answer_map.keys())
        assert answers == [("unrelated-answer", "JxSW21"), ("sales", None)]
