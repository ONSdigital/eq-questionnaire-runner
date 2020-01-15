import pytest
from app.utilities.schema import load_schema_from_name
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.views.contexts.list_collector_context import ListCollectorContext


@pytest.mark.usefixtures("app")
def test_build_list_collector_context(
    list_collector_block, schema, people_answer_store, people_list_store, form
):

    context = ListCollectorContext(
        language=DEFAULT_LANGUAGE_CODE,
        progress_store={},
        list_store=people_list_store,
        schema=schema,
        answer_store=people_answer_store,
        metadata=None,
    )

    list_context = context.build_list_collector_context(list_collector_block, form)

    assert all(keys in list_context.keys() for keys in ["block", "form", "list"])


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
        },
        {
            "item_title": "Barry Pheloung",
            "edit_link": "/questionnaire/people/UHPLbX/edit-person/",
            "remove_link": "/questionnaire/people/UHPLbX/remove-person/",
            "primary_person": False,
        },
    ]

    context = ListCollectorContext(
        language=DEFAULT_LANGUAGE_CODE,
        progress_store={},
        list_store=people_list_store,
        schema=schema,
        answer_store=people_answer_store,
        metadata=None,
    )

    actual = context.build_list_items_summary_context(
        list_collector_block=list_collector_block, return_to=None
    )

    assert expected == actual


@pytest.mark.usefixtures("app")
def test_assert_primary_person_string_appended(
    list_collector_block, people_answer_store, people_list_store
):
    schema = load_schema_from_name("test_list_collector_primary_person")
    people_list_store["people"].primary_person = "PlwgoG"

    context = ListCollectorContext(
        language=DEFAULT_LANGUAGE_CODE,
        progress_store={},
        list_store=people_list_store,
        schema=schema,
        answer_store=people_answer_store,
        metadata=None,
    )

    list_item_context = context.build_list_items_summary_context(
        list_collector_block=list_collector_block, return_to=None
    )

    assert list_item_context[0]["primary_person"] is True
    assert list_item_context[0]["item_title"] == "Toni Morrison (You)"
    assert list_item_context[1]["item_title"] == "Barry Pheloung"
