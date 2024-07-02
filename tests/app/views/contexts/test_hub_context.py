# pylint: disable=redefined-outer-name
import pytest

from app.data_models import CompletionStatus
from app.questionnaire.router import Router
from app.utilities.schema import load_schema_from_name
from app.views.contexts import HubContext


@pytest.fixture
def router(schema, data_stores):
    return Router(schema, data_stores)


def test_get_not_started_row_for_section(schema, data_stores):
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
                        "visuallyHiddenText": "Start section: Breakfast",
                        "url": "http://some/url",
                        "attributes": {"data-qa": "hub-row-section-1-link"},
                    }
                ],
            }
        ]
    }

    hub = HubContext(language=None, schema=schema, data_stores=data_stores)

    actual = hub.get_row_context_for_section(
        section_name="Breakfast",
        section_status=CompletionStatus.NOT_STARTED,
        section_url="http://some/url",
        row_id="section-1",
    )

    assert expected == actual


def test_get_completed_row_for_section(schema, data_stores):
    expected = {
        "rowItems": [
            {
                "rowTitle": "Breakfast",
                "rowTitleAttributes": {"data-qa": "hub-row-section-1-title"},
                "attributes": {"data-qa": "hub-row-section-1-state"},
                "iconType": "check",
                "valueList": [{"text": "Completed"}],
                "actions": [
                    {
                        "text": "View answers",
                        "visuallyHiddenText": "View answers: Breakfast",
                        "url": "http://some/url",
                        "attributes": {"data-qa": "hub-row-section-1-link"},
                    }
                ],
            }
        ]
    }

    hub = HubContext(language=None, schema=schema, data_stores=data_stores)

    actual = hub.get_row_context_for_section(
        section_name="Breakfast",
        section_status=CompletionStatus.COMPLETED,
        section_url="http://some/url",
        row_id="section-1",
    )

    assert expected == actual


def test_get_context(router, data_stores):
    schema = load_schema_from_name("test_hub_and_spoke")
    hub = HubContext(language="en", schema=schema, data_stores=data_stores)

    expected_context = {
        "individual_response_enabled": False,
        "individual_response_url": None,
        "guidance": None,
        "rows": [],
        "submit_button": "Continue",
        "title": "Choose another section to complete",
        "warning": None,
    }

    assert expected_context == hub(
        survey_complete=False, enabled_section_ids=router.enabled_section_ids
    )


def test_get_context_custom_content_incomplete(router, data_stores):
    schema = load_schema_from_name("test_hub_and_spoke_custom_content")
    hub_context = HubContext(language="en", schema=schema, data_stores=data_stores)

    expected_context = {
        "individual_response_enabled": False,
        "individual_response_url": None,
        "rows": [],
        "guidance": None,
        "submit_button": "Continue ",
        "title": "Choose another section to complete",
        "warning": None,
    }

    assert expected_context == hub_context(
        survey_complete=False, enabled_section_ids=router.enabled_section_ids
    )


def test_get_context_custom_content_complete(data_stores, router):
    schema = load_schema_from_name("test_hub_and_spoke_custom_content")
    hub_context = HubContext(language="en", schema=schema, data_stores=data_stores)

    expected_context = {
        "individual_response_enabled": False,
        "individual_response_url": None,
        "guidance": "Submission guidance",
        "rows": [],
        "submit_button": "Submission button",
        "title": "Submission title",
        "warning": "Submission warning",
    }

    assert expected_context == hub_context(
        survey_complete=True, enabled_section_ids=router.enabled_section_ids
    )


def test_get_context_no_list_items_survey_incomplete_individual_response_disabled(
    data_stores,
    router,
):
    schema = load_schema_from_name("test_individual_response")
    hub_context = HubContext(language="en", schema=schema, data_stores=data_stores)

    assert not (
        hub_context(
            survey_complete=False, enabled_section_ids=router.enabled_section_ids
        )["individual_response_enabled"]
    )
