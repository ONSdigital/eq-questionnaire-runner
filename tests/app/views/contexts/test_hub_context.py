# pylint: disable=redefined-outer-name
import pytest

from app.data_models.progress_store import CompletionStatus
from app.questionnaire.router import Router
from app.utilities.schema import load_schema_from_name
from app.views.contexts import HubContext


@pytest.fixture
def router(schema, answer_store, list_store, progress_store):
    return Router(schema, answer_store, list_store, progress_store, metadata={})


def test_get_not_started_row_for_section(
    schema, progress_store, answer_store, list_store
):
    expected = {
        "rowItems": [
            {
                "rowTitle": "Breakfast",
                "rowTitleAttributes": {"data-qa": "hub-row-section-1-title"},
                "attributes": {"data-qa": "hub-row-section-1-state"},
                "valueList": [{"text": "Not started"}],
                "actions": [
                    {
                        "text": "Start section",
                        "ariaLabel": "Start Breakfast section",
                        "url": "http://some/url",
                        "attributes": {"data-qa": "hub-row-section-1-link"},
                    }
                ],
            }
        ]
    }

    hub = HubContext(
        language=None,
        progress_store=progress_store,
        list_store=list_store,
        schema=schema,
        answer_store=answer_store,
        metadata={},
    )

    actual = hub.get_row_context_for_section(
        section_name="Breakfast",
        section_status=CompletionStatus.NOT_STARTED,
        section_url="http://some/url",
        row_id="section-1",
    )

    assert expected == actual


def test_get_completed_row_for_section(
    schema, progress_store, answer_store, list_store
):
    expected = {
        "rowItems": [
            {
                "rowTitle": "Breakfast",
                "rowTitleAttributes": {"data-qa": "hub-row-section-1-title"},
                "attributes": {"data-qa": "hub-row-section-1-state"},
                "icon": "check",
                "valueList": [{"text": "Completed"}],
                "actions": [
                    {
                        "text": "View answers",
                        "ariaLabel": "View answers for Breakfast",
                        "url": "http://some/url",
                        "attributes": {"data-qa": "hub-row-section-1-link"},
                    }
                ],
            }
        ]
    }

    hub = HubContext(
        language=None,
        progress_store=progress_store,
        list_store=list_store,
        schema=schema,
        answer_store=answer_store,
        metadata={},
    )

    actual = hub.get_row_context_for_section(
        section_name="Breakfast",
        section_status=CompletionStatus.COMPLETED,
        section_url="http://some/url",
        row_id="section-1",
    )

    assert expected == actual


def test_get_context(progress_store, answer_store, list_store, router):
    schema = load_schema_from_name("test_hub_and_spoke")
    hub = HubContext(
        language=None,
        progress_store=progress_store,
        list_store=list_store,
        schema=schema,
        answer_store=answer_store,
        metadata={},
    )

    expected_context = {
        "individual_response_enabled": False,
        "individual_response_url": None,
        "guidance": None,
        "rows": [],
        "submit_button": "Continue",
        "title": "Choose another section to complete",
        "warning": None,
    }

    assert expected_context == hub.get_context(
        survey_complete=False, enabled_section_ids=router.enabled_section_ids
    )


def test_get_context_custom_content_incomplete(
    progress_store, answer_store, list_store, router
):
    schema = load_schema_from_name("test_hub_and_spoke_custom_content")
    hub_context = HubContext(
        language=None,
        progress_store=progress_store,
        list_store=list_store,
        schema=schema,
        answer_store=answer_store,
        metadata={},
    )

    expected_context = {
        "individual_response_enabled": False,
        "individual_response_url": None,
        "rows": [],
        "guidance": None,
        "submit_button": "Continue",
        "title": "Choose another section to complete",
        "warning": None,
    }

    assert expected_context == hub_context.get_context(
        survey_complete=False, enabled_section_ids=router.enabled_section_ids
    )


def test_get_context_custom_content_complete(
    progress_store, answer_store, list_store, router
):
    schema = load_schema_from_name("test_hub_and_spoke_custom_content")
    hub_context = HubContext(
        language=None,
        progress_store=progress_store,
        list_store=list_store,
        schema=schema,
        answer_store=answer_store,
        metadata={},
    )

    expected_context = {
        "individual_response_enabled": False,
        "individual_response_url": None,
        "guidance": "Submission guidance",
        "rows": [],
        "submit_button": "Submission button",
        "title": "Submission title",
        "warning": "Submission warning",
    }

    assert expected_context == hub_context.get_context(
        survey_complete=True, enabled_section_ids=router.enabled_section_ids
    )


def test_get_context_no_list_items_survey_incomplete_individual_response_disabled(
    progress_store, answer_store, list_store, router
):
    schema = load_schema_from_name("test_individual_response")
    hub_context = HubContext(
        language=None,
        progress_store=progress_store,
        list_store=list_store,
        schema=schema,
        answer_store=answer_store,
        metadata={},
    )

    assert not (
        hub_context.get_context(
            survey_complete=False, enabled_section_ids=router.enabled_section_ids
        )["individual_response_enabled"]
    )
