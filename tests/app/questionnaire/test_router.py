from flask import url_for

from app.data_model.answer_store import AnswerStore
from app.data_model.list_store import ListStore
from app.data_model.progress_store import ProgressStore, CompletionStatus
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
        routing_path = RoutingPath(
            ["name-block", "summary"], section_id="default-section"
        )

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
                "summary",
            ],
            section_id="default-section",
        )

        can_access_location = router.can_access_location(current_location, routing_path)
        self.assertFalse(can_access_location)

    def test_next_location_url(self):
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
        routing_path = RoutingPath(
            ["name-block", "summary"], section_id="default-section"
        )
        next_location = router.get_next_location_url(current_location, routing_path)
        expected_location = Location(
            section_id="default-section", block_id="summary"
        ).url()

        self.assertEqual(next_location, expected_location)

    def test_previous_location_url(self):
        schema = load_schema_from_name("test_textfield")

        router = Router(
            schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        current_location = Location(section_id="default-section", block_id="summary")

        routing_path = RoutingPath(
            ["name-block", "summary"], section_id="default-section"
        )
        previous_location_url = router.get_previous_location_url(
            current_location, routing_path
        )
        expected_location_url = Location(
            section_id="default-section", block_id="name-block"
        ).url()

        self.assertEqual(previous_location_url, expected_location_url)

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

        is_survey_complete = router.is_survey_complete()

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

        is_survey_complete = router.is_survey_complete()

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

        is_survey_complete = router.is_survey_complete()

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

        is_survey_complete = router.is_survey_complete()

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

        is_survey_complete = router.is_survey_complete()

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

        expected_section_ids = ["section-1", "section-2", "summary-section"]

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
                ["mandatory-checkbox", "non-mandatory-checkbox", "summary"],
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
