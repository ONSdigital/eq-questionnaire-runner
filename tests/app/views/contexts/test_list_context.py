import pytest

from app.data_models import CompletionStatus, ProgressStore
from app.data_models.data_stores import DataStores
from app.data_models.progress import ProgressDict
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.utilities.schema import load_schema_from_name
from app.views.contexts import ListContext


@pytest.mark.usefixtures("app")
def test_build_list_collector_context(
    list_collector_block,
    schema,
    people_answer_store,
    people_list_store,
):
    list_context = ListContext(
        DEFAULT_LANGUAGE_CODE,
        schema,
        DataStores(answer_store=people_answer_store, list_store=people_list_store),
    )

    list_context = list_context(
        list_collector_block["summary"],
        for_list="people",
        section_id="section-id",
        has_repeating_blocks=False,
    )

    assert all(keys in list_context["list"] for keys in ["list_items", "editable"])


@pytest.mark.usefixtures("app")
def test_build_list_summary_context_no_summary_block(
    schema,
    people_answer_store,
    people_list_store,
):
    list_context = ListContext(
        DEFAULT_LANGUAGE_CODE,
        schema,
        DataStores(answer_store=people_answer_store, list_store=people_list_store),
    )

    list_context = list_context(
        summary_definition=None,
        for_list="people",
        section_id="section-id",
        has_repeating_blocks=False,
    )
    assert list_context == {"list": {"editable": False, "list_items": []}}


@pytest.mark.usefixtures("app")
def test_build_list_summary_context(
    list_collector_block,
    people_answer_store,
    people_list_store,
):
    schema = load_schema_from_name("test_list_collector_primary_person")
    expected = [
        {
            "item_title": "Toni Morrison",
            "edit_link": "/questionnaire/people/PlwgoG/edit-person/",
            "remove_link": "/questionnaire/people/PlwgoG/remove-person/",
            "primary_person": False,
            "list_item_id": "PlwgoG",
            "is_complete": False,
            "repeating_blocks": False,
        },
        {
            "item_title": "Barry Pheloung",
            "edit_link": "/questionnaire/people/UHPLbX/edit-person/",
            "remove_link": "/questionnaire/people/UHPLbX/remove-person/",
            "primary_person": False,
            "list_item_id": "UHPLbX",
            "is_complete": False,
            "repeating_blocks": False,
        },
    ]

    list_context = ListContext(
        DEFAULT_LANGUAGE_CODE,
        schema,
        DataStores(answer_store=people_answer_store, list_store=people_list_store),
    )

    list_context = list_context(
        summary_definition=list_collector_block["summary"],
        for_list="people",
        section_id="section-id",
        has_repeating_blocks=False,
        edit_block_id=list_collector_block["edit_block"]["id"],
        remove_block_id=list_collector_block["remove_block"]["id"],
    )

    assert expected == list_context["list"]["list_items"]


@pytest.mark.usefixtures("app")
def test_assert_primary_person_string_appended(
    list_collector_block,
    people_answer_store,
    people_list_store,
):
    schema = load_schema_from_name("test_list_collector_primary_person")
    people_list_store["people"].primary_person = "PlwgoG"

    list_context = ListContext(
        language=DEFAULT_LANGUAGE_CODE,
        schema=schema,
        data_stores=DataStores(
            answer_store=people_answer_store, list_store=people_list_store
        ),
    )
    list_context = list_context(
        summary_definition=list_collector_block["summary"],
        for_list=list_collector_block["for_list"],
        section_id="section-id",
        has_repeating_blocks=False,
    )

    assert list_context["list"]["list_items"][0]["primary_person"] is True
    assert list_context["list"]["list_items"][0]["item_title"] == "Toni Morrison (You)"
    assert list_context["list"]["list_items"][1]["item_title"] == "Barry Pheloung"


@pytest.mark.usefixtures("app")
def test_for_list_item_ids(
    list_collector_block,
    people_answer_store,
    people_list_store,
):
    schema = load_schema_from_name("test_list_collector_primary_person")

    list_context = ListContext(
        language=DEFAULT_LANGUAGE_CODE,
        schema=schema,
        data_stores=DataStores(
            answer_store=people_answer_store, list_store=people_list_store
        ),
    )
    list_context = list_context(
        summary_definition=list_collector_block["summary"],
        for_list=list_collector_block["for_list"],
        for_list_item_ids=["UHPLbX"],
        section_id="section-id",
        has_repeating_blocks=False,
    )

    expected = [
        {
            "item_title": "Barry Pheloung",
            "primary_person": False,
            "is_complete": False,
            "repeating_blocks": False,
            "list_item_id": "UHPLbX",
        }
    ]

    assert expected == list_context["list"]["list_items"]


@pytest.mark.usefixtures("app")
def test_list_context_items_complete_without_repeating_blocks(
    people_answer_store,
    people_list_store,
    list_collector_block,
):
    schema = load_schema_from_name("test_list_collector_primary_person")
    expected = [
        {
            "item_title": "Toni Morrison",
            "edit_link": "/questionnaire/people/PlwgoG/edit-person/",
            "remove_link": "/questionnaire/people/PlwgoG/remove-person/",
            "primary_person": False,
            "list_item_id": "PlwgoG",
            "is_complete": True,
            "repeating_blocks": False,
        },
        {
            "item_title": "Barry Pheloung",
            "edit_link": "/questionnaire/people/UHPLbX/edit-person/",
            "remove_link": "/questionnaire/people/UHPLbX/remove-person/",
            "primary_person": False,
            "list_item_id": "UHPLbX",
            "is_complete": True,
            "repeating_blocks": False,
        },
    ]

    progress_store = ProgressStore(
        [
            ProgressDict(
                section_id="section-id",
                list_item_id="PlwgoG",
                status=CompletionStatus.COMPLETED,
                block_ids=[],
            ),
            ProgressDict(
                section_id="section-id",
                list_item_id="UHPLbX",
                status=CompletionStatus.COMPLETED,
                block_ids=[],
            ),
        ]
    )

    list_context = ListContext(
        DEFAULT_LANGUAGE_CODE,
        schema,
        data_stores=DataStores(
            answer_store=people_answer_store,
            list_store=people_list_store,
            progress_store=progress_store,
        ),
    )

    list_context = list_context(
        summary_definition=list_collector_block["summary"],
        for_list="people",
        section_id="section-id",
        has_repeating_blocks=False,
        edit_block_id=list_collector_block["edit_block"]["id"],
        remove_block_id=list_collector_block["remove_block"]["id"],
    )

    assert expected == list_context["list"]["list_items"]


@pytest.mark.usefixtures("app")
def test_list_context_items_incomplete_with_repeating_blocks(
    repeating_blocks_answer_store,
    repeating_blocks_list_store,
):
    schema = load_schema_from_name(
        "test_list_collector_repeating_blocks_section_summary"
    )
    list_collector_block = schema.get_block("any-other-companies-or-branches")
    expected = [
        {
            "item_title": "CompanyA",
            "edit_link": "/questionnaire/companies/PlwgoG/edit-company/",
            "remove_link": "/questionnaire/companies/PlwgoG/remove-company/",
            "primary_person": False,
            "list_item_id": "PlwgoG",
            "is_complete": False,
            "repeating_blocks": True,
        },
        {
            "item_title": "CompanyB",
            "edit_link": "/questionnaire/companies/UHPLbX/edit-company/",
            "remove_link": "/questionnaire/companies/UHPLbX/remove-company/",
            "primary_person": False,
            "list_item_id": "UHPLbX",
            "is_complete": False,
            "repeating_blocks": True,
        },
    ]

    list_context = ListContext(
        DEFAULT_LANGUAGE_CODE,
        schema,
        DataStores(
            answer_store=repeating_blocks_answer_store,
            list_store=repeating_blocks_list_store,
        ),
    )

    list_context = list_context(
        summary_definition=list_collector_block["summary"],
        for_list=list_collector_block["for_list"],
        section_id="section-companies",
        has_repeating_blocks=True,
        edit_block_id=list_collector_block["edit_block"]["id"],
        remove_block_id=list_collector_block["remove_block"]["id"],
    )

    assert expected == list_context["list"]["list_items"]


@pytest.mark.usefixtures("app")
def test_list_context_items_complete_with_repeating_blocks(
    repeating_blocks_answer_store, repeating_blocks_list_store, supplementary_data_store
):
    schema = load_schema_from_name(
        "test_list_collector_repeating_blocks_section_summary"
    )
    list_collector_block = schema.get_block("any-other-companies-or-branches")
    expected = [
        {
            "item_title": "CompanyA",
            "edit_link": "/questionnaire/companies/PlwgoG/edit-company/",
            "remove_link": "/questionnaire/companies/PlwgoG/remove-company/",
            "primary_person": False,
            "list_item_id": "PlwgoG",
            "is_complete": True,
            "repeating_blocks": True,
        },
        {
            "item_title": "CompanyB",
            "edit_link": "/questionnaire/companies/UHPLbX/edit-company/",
            "remove_link": "/questionnaire/companies/UHPLbX/remove-company/",
            "primary_person": False,
            "list_item_id": "UHPLbX",
            "is_complete": True,
            "repeating_blocks": True,
        },
    ]

    progress_store = ProgressStore(
        [
            ProgressDict(
                section_id="section-companies",
                list_item_id="PlwgoG",
                status=CompletionStatus.COMPLETED,
                block_ids=[],
            ),
            ProgressDict(
                section_id="section-companies",
                list_item_id="UHPLbX",
                status=CompletionStatus.COMPLETED,
                block_ids=[],
            ),
        ]
    )

    list_context = ListContext(
        DEFAULT_LANGUAGE_CODE,
        schema,
        DataStores(
            answer_store=repeating_blocks_answer_store,
            list_store=repeating_blocks_list_store,
            supplementary_data_store=supplementary_data_store,
            progress_store=progress_store,
        ),
    )

    list_context = list_context(
        summary_definition=list_collector_block["summary"],
        for_list=list_collector_block["for_list"],
        section_id="section-companies",
        has_repeating_blocks=True,
        edit_block_id=list_collector_block["edit_block"]["id"],
        remove_block_id=list_collector_block["remove_block"]["id"],
    )

    assert expected == list_context["list"]["list_items"]
