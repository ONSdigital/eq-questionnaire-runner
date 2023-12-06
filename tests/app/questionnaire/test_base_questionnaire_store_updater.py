# pylint: disable=redefined-outer-name
import pytest
from mock import MagicMock, Mock

from app.data_models import AnswerStore, ListStore, ProgressStore, QuestionnaireStore
from app.data_models.progress import CompletionStatus, ProgressDict
from app.questionnaire.questionnaire_store_updater import QuestionnaireStoreUpdaterBase
from app.utilities.make_immutable import make_immutable
from app.utilities.types import DependentSection, SectionKey


@pytest.fixture
def questionnaire_store_with_supplementary_data(
    fake_questionnaire_store, supplementary_data_store_with_data
):
    fake_questionnaire_store.data_stores.supplementary_data_store = (
        supplementary_data_store_with_data
    )
    fake_questionnaire_store.data_stores.list_store = ListStore(
        [{"items": ["item-1", "item-2"], "name": "products"}]
    )
    # Mock the identifier generation in list store so the ids are item-1, item-2, ...
    # pylint: disable=protected-access
    fake_questionnaire_store.data_stores.list_store._generate_identifier = Mock(
        side_effect=(f"item-{i}" for i in range(3, 100))
    )
    return fake_questionnaire_store


@pytest.fixture
def questionnaire_store_with_employee_supplementary_data(
    fake_questionnaire_store,
    supplementary_data_store_with_employees,
):
    """Mock questionnaire store with supplementary data of two products and partial progress"""
    fake_questionnaire_store.data_stores.supplementary_data_store = (
        supplementary_data_store_with_employees
    )
    fake_questionnaire_store.data_stores.list_store = ListStore(
        [
            {"items": ["item-1", "item-2"], "name": "products"},
            {
                "items": ["employee-1", "employee-2", "employee-3", "employee-4"],
                "name": "employees",
            },
        ],
    )
    fake_questionnaire_store.data_stores.progress_store = ProgressStore(
        [
            ProgressDict(
                section_id="introduction-section",
                block_ids=["loaded-successfully-block", "introduction-block"],
                status=CompletionStatus.COMPLETED,
            ),
            ProgressDict(
                section_id="section-2",
                block_ids=["list-collector-employees"],
                status=CompletionStatus.COMPLETED,
            ),
            ProgressDict(
                section_id="section-3",
                block_ids=["any-additional-employees"],
                status=CompletionStatus.COMPLETED,
            ),
            ProgressDict(
                section_id="section-4",
                block_ids=["length-of-employment"],
                list_item_id="employee-1",
                status=CompletionStatus.COMPLETED,
            ),
            ProgressDict(
                section_id="section-4",
                block_ids=["length-of-employment"],
                list_item_id="employee-2",
                status=CompletionStatus.COMPLETED,
            ),
            ProgressDict(
                section_id="section-6",
                block_ids=["product-repeating-block-1"],
                status=CompletionStatus.COMPLETED,
                list_item_id="item-1",
            ),
            ProgressDict(
                section_id="section-6",
                block_ids=["product-repeating-block-1"],
                status=CompletionStatus.COMPLETED,
                list_item_id="item-2",
            ),
            ProgressDict(
                section_id="section-6",
                block_ids=[
                    "list-collector-products",
                    "calculated-summary-volume-sales",
                    "calculated-summary-volume-total",
                    "dynamic-products",
                    "calculated-summary-value-sales",
                ],
                status=CompletionStatus.COMPLETED,
            ),
            ProgressDict(
                section_id="section-8",
                block_ids=["product-volume-interstitial"],
                status=CompletionStatus.COMPLETED,
            ),
        ]
    )
    # Mock the identifier generation in list store so the ids are item-1, item-2, ...
    # pylint: disable=protected-access
    fake_questionnaire_store.data_stores.list_store._generate_identifier = Mock(
        side_effect=(f"item-{i}" for i in range(3, 100))
    )
    return fake_questionnaire_store


def test_removing_list_item_data(
    supplementary_data_schema, questionnaire_store_with_employee_supplementary_data
):
    """
    Tests that if you remove list item data with the base updater
    it removes the list item from the list store and removes the progress for any dependents of the list item
    """
    base_questionnaire_store_updater = QuestionnaireStoreUpdaterBase(
        schema=supplementary_data_schema,
        questionnaire_store=questionnaire_store_with_employee_supplementary_data,
        router=MagicMock(),
    )
    base_questionnaire_store_updater.remove_list_item_data("products", "item-2")
    base_questionnaire_store_updater.capture_dependencies_for_list_change("products")

    assert questionnaire_store_with_employee_supplementary_data.data_stores.list_store[
        "products"
    ].items == ["item-1"]
    # should not contain item-1 since this should be unaffected
    assert base_questionnaire_store_updater.dependent_sections == {
        DependentSection(section_id="section-6", list_item_id=None),
        DependentSection(section_id="section-8", list_item_id=None),
    }
    # this should affect all blocks in section-6
    assert base_questionnaire_store_updater.dependent_block_id_by_section_key == {
        SectionKey(section_id="section-6", list_item_id=None): {
            "list-collector-products",
            "calculated-summary-value-sales",
            "dynamic-products",
            "calculated-summary-volume-sales",
            "calculated-summary-volume-total",
        },
    }


@pytest.mark.parametrize(
    "section_id,list_item_id,dependent_blocks,expected_blocks",
    [
        (
            "section-6",
            None,
            {
                "calculated-summary-volume-sales",
                "calculated-summary-volume-total",
            },
            [
                "list-collector-products",
                "dynamic-products",
                "calculated-summary-value-sales",
            ],
        ),
        (
            "section-6",
            None,
            {
                "list-collector-products",
                "calculated-summary-value-sales",
                "dynamic-products",
                "calculated-summary-volume-sales",
                "calculated-summary-volume-total",
            },
            [],
        ),
        (
            "section-6",
            "item-1",
            {"product-repeating-block-1"},
            [],
        ),
        (
            "section-8",
            None,
            {"product-volume-interstitial"},
            [],
        ),
    ],
)
def test_remove_dependent_blocks_and_capture_dependent_sections(
    supplementary_data_schema,
    questionnaire_store_with_employee_supplementary_data,
    section_id,
    list_item_id,
    dependent_blocks,
    expected_blocks,
):
    """
    Tests that the progress store is successfully updated when removing captured dependencies
    and that the dependent sections are captured correctly
    """
    base_questionnaire_store_updater = QuestionnaireStoreUpdaterBase(
        schema=supplementary_data_schema,
        questionnaire_store=questionnaire_store_with_employee_supplementary_data,
        router=MagicMock(),
    )
    section_key = SectionKey(section_id=section_id, list_item_id=list_item_id)
    base_questionnaire_store_updater.dependent_block_id_by_section_key = {
        section_key: dependent_blocks,
    }
    base_questionnaire_store_updater.remove_dependent_blocks_and_capture_dependent_sections()
    assert (
        base_questionnaire_store_updater._progress_store._progress[  # pylint: disable=protected-access
            section_key
        ].block_ids
        == expected_blocks
    )
    assert base_questionnaire_store_updater.dependent_sections == {
        DependentSection(
            section_id=section_id, list_item_id=list_item_id, is_complete=False
        )
    }


@pytest.mark.parametrize(
    "section_id, list_item_id",
    [("section-6", None), ("section-6", "item-1"), ("section-8", None)],
)
def test_update_progress_for_dependent_sections(
    supplementary_data_schema,
    questionnaire_store_with_employee_supplementary_data,
    section_id,
    list_item_id,
):
    """
    Tests that captured dependent sections get set back to in progress
    """
    base_questionnaire_store_updater = QuestionnaireStoreUpdaterBase(
        schema=supplementary_data_schema,
        questionnaire_store=questionnaire_store_with_employee_supplementary_data,
        router=MagicMock(),
    )
    base_questionnaire_store_updater.dependent_sections = {
        dependent_section := DependentSection(
            section_id=section_id, list_item_id=list_item_id, is_complete=False
        )
    }
    base_questionnaire_store_updater.update_progress_for_dependent_sections()
    assert (
        base_questionnaire_store_updater._progress_store._progress[  # pylint: disable=protected-access
            dependent_section.section_key
        ].status
        == CompletionStatus.IN_PROGRESS
    )


def test_update_progress_of_repeating_dependent(
    supplementary_data_schema,
    questionnaire_store_with_employee_supplementary_data,
):
    """
    Tests that when a data change unlocks a new question within a repeating section
    Each repeating section which has been started is captured
    """
    base_questionnaire_store_updater = QuestionnaireStoreUpdaterBase(
        schema=supplementary_data_schema,
        questionnaire_store=questionnaire_store_with_employee_supplementary_data,
        router=MagicMock(),
    )
    base_questionnaire_store_updater.remove_list_item_data("employees", "employee-4")
    base_questionnaire_store_updater.capture_dependencies_for_list_change("employees")
    # employee-3 not affected as section had not yet been started
    assert base_questionnaire_store_updater.dependent_sections == {
        DependentSection(section_id="section-2"),
        DependentSection(section_id="section-4", list_item_id="employee-1"),
        DependentSection(section_id="section-4", list_item_id="employee-2"),
    }


class TestSettingSupplementaryData:
    store: QuestionnaireStore

    def get_questionnaire_store_updater_base(self):
        return QuestionnaireStoreUpdaterBase(
            schema=MagicMock(),
            questionnaire_store=self.store,
            router=MagicMock(),
        )

    def assert_list_store_data(self, list_name: str, list_item_ids: list[str]):
        """Helper function to check that ListStore contains the given list with matching list_item_ids"""
        lists = [list_model.name for list_model in self.store.data_stores.list_store]
        assert list_name in lists
        assert self.store.data_stores.list_store[list_name].items == list_item_ids

    def test_adding_new_supplementary_data(
        self, fake_questionnaire_store, supplementary_data
    ):
        """Tests that adding supplementary data adds supplementary list items to the list store
        this test doesn't mock list item ids, and checks that they match those in list_mappings
        """
        self.store = fake_questionnaire_store
        questionnaire_store_updater_base = self.get_questionnaire_store_updater_base()
        questionnaire_store_updater_base.set_supplementary_data(supplementary_data)
        assert "products" in self.store.data_stores.supplementary_data_store.list_lookup
        supplementary_list_item_ids = list(
            self.store.data_stores.supplementary_data_store.list_lookup[
                "products"
            ].values()
        )
        # check list mapping ids match list store ids
        self.assert_list_store_data("products", supplementary_list_item_ids)

    def test_updating_supplementary_data(
        self, questionnaire_store_with_supplementary_data, supplementary_data
    ):
        """Test that overwriting supplementary data with additional lists/items adds them to the list store
        without duplicating any existing data"""
        self.store = questionnaire_store_with_supplementary_data
        questionnaire_store_updater_base = self.get_questionnaire_store_updater_base()

        supplementary_data["items"]["supermarkets"] = [{"identifier": "54321"}]
        supplementary_data["items"]["products"].append({"identifier": "12345"})
        questionnaire_store_updater_base.set_supplementary_data(supplementary_data)

        assert (
            self.store.data_stores.supplementary_data_store.list_mappings
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
        questionnaire_store_updater_base = self.get_questionnaire_store_updater_base()

        del supplementary_data["items"]["products"][0]
        questionnaire_store_updater_base.set_supplementary_data(supplementary_data)

        # products item-1 should be gone
        self.assert_list_store_data("products", ["item-2"])

    def test_removing_all_supplementary_data(
        self, questionnaire_store_with_supplementary_data
    ):
        """Checks that removing all supplementary data clears out the list store"""
        self.store = questionnaire_store_with_supplementary_data
        questionnaire_store_updater_base = self.get_questionnaire_store_updater_base()
        questionnaire_store_updater_base.set_supplementary_data(to_set={})
        assert len(list(self.store.data_stores.list_store)) == 0

    def test_removing_supplementary_lists_with_answers(
        self, questionnaire_store_with_supplementary_data, supplementary_data
    ):
        """Tests that if you overwrite supplementary data,
        related answers for old list/list_item_ids are removed from the answer store"""
        self.store = questionnaire_store_with_supplementary_data
        # add some answers for the supplementary list items
        self.store.data_stores.answer_store = AnswerStore(
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
        questionnaire_store_updater_base = self.get_questionnaire_store_updater_base()

        # delete the first product and update supplementary data
        del supplementary_data["items"]["products"][0]
        questionnaire_store_updater_base.set_supplementary_data(supplementary_data)

        # item-1 should be gone
        self.assert_list_store_data("products", ["item-2"])
        # the answer for it should be too
        answers = list(self.store.data_stores.answer_store.answer_map.keys())
        assert len(answers) == 1
        assert answers[0] == ("product-sales-answer", "item-2")

        # remove all answers
        questionnaire_store_updater_base.set_supplementary_data({})
        assert not self.store.data_stores.answer_store.answer_map

    def test_removing_supplementary_data_ignores_non_supplementary_data(
        self, questionnaire_store_with_supplementary_data
    ):
        """Tests that removing supplementary data does not affect other lists and answers"""
        self.store = questionnaire_store_with_supplementary_data
        questionnaire_store_updater_base = self.get_questionnaire_store_updater_base()
        # unrelated
        self.store.data_stores.answer_store = AnswerStore(
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
        self.store.data_stores.list_store.add_list_item("supermarkets")
        self.assert_list_store_data("products", ["item-1", "item-2"])
        self.assert_list_store_data("supermarkets", ["item-3"])

        questionnaire_store_updater_base.set_supplementary_data({})
        self.assert_list_store_data("supermarkets", ["item-3"])
        answers = list(self.store.data_stores.answer_store.answer_map.keys())
        assert answers == [("unrelated-answer", "JxSW21"), ("sales", None)]
