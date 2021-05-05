from unittest.mock import MagicMock, Mock, patch

import pytest

from app.data_models.answer_store import Answer, AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress_store import ProgressStore
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.questionnaire.routing_path import RoutingPath
from app.utilities.schema import load_schema_from_name
from app.views.contexts import SectionSummaryContext
from app.views.contexts.calculated_summary_context import CalculatedSummaryContext
from tests.app.views.contexts.test_submit_context import TestStandardSummaryContext


class TestCalculatedSummaryContext(TestStandardSummaryContext):
    def setUp(self):
        super().setUp()
        self.schema = load_schema_from_name("test_calculated_summary")
        answers = [
            {"value": 1, "answer_id": "first-number-answer"},
            {"value": 2, "answer_id": "second-number-answer"},
            {"value": 3, "answer_id": "second-number-answer-unit-total"},
            {"value": 4, "answer_id": "second-number-answer-also-in-total"},
            {"value": 5, "answer_id": "third-number-answer"},
            {"value": 6, "answer_id": "third-and-a-half-number-answer-unit-total"},
            {"value": "No", "answer_id": "skip-fourth-block-answer"},
            {"value": 7, "answer_id": "fourth-number-answer"},
            {"value": 8, "answer_id": "fourth-and-a-half-number-answer-also-in-total"},
            {"value": 9, "answer_id": "fifth-percent-answer"},
            {"value": 10, "answer_id": "fifth-number-answer"},
            {"value": 11, "answer_id": "sixth-percent-answer"},
            {"value": 12, "answer_id": "sixth-number-answer"},
        ]
        self.answer_store = AnswerStore(answers)
        self.list_store = ListStore()
        self.progress_store = ProgressStore()
        self.block_type = "CalculatedSummary"

    @patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="en_GB"))
    def test_build_view_context_for_currency_calculated_summary_no_skip(self):
        current_location = Location(
            section_id="default-section", block_id="currency-total-playback-with-fourth"
        )

        calculated_summary_context = CalculatedSummaryContext(
            "en",
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        context = calculated_summary_context.build_view_context_for_calculated_summary(
            current_location
        )

        self.check_context(context)
        self.check_summary_rendering_context(context)
        self.assertEqual(len(context["summary"]), 6)
        context_summary = context["summary"]
        self.assertTrue("title" in context_summary)
        self.assertEqual(
            context_summary["title"],
            "We calculate the total of currency values entered to be £27.00. Is this correct? (With Fourth)",
        )

        self.assertTrue("calculated_question" in context_summary)
        self.assertEqual(len(context_summary["groups"][0]["blocks"]), 5)
        self.assertEqual(
            context_summary["calculated_question"]["title"],
            "Grand total of previous values",
        )
        self.assertEqual(
            context_summary["calculated_question"]["answers"][0]["value"], "£27.00"
        )

    @patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="en_GB"))
    def test_build_view_context_for_currency_calculated_summary_with_skip(self):
        current_location = Location(
            section_id="default-section",
            block_id="currency-total-playback-skipped-fourth",
        )

        skip_answer = Answer("skip-fourth-block-answer", "Yes")
        self.answer_store.add_or_update(skip_answer)

        calculated_summary_context = CalculatedSummaryContext(
            "en",
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        context = calculated_summary_context.build_view_context_for_calculated_summary(
            current_location
        )

        self.check_context(context)
        self.check_summary_rendering_context(context)
        self.assertEqual(len(context["summary"]), 6)
        context_summary = context["summary"]
        self.assertTrue("title" in context_summary)
        self.assertEqual(len(context_summary["groups"][0]["blocks"]), 3)
        self.assertEqual(
            context_summary["title"],
            "We calculate the total of currency values entered to be £12.00. Is this correct? (Skipped Fourth)",
        )

        self.assertTrue("calculated_question" in context_summary)
        self.assertEqual(
            context_summary["calculated_question"]["title"],
            "Grand total of previous values",
        )
        self.assertEqual(
            context_summary["calculated_question"]["answers"][0]["value"], "£12.00"
        )

    @patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="cy"))
    def test_build_view_context_for_unit_calculated_summary(self):
        current_location = Location(
            section_id="default-section", block_id="unit-total-playback"
        )

        calculated_summary_context = CalculatedSummaryContext(
            "cy",
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        context = calculated_summary_context.build_view_context_for_calculated_summary(
            current_location
        )

        self.check_context(context)
        self.check_summary_rendering_context(context)
        self.assertEqual(len(context["summary"]), 6)
        context_summary = context["summary"]
        self.assertTrue("title" in context_summary)
        self.assertEqual(
            context_summary["title"],
            "We calculate the total of unit values entered to be 9 cm. Is this correct?",
        )

        self.assertTrue("calculated_question" in context_summary)
        self.assertEqual(
            context_summary["calculated_question"]["title"],
            "Grand total of previous values",
        )
        self.assertEqual(
            context_summary["calculated_question"]["answers"][0]["value"], "9 cm"
        )

    def test_build_view_context_for_percentage_calculated_summary(self):
        current_location = Location(
            section_id="default-section", block_id="percentage-total-playback"
        )

        calculated_summary_context = CalculatedSummaryContext(
            "en",
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        context = calculated_summary_context.build_view_context_for_calculated_summary(
            current_location
        )

        self.check_context(context)
        self.check_summary_rendering_context(context)
        self.assertEqual(len(context["summary"]), 6)
        context_summary = context["summary"]
        self.assertTrue("title" in context_summary)
        self.assertEqual(
            context_summary["title"],
            "We calculate the total of percentage values entered to be 20%. Is this correct?",
        )

        self.assertTrue("calculated_question" in context_summary)
        self.assertEqual(
            context_summary["calculated_question"]["title"],
            "Grand total of previous values",
        )
        self.assertEqual(
            context_summary["calculated_question"]["answers"][0]["value"], "20%"
        )

    @patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="cy"))
    def test_build_view_context_for_number_calculated_summary(self):
        current_location = Location(
            section_id="default-section", block_id="number-total-playback"
        )

        calculated_summary_context = CalculatedSummaryContext(
            "cy",
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        context = calculated_summary_context.build_view_context_for_calculated_summary(
            current_location
        )

        self.check_context(context)
        self.check_summary_rendering_context(context)
        self.assertEqual(len(context["summary"]), 6)
        context_summary = context["summary"]
        self.assertTrue("title" in context_summary)
        self.assertEqual(
            context_summary["title"],
            "We calculate the total of number values entered to be 22. Is this correct?",
        )

        self.assertTrue("calculated_question" in context_summary)
        self.assertEqual(
            context_summary["calculated_question"]["title"],
            "Grand total of previous values",
        )
        self.assertEqual(
            context_summary["calculated_question"]["answers"][0]["value"], "22"
        )


@pytest.mark.usefixtures("app")
def test_context_for_section_list_summary(people_answer_store):
    schema = load_schema_from_name("test_list_collector_section_summary")

    summary_context = SectionSummaryContext(
        language=DEFAULT_LANGUAGE_CODE,
        schema=schema,
        answer_store=people_answer_store,
        list_store=ListStore(
            [
                {"items": ["PlwgoG", "UHPLbX"], "name": "people"},
                {"items": ["gTrlio"], "name": "visitors"},
            ]
        ),
        progress_store=ProgressStore(),
        metadata={"display_address": "70 Abingdon Road, Goathill"},
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
    expected = {
        "summary": {
            "answers_are_editable": True,
            "collapsible": False,
            "custom_summary": [
                {
                    "add_link": "/questionnaire/people/add-person/?return_to=section-summary",
                    "add_link_text": "Add someone to this household",
                    "empty_list_text": "There are no householders",
                    "list": {
                        "editable": True,
                        "list_items": [
                            {
                                "edit_link": "/questionnaire/people/PlwgoG/edit-person/?return_to=section-summary",
                                "item_title": "Toni Morrison",
                                "primary_person": False,
                                "remove_link": "/questionnaire/people/PlwgoG/remove-person/?return_to=section-summary",
                                "list_item_id": "PlwgoG",
                            },
                            {
                                "edit_link": "/questionnaire/people/UHPLbX/edit-person/?return_to=section-summary",
                                "item_title": "Barry Pheloung",
                                "primary_person": False,
                                "remove_link": "/questionnaire/people/UHPLbX/remove-person/?return_to=section-summary",
                                "list_item_id": "UHPLbX",
                            },
                        ],
                    },
                    "list_name": "people",
                    "title": "Household members staying overnight on 13 October 2019 at 70 Abingdon Road, Goathill",
                    "type": "List",
                },
                {
                    "add_link": "/questionnaire/visitors/add-visitor/?return_to=section-summary",
                    "add_link_text": "Add another visitor to this household",
                    "empty_list_text": "There are no visitors",
                    "list": {
                        "editable": True,
                        "list_items": [
                            {
                                "edit_link": "/questionnaire/visitors/gTrlio/edit-visitor-person/?return_to=section-summary",
                                "item_title": "",
                                "primary_person": False,
                                "remove_link": "/questionnaire/visitors/gTrlio/remove-visitor/?return_to=section-summary",
                                "list_item_id": "gTrlio",
                            }
                        ],
                    },
                    "list_name": "visitors",
                    "title": "Visitors staying overnight on 13 October 2019 at 70 Abingdon Road, Goathill",
                    "type": "List",
                },
            ],
            "page_title": "People who live here and overnight visitors",
            "summary_type": "SectionSummary",
            "title": "People who live here and overnight visitors",
        }
    }

    assert context == expected


@pytest.mark.usefixtures("app")
def test_context_for_driving_question_summary_empty_list():
    schema = load_schema_from_name("test_list_collector_driving_question")

    summary_context = SectionSummaryContext(
        DEFAULT_LANGUAGE_CODE,
        schema,
        AnswerStore([{"answer_id": "anyone-usually-live-at-answer", "value": "No"}]),
        ListStore(),
        ProgressStore(),
        {},
        current_location=Location(section_id="section"),
        routing_path=RoutingPath(["anyone-usually-live-at"], section_id="section"),
    )

    context = summary_context()
    expected = {
        "summary": {
            "answers_are_editable": True,
            "collapsible": False,
            "custom_summary": [
                {
                    "add_link": "/questionnaire/anyone-usually-live-at/?return_to=section-summary",
                    "add_link_text": "Add someone to this household",
                    "empty_list_text": "There are no householders",
                    "list": {"editable": False, "list_items": []},
                    "list_name": "people",
                    "title": "Household members",
                    "type": "List",
                }
            ],
            "page_title": "List Collector Driving Question Summary",
            "summary_type": "SectionSummary",
            "title": "List Collector Driving Question Summary",
        }
    }

    assert context == expected


@pytest.mark.usefixtures("app")
def test_context_for_driving_question_summary():
    schema = load_schema_from_name("test_list_collector_driving_question")

    summary_context = SectionSummaryContext(
        DEFAULT_LANGUAGE_CODE,
        schema,
        AnswerStore(
            [
                {"answer_id": "anyone-usually-live-at-answer", "value": "Yes"},
                {"answer_id": "first-name", "value": "Toni", "list_item_id": "PlwgoG"},
                {
                    "answer_id": "last-name",
                    "value": "Morrison",
                    "list_item_id": "PlwgoG",
                },
            ]
        ),
        ListStore([{"items": ["PlwgoG"], "name": "people"}]),
        ProgressStore(),
        {},
        current_location=Location(section_id="section"),
        routing_path=RoutingPath(
            ["anyone-usually-live-at", "anyone-else-live-at"], section_id="section"
        ),
    )

    context = summary_context()

    expected = {
        "summary": {
            "answers_are_editable": True,
            "collapsible": False,
            "custom_summary": [
                {
                    "add_link": "/questionnaire/people/add-person/?return_to=section-summary",
                    "add_link_text": "Add someone to this household",
                    "empty_list_text": "There are no householders",
                    "list": {
                        "editable": True,
                        "list_items": [
                            {
                                "item_title": "Toni Morrison",
                                "primary_person": False,
                                "edit_link": "/questionnaire/people/PlwgoG/edit-person/?return_to=section-summary",
                                "remove_link": "/questionnaire/people/PlwgoG/remove-person/?return_to=section-summary",
                                "list_item_id": "PlwgoG",
                            }
                        ],
                    },
                    "list_name": "people",
                    "title": "Household members",
                    "type": "List",
                }
            ],
            "page_title": "List Collector Driving Question Summary",
            "summary_type": "SectionSummary",
            "title": "List Collector Driving Question Summary",
        }
    }

    assert context == expected


@pytest.mark.usefixtures("app")
def test_titles_for_repeating_section_summary(people_answer_store):
    schema = load_schema_from_name("test_repeating_sections_with_hub_and_spoke")

    section_summary_context = SectionSummaryContext(
        DEFAULT_LANGUAGE_CODE,
        schema,
        people_answer_store,
        ListStore(
            [
                {"items": ["PlwgoG", "UHPLbX"], "name": "people"},
                {"items": ["gTrlio"], "name": "visitors"},
            ]
        ),
        ProgressStore(),
        {},
        current_location=Location(
            section_id="personal-details-section",
            list_name="people",
            list_item_id="PlwgoG",
        ),
        routing_path=MagicMock(),
    )

    context = section_summary_context()

    assert context["summary"]["title"] == "Toni Morrison"

    section_summary_context = SectionSummaryContext(
        DEFAULT_LANGUAGE_CODE,
        schema,
        people_answer_store,
        ListStore(
            [
                {"items": ["PlwgoG", "UHPLbX"], "name": "people"},
                {"items": ["gTrlio"], "name": "visitors"},
            ]
        ),
        ProgressStore(),
        {},
        current_location=Location(
            block_id="personal-summary",
            section_id="personal-details-section",
            list_name="people",
            list_item_id="UHPLbX",
        ),
        routing_path=MagicMock(),
    )

    context = section_summary_context()
    assert context["summary"]["title"] == "Barry Pheloung"


@pytest.mark.usefixtures("app")
def test_primary_only_links_for_section_summary(people_answer_store):
    schema = load_schema_from_name("test_list_collector_section_summary")

    summary_context = SectionSummaryContext(
        language=DEFAULT_LANGUAGE_CODE,
        schema=schema,
        answer_store=people_answer_store,
        list_store=ListStore(
            [{"items": ["PlwgoG"], "name": "people", "primary_person": "PlwgoG"}]
        ),
        progress_store=ProgressStore(),
        metadata={"display_address": "70 Abingdon Road, Goathill"},
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

    assert "/add-or-edit-primary-person/" in list_items[0]["edit_link"]


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
