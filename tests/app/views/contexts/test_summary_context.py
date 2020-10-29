from unittest.mock import Mock, patch

import pytest

from app.data_models.answer_store import Answer, AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress_store import ProgressStore
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.utilities.schema import load_schema_from_name
from app.views.contexts import QuestionnaireSummaryContext, SectionSummaryContext
from app.views.contexts.calculated_summary_context import CalculatedSummaryContext
from tests.app.app_context_test_case import AppContextTestCase


class TestStandardSummaryContext(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self.metadata = {
            "return_by": "2016-10-10",
            "ref_p_start_date": "2016-10-10",
            "ref_p_end_date": "2016-10-10",
            "ru_ref": "def123",
            "response_id": "abc123",
            "ru_name": "Mr Cloggs",
            "trad_as": "Samsung",
            "tx_id": "12345678-1234-5678-1234-567812345678",
            "period_str": "201610",
            "employment_date": "2016-10-10",
            "collection_exercise_sid": "789",
            "schema_name": "0000_1",
        }
        self.language = "en"

    def check_context(self, context):
        self.assertEqual(len(context), 1)
        self.assertTrue(
            "summary" in context, "Key value {} missing from context".format("summary")
        )

        summary_context = context["summary"]
        for key_value in ("groups", "answers_are_editable", "summary_type"):
            self.assertTrue(
                key_value in summary_context,
                "Key value {} missing from context['summary']".format(key_value),
            )

    def check_summary_rendering_context(self, summary_rendering_context):
        for group in summary_rendering_context["summary"]["groups"]:
            self.assertTrue("id" in group)
            self.assertTrue("blocks" in group)
            for block in group["blocks"]:
                self.assertTrue("question" in block)
                self.assertTrue("title" in block["question"])
                self.assertTrue("answers" in block["question"])
                for answer in block["question"]["answers"]:
                    self.assertTrue("id" in answer)
                    self.assertTrue("value" in answer)
                    self.assertTrue("type" in answer)


class TestSummaryContext(TestStandardSummaryContext):
    def setUp(self):
        super().setUp()
        self.schema = load_schema_from_name("test_summary")
        self.answer_store = AnswerStore()
        self.list_store = ListStore()
        self.progress_store = ProgressStore()
        self.block_type = "Summary"
        self.rendered_block = {
            "parent_id": "summary-group",
            "id": "summary",
            "type": "Summary",
            "collapsible": True,
        }
        self.current_location = Location(
            section_id="default-section", block_id="summary"
        )

    def test_build_summary_rendering_context(self):
        questionnaire_summary_context = QuestionnaireSummaryContext(
            self.language,
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        summary_groups = questionnaire_summary_context()
        self.check_summary_rendering_context(summary_groups)

    def test_summary_context_with_custom_submission_content(self):
        self.schema = load_schema_from_name("test_summary_with_submission_text")

        questionnaire_summary_context = QuestionnaireSummaryContext(
            self.language,
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        summary_groups = questionnaire_summary_context()

        self.assertEqual(summary_groups["title"], "Submission title")
        self.assertEqual(summary_groups["guidance"], "Submission guidance")
        self.assertEqual(summary_groups["warning"], "Submission warning")
        self.assertEqual(summary_groups["submit_button"], "Submission button")


class TestSectionSummaryContext(TestStandardSummaryContext):
    def setUp(self):
        super().setUp()
        self.schema = load_schema_from_name("test_section_summary")
        self.answer_store = AnswerStore()
        self.list_store = ListStore()
        self.progress_store = ProgressStore()
        self.block_type = "SectionSummary"

    def test_build_summary_rendering_context(self):
        section_summary_context = SectionSummaryContext(
            self.language,
            self.schema,
            self.answer_store,
            self.progress_store,
            self.list_store,
            self.metadata,
        )

        single_section_context = section_summary_context(
            Location(section_id="property-details-section")
        )

        self.check_summary_rendering_context(single_section_context)

    def test_build_view_context_for_section_summary(self):
        current_location = Location(
            section_id="property-details-section", block_id="property-details-summary"
        )

        summary_context = SectionSummaryContext(
            self.language,
            self.schema,
            self.answer_store,
            self.progress_store,
            self.list_store,
            self.metadata,
        )
        context = summary_context(current_location)

        self.check_context(context)
        self.check_summary_rendering_context(context)
        self.assertEqual(len(context["summary"]), 6)
        self.assertTrue("title" in context["summary"])

    def test_custom_setion_summary_title(self):
        current_location = Location(section_id="house-details-section")
        answers = [{"answer_id": "house-type-answer", "value": "Semi-detached"}]
        summary_context = SectionSummaryContext(
            self.language,
            self.schema,
            AnswerStore(answers),
            self.list_store,
            self.progress_store,
            self.metadata,
        )
        context = summary_context(current_location)
        self.assertEqual(
            "Household Summary - Semi-detached", context["summary"]["title"]
        )

    def test_custom_section_summary_page_title(self):
        current_location = Location(section_id="property-details-section")
        summary_context = SectionSummaryContext(
            self.language,
            self.schema,
            AnswerStore([]),
            self.list_store,
            self.progress_store,
            self.metadata,
        )
        context = summary_context(current_location)
        self.assertEqual(
            "Custom section summary title", context["summary"]["page_title"]
        )

    def test_section_summary_page_title_placeholder_text_replaced(self):
        current_location = Location(section_id="house-details-section")
        answers = [{"answer_id": "house-type-answer", "value": "Semi-detached"}]
        summary_context = SectionSummaryContext(
            self.language,
            self.schema,
            AnswerStore(answers),
            self.progress_store,
            self.list_store,
            self.metadata,
        )
        context = summary_context(current_location)
        self.assertEqual(context["summary"]["page_title"], "Household Summary - …")

    def test_section_summary_page_title_placeholder_text_plural_replaced(self):
        current_location = Location(section_id="household-count-section")
        answers = [{"answer_id": "number-of-people-answer", "value": 3}]
        summary_context = SectionSummaryContext(
            self.language,
            self.schema,
            AnswerStore(answers),
            self.list_store,
            self.progress_store,
            self.metadata,
        )
        context = summary_context(current_location)
        self.assertEqual(context["summary"]["page_title"], "… people live here")

    def test_section_summary_title_is_section_title(self):
        current_location = Location(section_id="property-details-section")
        summary_context = SectionSummaryContext(
            self.language,
            self.schema,
            self.answer_store,
            self.progress_store,
            self.list_store,
            self.metadata,
        )
        context = summary_context(current_location)
        self.assertEqual(context["summary"]["title"], "Property Details Section")


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
    current_location = Location(section_id="section")

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
    )
    context = summary_context(current_location)

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
                            },
                            {
                                "edit_link": "/questionnaire/people/UHPLbX/edit-person/?return_to=section-summary",
                                "item_title": "Barry Pheloung",
                                "primary_person": False,
                                "remove_link": "/questionnaire/people/UHPLbX/remove-person/?return_to=section-summary",
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
    current_location = Location(section_id="section")

    summary_context = SectionSummaryContext(
        DEFAULT_LANGUAGE_CODE,
        schema,
        AnswerStore([{"answer_id": "anyone-usually-live-at-answer", "value": "No"}]),
        ListStore(),
        ProgressStore(),
        {},
    )

    context = summary_context(current_location)
    expected = {
        "summary": {
            "answers_are_editable": True,
            "collapsible": False,
            "custom_summary": [
                {
                    "add_link": "/questionnaire/anyone-usually-live-at/?return_to=section-summary",
                    "add_link_text": "Add someone to this household",
                    "empty_list_text": "There are no householders",
                    "list_name": "people",
                    "list": {"list_items": [], "editable": True},
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
    current_location = Location(section_id="section")

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
    )

    context = summary_context(current_location)

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
    current_location = Location(
        section_id="personal-details-section", list_name="people", list_item_id="PlwgoG"
    )

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
    )

    context = section_summary_context(current_location)

    assert context["summary"]["title"] == "Toni Morrison"

    new_location = Location(
        block_id="personal-summary",
        section_id="personal-details-section",
        list_name="people",
        list_item_id="UHPLbX",
    )

    context = section_summary_context(new_location)
    assert context["summary"]["title"] == "Barry Pheloung"


@pytest.mark.usefixtures("app")
def test_primary_only_links_for_section_summary(people_answer_store):
    schema = load_schema_from_name("test_list_collector_section_summary")
    current_location = Location(section_id="section")

    summary_context = SectionSummaryContext(
        language=DEFAULT_LANGUAGE_CODE,
        schema=schema,
        answer_store=people_answer_store,
        list_store=ListStore(
            [{"items": ["PlwgoG"], "name": "people", "primary_person": "PlwgoG"}]
        ),
        progress_store=ProgressStore(),
        metadata={"display_address": "70 Abingdon Road, Goathill"},
    )
    context = summary_context(current_location)

    list_items = context["summary"]["custom_summary"][0]["list"]["list_items"]

    assert "/add-or-edit-primary-person/" in list_items[0]["edit_link"]


@pytest.mark.usefixtures("app")
def test_primary_links_for_section_summary(people_answer_store):
    schema = load_schema_from_name("test_list_collector_section_summary")
    current_location = Location(section_id="section")

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
    )
    context = summary_context(current_location)

    list_items = context["summary"]["custom_summary"][0]["list"]["list_items"]

    assert "/edit-person/" in list_items[0]["edit_link"]
    assert "/edit-person/" in list_items[1]["edit_link"]
