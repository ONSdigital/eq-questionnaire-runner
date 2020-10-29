import pytest

from app.data_models.progress_store import ProgressStore
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.utilities.schema import load_schema_from_name
from app.views.contexts import ListContext


@pytest.mark.usefixtures("app")
def test_build_list_collector_context(
    list_collector_block, schema, people_answer_store, people_list_store
):
    list_context = ListContext(
        DEFAULT_LANGUAGE_CODE, schema, people_answer_store, people_list_store, {}, None
    )

    list_context = list_context(list_collector_block["summary"], for_list="people")

    assert all(
        keys in list_context["list"].keys() for keys in ["list_items", "editable"]
    )


@pytest.mark.usefixtures("app")
def test_build_list_summary_context_no_summary_block(
    schema, people_answer_store, people_list_store
):
    list_context = ListContext(
        DEFAULT_LANGUAGE_CODE, schema, people_answer_store, people_list_store, {}, None
    )

    list_context = list_context(None, for_list="people")

    assert list_context == {"list": {"editable": False, "list_items": []}}


@pytest.mark.usefixtures("app")
def test_build_list_summary_context(
    list_collector_block, people_answer_store, people_list_store
):

    schema = load_schema_from_name("test_list_collector_primary_person")
    expected = [
        {
            "item_title": "Toni Morrison",
            "edit_link": "/questionnaire/people/PlwgoG/edit-person/",
            "remove_link": "/questionnaire/people/PlwgoG/remove-person/",
            "primary_person": False,
            "list_item_id": "PlwgoG",
        },
        {
            "item_title": "Barry Pheloung",
            "edit_link": "/questionnaire/people/UHPLbX/edit-person/",
            "remove_link": "/questionnaire/people/UHPLbX/remove-person/",
            "primary_person": False,
            "list_item_id": "UHPLbX",
        },
    ]

    list_context = ListContext(
        DEFAULT_LANGUAGE_CODE, schema, people_answer_store, people_list_store, {}, None
    )

    list_context = list_context(
        list_collector_block["summary"],
        "people",
        edit_block_id=list_collector_block["edit_block"]["id"],
        remove_block_id=list_collector_block["remove_block"]["id"],
    )

    assert expected == list_context["list"]["list_items"]


@pytest.mark.usefixtures("app")
def test_assert_primary_person_string_appended(
    list_collector_block, people_answer_store, people_list_store
):
    schema = load_schema_from_name("test_list_collector_primary_person")
    people_list_store["people"].primary_person = "PlwgoG"

    list_context = ListContext(
        language=DEFAULT_LANGUAGE_CODE,
        progress_store=ProgressStore(),
        list_store=people_list_store,
        schema=schema,
        answer_store=people_answer_store,
        metadata=None,
    )
    list_context = list_context(
        list_collector_block["summary"], list_collector_block["for_list"]
    )

    assert list_context["list"]["list_items"][0]["primary_person"] is True
    assert list_context["list"]["list_items"][0]["item_title"] == "Toni Morrison (You)"
    assert list_context["list"]["list_items"][1]["item_title"] == "Barry Pheloung"


@pytest.mark.usefixtures("app")
def test_for_list_item_ids(
    list_collector_block, people_answer_store, people_list_store
):
    schema = load_schema_from_name("test_list_collector_primary_person")

    list_context = ListContext(
        language=DEFAULT_LANGUAGE_CODE,
        progress_store=ProgressStore(),
        list_store=people_list_store,
        schema=schema,
        answer_store=people_answer_store,
        metadata=None,
    )
    list_context = list_context(
        list_collector_block["summary"],
        list_collector_block["for_list"],
        for_list_item_ids=["UHPLbX"],
    )

    expected = [
        {
            "item_title": "Barry Pheloung",
            "primary_person": False,
            "list_item_id": "UHPLbX",
        }
    ]

    assert expected == list_context["list"]["list_items"]
