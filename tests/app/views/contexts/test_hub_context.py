import pytest

from app.data_model.list_store import ListStore
from app.data_model.progress_store import ProgressStore, CompletionStatus
from app.data_model.answer_store import AnswerStore
from app.questionnaire.path_finder import PathFinder
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.contexts.hub_context import HubContext


@pytest.fixture(name='schema')
def fixture_schema():
    return QuestionnaireSchema({})


@pytest.fixture(name='answer_store')
def fixture_answer_store():
    return AnswerStore()


@pytest.fixture(name='list_storw')
def fixture_list_store():
    return ListStore()


@pytest.fixture(name='progress_store')
def fixture_progress_store():
    return ProgressStore()


@pytest.fixture(name='path_finder')
def fixture_path_finder(schema, answer_store):
    return PathFinder(schema=schema, answer_store=answer_store, metadata={})


def test_get_not_started_row_for_section(
    schema, progress_store, answer_store, list_store, path_finder
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
        path_finder=path_finder,
    )

    actual = hub.get_row_context_for_section(
        section_name='Breakfast',
        section_status=CompletionStatus.NOT_STARTED,
        section_url='http://some/url',
    )

    assert expected == actual


def test_get_completed_row_for_section(
    schema, progress_store, answer_store, list_store, path_finder
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
        path_finder=path_finder,
    )

    actual = hub.get_row_context_for_section(
        section_name='Breakfast',
        section_status=CompletionStatus.COMPLETED,
        section_url='http://some/url',
    )

    assert expected == actual


def test_get_context(schema, progress_store, answer_store, list_store, path_finder):

    hub = HubContext(
        language=None,
        progress_store=progress_store,
        list_store=list_store,
        schema=schema,
        answer_store=answer_store,
        metadata={},
        survey_complete=False,
        path_finder=path_finder,
    )

    expected_context = {
        'title': 'Choose another section to complete',
        'description': 'You must complete all sections in order to submit this survey',
        'rows': [],
        'submit_button': 'Continue',
    }

    assert expected_context == hub.get_context()
