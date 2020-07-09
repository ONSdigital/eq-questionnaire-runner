# pylint: disable=redefined-outer-name
import pytest

from app.data_model.progress_store import CompletionStatus
from app.questionnaire.router import Router
from app.utilities.schema import load_schema_from_name
from app.views.contexts.hub_context import HubContext


@pytest.fixture
def router(schema, answer_store, list_store, progress_store):
    return Router(schema, answer_store, list_store, progress_store, metadata={})


def test_get_not_started_row_for_section(
    schema, progress_store, answer_store, list_store
):
    expected = {
        "rowTitle": "Breakfast",
        "rowItems": [
            {
                "rowTitleAttributes": {"data-qa": "hub-row-title-section-1"},
                "attributes": {"data-qa": "hub-row-state-section-1"},
                "valueList": [{"text": "Not started"}],
                "actions": [
                    {
                        "text": "Start section",
                        "ariaLabel": "Start Breakfast section",
                        "url": "http://some/url",
                        "attributes": {"data-qa": "hub-row-link-section-1"},
                    }
                ],
            }
        ],
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
        section_id="section-1",
        section_url="http://some/url",
    )

    assert expected == actual


def test_get_completed_row_for_section(
    schema, progress_store, answer_store, list_store
):
    expected = {
        "rowTitle": "Breakfast",
        "rowItems": [
            {
                "rowTitleAttributes": {"data-qa": "hub-row-title-section-1"},
                "attributes": {"data-qa": "hub-row-state-section-1"},
                "icon": "check-green",
                "valueList": [{"text": "Completed"}],
                "actions": [
                    {
                        "text": "View answers",
                        "ariaLabel": "View answers for Breakfast",
                        "url": "http://some/url",
                        "attributes": {"data-qa": "hub-row-link-section-1"},
                    }
                ],
            }
        ],
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
        section_id="section-1",
        section_url="http://some/url",
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
        "title": "Choose another section to complete",
        "guidance": "You must complete all sections in order to submit this survey",
        "rows": [],
        "submit_button": "Continue",
        "submission_guidance": None,
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
        "title": "Choose another section to complete",
        "guidance": "Guidance displayed on hub when incomplete",
        "rows": [],
        "submit_button": "Continue",
        "submission_guidance": None,
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
        "title": "Title displayed on hub when complete",
        "guidance": "Guidance displayed on hub when complete",
        "rows": [],
        "submit_button": "Submission text",
        "submission_guidance": "Submission guidance",
    }

    assert expected_context == hub_context.get_context(
        survey_complete=True, enabled_section_ids=router.enabled_section_ids
    )
