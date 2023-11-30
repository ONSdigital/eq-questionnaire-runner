# pylint: disable=redefined-outer-name
import pytest
from mock import MagicMock

from app.data_models import ListStore, ProgressStore
from app.data_models.progress import CompletionStatus, ProgressDict
from app.questionnaire.questionnaire_store_updater import BaseQuestionnaireStoreUpdater
from app.utilities.types import DependentSection, SectionKey


@pytest.fixture
def questionnaire_store_with_supplementary_data(
    mock_questionnaire_store,
    supplementary_data_store_with_employees,
):
    """Mock questionnaire store with supplementary data of two products and partial progress"""
    mock_questionnaire_store.data_stores.supplementary_data_store = (
        supplementary_data_store_with_employees
    )
    mock_questionnaire_store.data_stores.list_store = ListStore(
        [
            {"items": ["item-1", "item-2"], "name": "products"},
            {
                "items": ["employee-1", "employee-2", "employee-3", "employee-4"],
                "name": "employees",
            },
        ],
    )
    mock_questionnaire_store.data_stores.progress_store = ProgressStore(
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
    return mock_questionnaire_store


def test_removing_list_item_data(
    supplementary_data_schema, questionnaire_store_with_supplementary_data
):
    """
    Tests that if you remove list item data with the base updater
    it removes the list item from the list store and removes the progress for any dependents of the list item
    """
    base_questionnaire_store_updater = BaseQuestionnaireStoreUpdater(
        schema=supplementary_data_schema,
        questionnaire_store=questionnaire_store_with_supplementary_data,
        router=MagicMock(),
    )
    base_questionnaire_store_updater.remove_list_item_data("products", "item-2")
    base_questionnaire_store_updater.capture_dependencies_for_list_change("products")

    assert questionnaire_store_with_supplementary_data.data_stores.list_store[
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
    questionnaire_store_with_supplementary_data,
    section_id,
    list_item_id,
    dependent_blocks,
    expected_blocks,
):
    """
    Tests that the progress store is successfully updated when removing captured dependencies
    and that the dependent sections are captured correctly
    """
    base_questionnaire_store_updater = BaseQuestionnaireStoreUpdater(
        schema=supplementary_data_schema,
        questionnaire_store=questionnaire_store_with_supplementary_data,
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
    questionnaire_store_with_supplementary_data,
    section_id,
    list_item_id,
):
    """
    Tests that captured dependent sections get set back to in progress
    """
    base_questionnaire_store_updater = BaseQuestionnaireStoreUpdater(
        schema=supplementary_data_schema,
        questionnaire_store=questionnaire_store_with_supplementary_data,
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
    questionnaire_store_with_supplementary_data,
):
    """
    Tests that when a data change unlocks a new question within a repeating section
    Each repeating section which has been started is captured
    """
    base_questionnaire_store_updater = BaseQuestionnaireStoreUpdater(
        schema=supplementary_data_schema,
        questionnaire_store=questionnaire_store_with_supplementary_data,
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
