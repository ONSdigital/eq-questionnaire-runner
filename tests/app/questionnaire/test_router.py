from unittest.mock import Mock

from flask import url_for

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress_store import CompletionStatus, ProgressStore
from app.questionnaire.location import Location
from app.questionnaire.router import Router
from app.questionnaire.routing_path import RoutingPath
from app.utilities.schema import load_schema_from_name
from tests.app.app_context_test_case import AppContextTestCase


class TestRouter(AppContextTestCase):  # pylint: disable=too-many-public-methods
    answer_store = AnswerStore()
    list_store = ListStore()
    progress_store = ProgressStore()
    metadata = {}

    def test_can_access_location(self):
        schema = load_schema_from_name("test_textfield")
        router = Router(
            schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        current_location = Location(section_id="default-section", block_id="name-block")
        routing_path = RoutingPath(["name-block"], section_id="default-section")

        can_access_location = router.can_access_location(current_location, routing_path)

        self.assertTrue(can_access_location)

    def test_cant_access_location(self):
        schema = load_schema_from_name("test_repeating_sections_with_hub_and_spoke")

        list_store = ListStore(
            [
                {
                    "items": ["abc123", "123abc"],
                    "name": "people",
                    "primary_person": "abc123",
                }
            ]
        )
        router = Router(
            schema, self.answer_store, list_store, self.progress_store, self.metadata
        )

        current_location = Location(
            section_id="personal-details-section",
            block_id="proxy",
            list_item_id="invalid-list-item-id",
        )
        routing_path = []
        can_access_location = router.can_access_location(current_location, routing_path)

        self.assertFalse(can_access_location)

    def test_cant_access_location_section_disabled(self):
        schema = load_schema_from_name("test_section_enabled_checkbox")

        router = Router(
            schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        current_location = Location(
            section_id="section-2", block_id="section-2-block", list_item_id=None
        )
        can_access_location = router.can_access_location(
            current_location, routing_path=[]
        )

        self.assertFalse(can_access_location)

    def test_cant_access_location_invalid_list_item_id(self):
        schema = load_schema_from_name("test_textfield")
        router = Router(
            schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        current_location = Location(section_id="default-section", block_id="name-block")
        routing_path = []
        can_access_location = router.can_access_location(current_location, routing_path)

        self.assertFalse(can_access_location)

    def test_cant_access_location_not_on_allowable_path(self):
        schema = load_schema_from_name("test_unit_patterns")

        router = Router(
            schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        current_location = Location(
            section_id="default-section", block_id="set-duration-units-block"
        )
        routing_path = RoutingPath(
            [
                "set-length-units-block",
                "set-duration-units-block",
                "set-area-units-block",
                "set-volume-units-block",
            ],
            section_id="default-section",
        )

        can_access_location = router.can_access_location(current_location, routing_path)
        self.assertFalse(can_access_location)

    def test_next_location_url(self):
        schema = load_schema_from_name("test_checkbox")
        progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.IN_PROGRESS,
                    "block_ids": ["mandatory-checkbox"],
                }
            ]
        )

        router = Router(
            schema, self.answer_store, self.list_store, progress_store, self.metadata
        )

        current_location = Location(
            section_id="default-section", block_id="mandatory-checkbox"
        )
        routing_path = RoutingPath(
            ["mandatory-checkbox", "non-mandatory-checkbox", "single-checkbox"],
            section_id="default-section",
        )
        next_location = router.get_next_location_url(current_location, routing_path)
        expected_location = Location(
            section_id="default-section", block_id="non-mandatory-checkbox"
        ).url()

        self.assertEqual(next_location, expected_location)

    def test_return_to_section_summary_next_location_url(self):
        schema = load_schema_from_name("test_section_summary")
        progress_store = ProgressStore(
            [
                {
                    "section_id": "property-details-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["insurance-type", "insurance-address"],
                }
            ]
        )

        router = Router(
            schema, self.answer_store, self.list_store, progress_store, self.metadata
        )

        current_location = Location(
            section_id="property-details-section", block_id="insurance-type"
        )
        routing_path = RoutingPath(
            ["insurance-type", "insurance-address"], section_id="default-section"
        )
        next_location = router.get_next_location_url(
            current_location, routing_path, return_to="section-summary"
        )

        self.assertIn(
            "/questionnaire/sections/property-details-section/", next_location
        )

    def test_linear_questionnaire_get_next_location_url_routes_to_submit_page_when_questionnaire_completed(
        self,
    ):
        schema = load_schema_from_name("test_textfield")
        progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["name-block"],
                }
            ]
        )

        router = Router(
            schema, self.answer_store, self.list_store, progress_store, self.metadata
        )
        current_location = Location(section_id="default-section", block_id="name-block")
        routing_path = RoutingPath(["name-block"], section_id="default-section")
        next_location = router.get_next_location_url(current_location, routing_path)

        self.assertEqual(url_for("questionnaire.submit"), next_location)

    def test_return_to_final_summary_next_location_url_questionnaire_complete(self):
        schema = load_schema_from_name("test_textfield")
        progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["name-block"],
                }
            ]
        )

        router = Router(
            schema, self.answer_store, self.list_store, progress_store, self.metadata
        )
        current_location = Location(section_id="default-section", block_id="name-block")
        routing_path = RoutingPath(["name-block"], section_id="default-section")
        next_location = router.get_next_location_url(
            current_location, routing_path, return_to="final-summary"
        )

        self.assertEqual(url_for("questionnaire.submit"), next_location)

    def test_return_to_final_summary_next_location_url_questionnaire_incomplete(self):
        schema = load_schema_from_name(
            "test_skipping_to_questionnaire_end_multiple_sections"
        )
        answer_store = AnswerStore(
            [{"answer_id": "test-skipping-answer", "value": "Yes"}]
        )
        progress_store = ProgressStore(
            [
                {
                    "section_id": "test-skipping-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["test-skipping-forced"],
                }
            ]
        )

        router = Router(
            schema, answer_store, self.list_store, progress_store, self.metadata
        )
        current_location = Location(
            section_id="test-skipping-section", block_id="test-skipping-forced"
        )
        routing_path = RoutingPath(
            ["test-skipping-forced"], section_id="test-skipping-section"
        )
        next_location = router.get_next_location_url(
            current_location, routing_path, return_to="final-summary"
        )
        expected_location = Location(
            section_id="test-skipping-section-2",
            block_id="test-skipping-optional",
            list_item_id=None,
        )

        self.assertEqual(expected_location.url(), next_location)

    def test_return_to_first_incomplete_location_when_last_block_in_section_in_progress(
        self,
    ):
        schema = Mock()
        schema.get_block.return_value = {"type": "Question"}
        progress_store = ProgressStore(
            [
                {
                    "section_id": "section-1",
                    "list_item_id": None,
                    "status": CompletionStatus.IN_PROGRESS,
                    "block_ids": ["block-1"],
                }
            ]
        )
        router = Router(
            schema, self.answer_store, self.list_store, progress_store, self.metadata
        )
        current_location = Location(section_id="section-1", block_id="block-1")
        routing_path = RoutingPath(
            ["block-1", "block-2", "block-1"], section_id="section-1"
        )
        next_location = router.get_next_location_url(current_location, routing_path)
        self.assertIn("questionnaire/block-2/", next_location)

    def test_last_block_section_summary_on_completion_true_next_location_url(self):
        schema = load_schema_from_name("test_show_section_summary_on_completion")
        progress_store = ProgressStore(
            [
                {
                    "section_id": "accommodation-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["proxy"],
                }
            ]
        )
        router = Router(
            schema, self.answer_store, self.list_store, progress_store, self.metadata
        )
        current_location = Location(
            section_id="accommodation-section", block_id="proxy"
        )
        routing_path = RoutingPath(["proxy"], section_id="default-section")
        next_location = router.get_next_location_url(current_location, routing_path)

        self.assertIn("questionnaire/sections/accommodation-section/", next_location)

    def test_last_block_section_summary_on_completion_false_next_location_url(self):
        schema = load_schema_from_name("test_show_section_summary_on_completion")
        progress_store = ProgressStore(
            [
                {
                    "section_id": "employment-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["employment-status"],
                }
            ]
        )
        router = Router(
            schema, self.answer_store, self.list_store, progress_store, self.metadata
        )
        current_location = Location(
            section_id="employment-section", block_id="employment-type"
        )
        routing_path = RoutingPath(
            ["employment-status", "employment-type"], section_id="employment-section"
        )
        next_location = router.get_next_location_url(current_location, routing_path)
        expected_location_url = url_for("questionnaire.get_questionnaire")

        self.assertEqual(next_location, expected_location_url)

    def test_last_block_no_section_summary_next_location_url_is_submit_page(self):
        schema = load_schema_from_name("test_checkbox")
        progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": [
                        "mandatory-checkbox",
                        "non-mandatory-checkbox",
                        "single-checkbox",
                    ],
                }
            ]
        )
        router = Router(
            schema, self.answer_store, self.list_store, progress_store, self.metadata
        )
        current_location = Location(
            section_id="default-section", block_id="single-checkbox"
        )
        routing_path = RoutingPath(
            ["mandatory-checkbox", "non-mandatory-checkbox", "single-checkbox"],
            section_id="default-section",
        )
        next_location = router.get_next_location_url(current_location, routing_path)

        self.assertEqual(url_for("questionnaire.submit"), next_location)

    def test_previous_location_url_on_question_page(self):
        schema = load_schema_from_name("test_checkbox")

        router = Router(
            schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        current_location = Location(
            section_id="default-section", block_id="non-mandatory-checkbox"
        )

        routing_path = RoutingPath(
            ["mandatory-checkbox", "non-mandatory-checkbox"],
            section_id="default-section",
        )
        previous_location_url = router.get_previous_location_url(
            current_location, routing_path
        )
        expected_location_url = Location(
            section_id="default-section", block_id="mandatory-checkbox"
        ).url()

        self.assertEqual(previous_location_url, expected_location_url)

    def test_previous_location_on_first_block_with_hub_enabled(self):
        schema = load_schema_from_name("test_hub_and_spoke")

        router = Router(
            schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        current_location = Location(
            section_id="employment-section", block_id="employment-status"
        )

        routing_path = RoutingPath(
            ["employment-status", "employment-type"], section_id="employment-section"
        )
        previous_location_url = router.get_previous_location_url(
            current_location, routing_path
        )

        self.assertEqual(
            url_for("questionnaire.get_questionnaire"), previous_location_url
        )

    def test_previous_location_with_hub_enabled(self):
        schema = load_schema_from_name("test_hub_and_spoke")

        router = Router(
            schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        current_location = Location(
            section_id="employment-section", block_id="employment-status"
        )
        routing_path = RoutingPath(
            ["employment-status", "employment-status"], section_id="employment-section"
        )
        previous_location_url = router.get_previous_location_url(
            current_location, routing_path
        )
        expected_location_url = url_for("questionnaire.get_questionnaire")

        self.assertEqual(previous_location_url, expected_location_url)

    def test_is_path_complete(self):
        schema = load_schema_from_name("test_textfield")
        progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.IN_PROGRESS,
                    "block_ids": ["name-block"],
                }
            ]
        )

        router = Router(
            schema, self.answer_store, self.list_store, progress_store, self.metadata
        )

        routing_path = router.routing_path(section_id="default-section")

        is_path_complete = router.is_path_complete(routing_path)

        self.assertTrue(is_path_complete)

    def test_is_path_not_complete(self):
        schema = load_schema_from_name("test_textfield")

        router = Router(
            schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        routing_path = router.routing_path(section_id="default-section")

        is_path_complete = router.is_path_complete(routing_path)

        self.assertFalse(is_path_complete)

    def test_is_survey_complete(self):
        schema = load_schema_from_name("test_textfield")
        progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["name-block"],
                }
            ]
        )

        router = Router(
            schema, self.answer_store, self.list_store, progress_store, self.metadata
        )

        is_survey_complete = router.is_questionnaire_complete

        self.assertTrue(is_survey_complete)

    def test_is_survey_not_complete(self):
        schema = load_schema_from_name("test_textfield")

        router = Router(
            schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        is_survey_complete = router.is_questionnaire_complete

        self.assertFalse(is_survey_complete)

    def test_is_survey_not_complete_with_repeating_sections(self):
        schema = load_schema_from_name("test_repeating_sections_with_hub_and_spoke")

        progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["mandatory-checkbox", "non-mandatory-checkbox"],
                }
            ]
        )

        list_store = ListStore(
            [
                {
                    "items": ["abc123", "123abc"],
                    "name": "people",
                    "primary_person": "abc123",
                }
            ]
        )

        router = Router(
            schema, self.answer_store, list_store, progress_store, self.metadata
        )

        is_survey_complete = router.is_questionnaire_complete

        self.assertFalse(is_survey_complete)

    def test_is_survey_complete_with_repeating_sections(self):
        schema = load_schema_from_name("test_repeating_sections_with_hub_and_spoke")

        progress_store = ProgressStore(
            [
                {
                    "section_id": "section",
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": [
                        "primary-person-list-collector",
                        "list-collector",
                        "next-interstitial",
                        "another-list-collector-block",
                    ],
                },
                {
                    "section_id": "personal-details-section",
                    "status": CompletionStatus.COMPLETED,
                    "list_item_id": "abc123",
                    "block_ids": ["proxy", "date-of-birth", "confirm-dob", "sex"],
                },
            ]
        )

        list_store = ListStore(
            [{"items": ["abc123"], "name": "people", "primary_person": "abc123"}]
        )

        router = Router(
            schema, self.answer_store, list_store, progress_store, self.metadata
        )

        is_survey_complete = router.is_questionnaire_complete

        self.assertTrue(is_survey_complete)

    def test_is_survey_complete_summary_in_own_section(self):
        schema = load_schema_from_name("test_placeholder_full")

        progress_store = ProgressStore(
            [
                {
                    "section_id": "name-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["name-question"],
                },
                {
                    "section_id": "age-input-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["dob-question-block"],
                },
                {
                    "section_id": "age-confirmation-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["confirm-dob-proxy"],
                },
                {
                    "section_id": "mutually-exclusive-checkbox-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["mutually-exclusive-checkbox"],
                },
            ]
        )

        router = Router(
            schema, self.answer_store, self.list_store, progress_store, self.metadata
        )

        is_survey_complete = router.is_questionnaire_complete

        self.assertTrue(is_survey_complete)

    def test_get_first_incomplete_location_url_in_section(self):
        schema = load_schema_from_name("test_section_summary")

        progress_store = ProgressStore(
            [
                {
                    "section_id": "property-details-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["insurance-type"],
                }
            ]
        )

        router = Router(
            schema, self.answer_store, self.list_store, progress_store, self.metadata
        )

        section_routing_path = RoutingPath(
            ["insurance-type", "insurance-address"],
            section_id="property-details-section",
        )

        section_resume_url = router.get_section_resume_url(
            routing_path=section_routing_path
        )

        self.assertEqual(
            section_resume_url,
            "http://test.localdomain/questionnaire/insurance-address/?resume=True",
        )

    def test_get_section_return_location_url_when_section_complete_no_section_summary(
        self,
    ):
        schema = load_schema_from_name("test_hub_and_spoke")

        router = Router(
            schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        routing_path = RoutingPath(
            ["employment-status", "employment-type"], section_id="employment-section"
        )

        section_resume_url = router.get_section_resume_url(routing_path=routing_path)

        self.assertEqual(
            section_resume_url,
            "http://test.localdomain/questionnaire/employment-status/",
        )

    def test_enabled_section_ids(self):
        schema = load_schema_from_name("test_section_enabled_checkbox")
        progress_store = ProgressStore(
            [
                {
                    "section_id": "section-1",
                    "block_ids": ["section-1-block"],
                    "status": "COMPLETED",
                }
            ]
        )

        answer_store = AnswerStore(
            [{"answer_id": "section-1-answer", "value": ["Section 2"]}]
        )
        router = Router(
            schema=schema,
            answer_store=answer_store,
            list_store=ListStore(),
            progress_store=progress_store,
            metadata={},
        )

        expected_section_ids = ["section-1", "section-2"]

        self.assertEqual(router.enabled_section_ids, expected_section_ids)

    def test_full_routing_path_without_repeating_sections(self):
        schema = load_schema_from_name("test_checkbox")

        router = Router(
            schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        routing_path = router.full_routing_path()

        expected_path = [
            RoutingPath(
                [
                    "mandatory-checkbox",
                    "non-mandatory-checkbox",
                    "single-checkbox",
                ],
                section_id="default-section",
            )
        ]

        self.assertEqual(routing_path, expected_path)

    def test_full_routing_path_with_repeating_sections(self):
        schema = load_schema_from_name("test_repeating_sections_with_hub_and_spoke")

        list_store = ListStore(
            [
                {
                    "items": ["abc123", "123abc"],
                    "name": "people",
                    "primary_person": "abc123",
                }
            ]
        )

        router = Router(
            schema, self.answer_store, list_store, self.progress_store, self.metadata
        )

        routing_path = router.full_routing_path()

        expected_path = [
            RoutingPath(
                [
                    "primary-person-list-collector",
                    "list-collector",
                    "next-interstitial",
                    "another-list-collector-block",
                    "visitors-block",
                ],
                section_id="section",
                list_name=None,
                list_item_id=None,
            ),
            RoutingPath(
                ["proxy", "date-of-birth", "confirm-dob", "sex"],
                section_id="personal-details-section",
                list_name="people",
                list_item_id="abc123",
            ),
            RoutingPath(
                ["proxy", "date-of-birth", "confirm-dob", "sex"],
                section_id="personal-details-section",
                list_name="people",
                list_item_id="123abc",
            ),
        ]

        self.assertEqual(routing_path, expected_path)
