# pylint: disable=redefined-outer-name
import pytest

from app.data_model.progress_store import CompletionStatus
from app.questionnaire.router import Router
from app.views.contexts.hub_context import HubContext


@pytest.fixture
def router(schema, answer_store, list_store, progress_store):
    return Router(schema, answer_store, list_store, progress_store, metadata={})


def test_get_not_started_row_for_section(
    schema, progress_store, answer_store, list_store, router
):
    expected = {
        'title': 'Breakfast',
        'rowItems': [
            {
                'valueList': [{'text': 'Not started'}],
                'actions': [
                    {
                        'text': 'Start section',
                        'ariaLabel': 'Start Breakfast section',
                        'url': 'http://some/url',
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
        survey_complete=False,
        enabled_section_ids=router.enabled_section_ids,
    )

    actual = hub.get_row_context_for_section(
        section_name='Breakfast',
        section_status=CompletionStatus.NOT_STARTED,
        section_url='http://some/url',
    )

    assert expected == actual


def test_get_completed_row_for_section(
    schema, progress_store, answer_store, list_store, router
):
    expected = {
        'title': 'Breakfast',
        'rowItems': [
            {
                'icon': 'check-green',
                'valueList': [{'text': 'Completed'}],
                'actions': [
                    {
                        'text': 'View answers',
                        'ariaLabel': 'View answers for Breakfast',
                        'url': 'http://some/url',
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
        survey_complete=False,
        enabled_section_ids=router.enabled_section_ids,
    )

    actual = hub.get_row_context_for_section(
        section_name='Breakfast',
        section_status=CompletionStatus.COMPLETED,
        section_url='http://some/url',
    )

    assert expected == actual


def test_get_context(schema, progress_store, answer_store, list_store, router):
    hub = HubContext(
        language=None,
        progress_store=progress_store,
        list_store=list_store,
        schema=schema,
        answer_store=answer_store,
        metadata={},
        survey_complete=False,
        enabled_section_ids=router.enabled_section_ids,
    )

    expected_context = {
        'title': 'Choose another section to complete',
        'description': 'You must complete all sections in order to submit this survey',
        'rows': [],
        'submit_button': 'Continue',
    }

    assert expected_context == hub.get_context()
