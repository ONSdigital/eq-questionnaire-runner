from unittest.mock import MagicMock

import pytest

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress_store import ProgressStore
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.questionnaire.routing_path import RoutingPath
from app.utilities.schema import load_schema_from_name
from app.views.contexts import SectionSummaryContext
from tests.app.views.contexts import SummaryContextTestCase


class TestSectionSummaryContext(SummaryContextTestCase):
    def setUp(self):
        super().setUp()
        self.block_type = "SectionSummary"
        self.schema = load_schema_from_name("test_section_summary")
        self.language = "en"
        self.metadata = {}
        self.response_metadata = {}
        self.answer_store = AnswerStore()
        self.list_store = ListStore()
        self.progress_store = ProgressStore()

    def test_build_summary_rendering_context(self):
        section_summary_context = SectionSummaryContext(
            self.language,
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
            self.response_metadata,
            current_location=Location(section_id="property-details-section"),
            routing_path=MagicMock(),
        )

        single_section_context = section_summary_context()

        self.assert_summary_context(single_section_context)

    def test_build_view_context_for_section_summary(self):
        summary_context = SectionSummaryContext(
            self.language,
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
            self.response_metadata,
            current_location=Location(
                section_id="property-details-section",
                block_id="property-details-summary",
            ),
            routing_path=MagicMock(),
        )
        context = summary_context()

        self.assertIn("summary", context)
        self.assert_summary_context(context)
        self.assertEqual(len(context["summary"]), 6)
        self.assertTrue("title" in context["summary"])

    def test_custom_section_summary_title(self):
        answers = [{"answer_id": "house-type-answer", "value": "Semi-detached"}]
        summary_context = SectionSummaryContext(
            self.language,
            self.schema,
            AnswerStore(answers),
            self.list_store,
            self.progress_store,
            self.metadata,
            self.response_metadata,
            current_location=Location(section_id="house-details-section"),
            routing_path=MagicMock(),
        )
        context = summary_context()
        self.assertEqual(
            "Household Summary - Semi-detached", context["summary"]["title"]
        )

    def test_custom_section_summary_page_title(self):
        summary_context = SectionSummaryContext(
            self.language,
            self.schema,
            AnswerStore([]),
            self.list_store,
            self.progress_store,
            self.metadata,
            self.response_metadata,
            current_location=Location(section_id="property-details-section"),
            routing_path=MagicMock(),
        )
        context = summary_context()
        self.assertEqual(
            "Custom section summary title", context["summary"]["page_title"]
        )

    def test_section_summary_page_title_placeholder_text_replaced(self):
        answers = [{"answer_id": "house-type-answer", "value": "Semi-detached"}]
        summary_context = SectionSummaryContext(
            self.language,
            self.schema,
            AnswerStore(answers),
            self.progress_store,
            self.list_store,
            self.metadata,
            self.response_metadata,
            current_location=Location(section_id="house-details-section"),
            routing_path=MagicMock(),
        )
        context = summary_context()
        self.assertEqual(context["summary"]["page_title"], "Household Summary - …")

    def test_section_summary_page_title_placeholder_text_plural_replaced(self):
        answers = [{"answer_id": "number-of-people-answer", "value": 3}]
        summary_context = SectionSummaryContext(
            self.language,
            self.schema,
            AnswerStore(answers),
            self.list_store,
            self.progress_store,
            self.metadata,
            self.response_metadata,
            current_location=Location(section_id="household-count-section"),
            routing_path=MagicMock(),
        )
        context = summary_context()
        self.assertEqual(context["summary"]["page_title"], "… people live here")

    def test_section_summary_title_is_section_title(self):
        summary_context = SectionSummaryContext(
            self.language,
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
            self.response_metadata,
            routing_path=MagicMock(),
            current_location=Location(section_id="property-details-section"),
        )
        context = summary_context()
        self.assertEqual(context["summary"]["title"], "Property Details Section")


@pytest.mark.usefixtures("app")
def test_primary_links_for_section_summary(people_answer_store):
    schema = load_schema_from_name("test_list_collector_section_summary")

    summary_context = SectionSummaryContext(
        language=DEFAULT_LANGUAGE_CODE,
        schema=schema,
        answer_store=people_answer_store,
        list_store=ListStore(
            [
                {
                    "items": ["PlwgoG", "fg0sPd"],
                    "name": "people",
                    "primary_person": "PlwgoG",
                }
            ]
        ),
        progress_store=ProgressStore(),
        metadata={"display_address": "70 Abingdon Road, Goathill"},
        response_metadata={},
        current_location=Location(section_id="section"),
        routing_path=RoutingPath(
            [
                "primary-person-list-collector",
                "list-collector",
                "visitor-list-collector",
            ],
            section_id="section",
        ),
    )
    context = summary_context()

    list_items = context["summary"]["custom_summary"][0]["list"]["list_items"]

    assert "/edit-person/" in list_items[0]["edit_link"]
    assert "/edit-person/" in list_items[1]["edit_link"]
