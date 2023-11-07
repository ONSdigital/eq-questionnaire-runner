# pylint: disable=too-many-lines
from functools import cached_property

import pytest
from flask import url_for
from mock import Mock

from app.data_models import CompletionStatus
from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress import ProgressDict
from app.data_models.progress_store import ProgressStore
from app.data_models.supplementary_data_store import SupplementaryDataStore
from app.questionnaire.location import Location, SectionKey
from app.questionnaire.return_location import ReturnLocation
from app.questionnaire.router import Router
from app.questionnaire.routing_path import RoutingPath
from app.utilities.schema import load_schema_from_name
from tests.app.questionnaire.conftest import get_metadata


class RouterTestCase:
    schema = None
    answer_store = AnswerStore()
    list_store = ListStore()
    progress_store = ProgressStore()
    metadata = get_metadata()
    supplementary_data_store = SupplementaryDataStore()
    response_metadata = {}

    @cached_property
    def router(self):
        return Router(
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
            self.response_metadata,
            self.supplementary_data_store,
        )


class TestRouter(RouterTestCase):
    def test_enabled_section_ids(self):
        self.schema = load_schema_from_name("test_section_enabled_checkbox")
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="section-1",
                    block_ids=["section-1-block"],
                    status=CompletionStatus.COMPLETED,
                )
            ]
        )
        self.answer_store = AnswerStore(
            [{"answer_id": "section-1-answer", "value": ["Section 2"]}]
        )

        expected_section_ids = ["section-1", "section-2"]

        assert expected_section_ids == self.router.enabled_section_ids

    def test_full_routing_path_without_repeating_sections(self):
        self.schema = load_schema_from_name("test_checkbox")
        routing_path = self.router.full_routing_path()

        expected_path = [
            RoutingPath(
                block_ids=[
                    "mandatory-checkbox",
                    "non-mandatory-checkbox",
                    "single-checkbox",
                ],
                section_id="default-section",
            )
        ]

        assert expected_path == routing_path

    def test_full_routing_path_with_repeating_sections(self):
        self.schema = load_schema_from_name(
            "test_repeating_sections_with_hub_and_spoke"
        )
        self.list_store = ListStore(
            [
                {
                    "items": ["abc123", "123abc"],
                    "name": "people",
                    "primary_person": "abc123",
                }
            ]
        )

        routing_path = self.router.full_routing_path()

        expected_path = [
            RoutingPath(
                block_ids=[
                    "primary-person-list-collector",
                    "list-collector",
                    "next-interstitial",
                    "another-list-collector-block",
                    "visitors-block",
                ],
                section_id="section",
            ),
            RoutingPath(
                block_ids=["proxy", "date-of-birth", "confirm-dob", "sex"],
                section_id="personal-details-section",
                list_name="people",
                list_item_id="abc123",
            ),
            RoutingPath(
                block_ids=["proxy", "date-of-birth", "confirm-dob", "sex"],
                section_id="personal-details-section",
                list_name="people",
                list_item_id="123abc",
            ),
        ]

        assert expected_path == routing_path


class TestRouterPathCompletion(RouterTestCase):
    def test_is_complete(self):
        self.schema = load_schema_from_name("test_textfield")
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="default-section",
                    list_item_id=None,
                    status=CompletionStatus.IN_PROGRESS,
                    block_ids=["name-block"],
                )
            ]
        )

        routing_path = self.router.routing_path(SectionKey("default-section"))
        is_path_complete = self.router.is_path_complete(routing_path)

        assert is_path_complete

    def test_is_not_complete(self):
        self.schema = load_schema_from_name("test_textfield")

        routing_path = self.router.routing_path(SectionKey("default-section"))
        is_path_complete = self.router.is_path_complete(routing_path)

        assert not is_path_complete


class TestRouterQuestionnaireCompletion(RouterTestCase):
    def test_is_complete(self):
        self.schema = load_schema_from_name("test_textfield")
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="default-section",
                    list_item_id=None,
                    status=CompletionStatus.COMPLETED,
                    block_ids=["name-block"],
                )
            ]
        )

        is_questionnaire_complete = self.router.is_questionnaire_complete

        assert is_questionnaire_complete

    def test_is_not_complete(self):
        self.schema = load_schema_from_name("test_textfield")

        is_questionnaire_complete = self.router.is_questionnaire_complete

        assert not is_questionnaire_complete

    def test_is_complete_with_repeating_sections(self):
        self.schema = load_schema_from_name(
            "test_repeating_sections_with_hub_and_spoke"
        )
        self.progress_store = ProgressStore(
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
        self.list_store = ListStore(
            [{"items": ["abc123"], "name": "people", "primary_person": "abc123"}]
        )

        is_questionnaire_complete = self.router.is_questionnaire_complete

        assert is_questionnaire_complete

    def test_is_not_complete_with_repeating_sections(self):
        self.schema = load_schema_from_name(
            "test_repeating_sections_with_hub_and_spoke"
        )
        self.progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["mandatory-checkbox", "non-mandatory-checkbox"],
                }
            ]
        )
        self.list_store = ListStore(
            [
                {
                    "items": ["abc123", "123abc"],
                    "name": "people",
                    "primary_person": "abc123",
                }
            ]
        )

        is_questionnaire_complete = self.router.is_questionnaire_complete

        assert not is_questionnaire_complete


class TestRouterLocationValidity(RouterTestCase):
    def test_can_access(self):
        self.schema = load_schema_from_name("test_textfield")

        current_location = Location(section_id="default-section", block_id="name-block")
        routing_path = RoutingPath(
            block_ids=["name-block"], section_id="default-section"
        )
        can_access_location = self.router.can_access_location(
            current_location, routing_path
        )

        assert can_access_location

    def test_can_access_with_list_name_and_list_name_id(self):
        self.schema = load_schema_from_name("test_textfield")

        current_location = Location(
            section_id="default-section",
            block_id="name-block",
            list_name="default-list",
            list_item_id="default-list-id",
        )
        routing_path = RoutingPath(
            block_ids=["name-block"], section_id="default-section"
        )
        can_access_location = self.router.can_access_location(
            current_location, routing_path
        )

        assert not can_access_location

    def test_cant_access(self):
        self.schema = load_schema_from_name(
            "test_repeating_sections_with_hub_and_spoke"
        )

        self.list_store = ListStore(
            [
                {
                    "items": ["abc123", "123abc"],
                    "name": "people",
                    "primary_person": "abc123",
                }
            ]
        )

        current_location = Location(
            section_id="personal-details-section",
            block_id="proxy",
            list_item_id="invalid-list-item-id",
        )
        can_access_location = self.router.can_access_location(
            current_location, routing_path=[]
        )

        assert not can_access_location

    def test_cant_access_section_disabled(self):
        self.schema = load_schema_from_name("test_section_enabled_checkbox")

        current_location = Location(
            section_id="section-2", block_id="section-2-block", list_item_id=None
        )
        can_access_location = self.router.can_access_location(
            current_location, routing_path=[]
        )

        assert not can_access_location

    def test_cant_access_invalid_list_item_id(self):
        self.schema = load_schema_from_name("test_textfield")

        current_location = Location(section_id="default-section", block_id="name-block")
        can_access_location = self.router.can_access_location(
            current_location, routing_path=[]
        )

        assert not can_access_location

    def test_cant_access_not_on_allowable_path(self):
        self.schema = load_schema_from_name("test_unit_patterns")

        current_location = Location(
            section_id="default-section", block_id="set-duration-units-block"
        )
        routing_path = RoutingPath(
            block_ids=[
                "set-length-units-block",
                "set-duration-units-block",
                "set-area-units-block",
                "set-volume-units-block",
            ],
            section_id="default-section",
        )
        can_access_location = self.router.can_access_location(
            current_location, routing_path
        )

        assert not can_access_location


class TestRouterNextLocation(RouterTestCase):
    @pytest.mark.usefixtures("app")
    def test_within_section(self):
        self.schema = load_schema_from_name("test_checkbox")
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="default-section",
                    list_item_id=None,
                    status=CompletionStatus.IN_PROGRESS,
                    block_ids=["mandatory-checkbox"],
                )
            ]
        )

        current_location = Location(
            section_id="default-section", block_id="mandatory-checkbox"
        )
        routing_path = RoutingPath(
            block_ids=[
                "mandatory-checkbox",
                "non-mandatory-checkbox",
                "single-checkbox",
            ],
            section_id="default-section",
        )
        return_location = ReturnLocation()

        next_location = self.router.get_next_location_url(
            current_location,
            routing_path,
            return_location,
        )

        expected_location = Location(
            section_id="default-section", block_id="non-mandatory-checkbox"
        ).url()

        assert expected_location == next_location

    @pytest.mark.usefixtures("app")
    def test_last_block_in_section_but_section_is_not_complete_when_routing_backwards(
        self,
    ):
        self.schema = Mock()
        self.schema.get_block.return_value = {"type": "Question"}
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="section-1",
                    list_item_id=None,
                    status=CompletionStatus.IN_PROGRESS,
                    block_ids=["block-1"],
                )
            ]
        )
        current_location = Location(section_id="section-1", block_id="block-1")
        # Simulates routing backwards. Last block in section does not mean section is complete.
        routing_path = RoutingPath(
            block_ids=["block-1", "block-2", "block-1"], section_id="section-1"
        )
        return_location = ReturnLocation()

        next_location = self.router.get_next_location_url(
            current_location,
            routing_path,
            return_location,
        )

        assert "questionnaire/block-2/" in next_location

    @pytest.mark.usefixtures("app")
    def test_return_to_section_summary_section_is_complete(self):
        self.schema = load_schema_from_name("test_section_summary")
        self.progress_store = ProgressStore(
            [
                {
                    "section_id": "property-details-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": [
                        "insurance-type",
                        "insurance-address",
                        "listed",
                    ],
                }
            ]
        )

        current_location = Location(
            section_id="property-details-section", block_id="insurance-type"
        )
        routing_path = RoutingPath(
            block_ids=["insurance-type", "insurance-address", "listed"],
            section_id="property-details-section",
        )
        return_location = ReturnLocation(return_to="section-summary")

        next_location = self.router.get_next_location_url(
            current_location, routing_path, return_location
        )

        assert "/questionnaire/sections/property-details-section/" in next_location

    @pytest.mark.usefixtures("app")
    def test_return_to_section_summary_section_is_in_progress(self):
        self.schema = load_schema_from_name("test_section_summary")
        self.answer_store = AnswerStore(
            [
                {"answer_id": "insurance-type-answer", "value": "Both"},
                {"answer_id": "insurance-address-answer", "value": "Address"},
                {"answer_id": "listed-answer", "value": "No"},
            ]
        )
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="property-details-section",
                    list_item_id=None,
                    status=CompletionStatus.IN_PROGRESS,
                    block_ids=["insurance-type", "insurance-address", "listed"],
                )
            ]
        )
        current_location = Location(
            section_id="property-details-section", block_id="insurance-address"
        )
        routing_path = RoutingPath(
            block_ids=[
                "insurance-type",
                "insurance-address",
                "address-duration",
                "listed",
            ],
            section_id="property-details-section",
        )
        return_location = ReturnLocation(return_to="section-summary")

        next_location = self.router.get_next_location_url(
            current_location, routing_path, return_location
        )

        assert (
            "/questionnaire/address-duration/?return_to=section-summary"
            in next_location
        )

    @pytest.mark.usefixtures("app")
    def test_section_summary_on_completion_true(self):
        self.schema = load_schema_from_name("test_show_section_summary_on_completion")
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="accommodation-section",
                    list_item_id=None,
                    status=CompletionStatus.COMPLETED,
                    block_ids=["proxy"],
                )
            ]
        )
        current_location = Location(
            section_id="accommodation-section", block_id="proxy"
        )
        routing_path = RoutingPath(block_ids=["proxy"], section_id="default-section")

        return_location = ReturnLocation()

        next_location = self.router.get_next_location_url(
            current_location, routing_path, return_location
        )

        assert "questionnaire/sections/accommodation-section/" in next_location

    @pytest.mark.usefixtures("app")
    def test_section_summary_on_completion_false(self):
        self.schema = load_schema_from_name("test_show_section_summary_on_completion")
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="employment-section",
                    list_item_id=None,
                    status=CompletionStatus.COMPLETED,
                    block_ids=["employment-status"],
                )
            ]
        )
        current_location = Location(
            section_id="employment-section", block_id="employment-type"
        )
        routing_path = RoutingPath(
            block_ids=["employment-status", "employment-type"],
            section_id="employment-section",
        )
        return_location = ReturnLocation()

        next_location = self.router.get_next_location_url(
            current_location, routing_path, return_location
        )
        expected_location_url = url_for("questionnaire.get_questionnaire")

        assert expected_location_url == next_location

    @pytest.mark.usefixtures("app")
    @pytest.mark.parametrize(
        "schema",
        ("test_calculated_summary",),
    )
    def test_return_to_calculated_summary(self, schema):
        """
        This tests that when you hit continue on an edited answer for a calculated summary and all other dependent answers are complete
        you are routed to the calculated summary, anchored to the answer that you edited
        """
        self.schema = load_schema_from_name(schema)
        # for the purposes of this test, assume the routing path consists only of the first two blocks and the calculated summary
        # and that those two blocks are complete - this will be a sufficient condition to return to the calculated summary
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="default-section",
                    block_ids=[
                        "first-number-block",
                        "second-number-block",
                    ],
                    status=CompletionStatus.IN_PROGRESS,
                )
            ]
        )

        current_location = Location(
            section_id="default-section", block_id="second-number-block"
        )

        routing_path = RoutingPath(
            block_ids=[
                "first-number-block",
                "second-number-block",
                "currency-total-playback",
            ],
            section_id="default-section",
        )

        return_location = ReturnLocation(
            return_to_answer_id="first-number-answer",
            return_to="calculated-summary",
            return_to_block_id="currency-total-playback",
        )

        next_location_url = self.router.get_next_location_url(
            current_location, routing_path, return_location
        )

        expected_location = Location(
            section_id="default-section",
            block_id="currency-total-playback",
        )

        expected_location_url = url_for(
            "questionnaire.block",
            list_item_id=expected_location.list_item_id,
            block_id=expected_location.block_id,
            _anchor="first-number-answer",
        )

        assert expected_location_url == next_location_url

    @pytest.mark.usefixtures("app")
    @pytest.mark.parametrize(
        "schema",
        (
            "test_calculated_summary_dependent_questions",
            "test_new_calculated_summary_dependent_questions",
        ),
    )
    def test_return_to_calculated_summary_not_on_allowable_path(self, schema):
        """
        This tests that if you try to return to a calculated summary before all its dependencies have been answered
        then you are instead routed to the first incomplete block of the section
        """
        self.schema = load_schema_from_name(schema)
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="default-section",
                    block_ids=["block-3"],
                    status=CompletionStatus.IN_PROGRESS,
                )
            ]
        )

        current_location = Location(section_id="default-section", block_id="block-3")

        # block 3 is complete, and block 4 is not, so block 4 should be routed to before the calculated summary
        routing_path = RoutingPath(
            block_ids=[
                "block-3",
                "block-4",
                "calculated-summary-block",
            ],
            section_id="default-section",
        )

        return_location = ReturnLocation(
            return_to_answer_id="answer-3",
            return_to="calculated-summary",
            return_to_block_id="calculated-summary-block",
        )

        next_location_url = self.router.get_next_location_url(
            current_location,
            routing_path,
            return_location,
        )

        expected_location = Location(
            section_id="default-section",
            block_id="block-4",
        )

        expected_location_url = url_for(
            "questionnaire.block",
            list_item_id=expected_location.list_item_id,
            block_id=expected_location.block_id,
            return_to=return_location.return_to,
            return_to_block_id=return_location.return_to_block_id,
            return_to_answer_id=return_location.return_to_answer_id,
        )

        assert expected_location_url == next_location_url

    @pytest.mark.usefixtures("app")
    @pytest.mark.parametrize(
        "schema, return_to_block_id, expected_url",
        [
            (
                "test_calculated_summary",
                "non-valid-block",
                "/questionnaire/sixth-number-block/?return_to=calculated-summary&return_to_block_id=non-valid-block",
            ),
            (
                "test_calculated_summary",
                None,
                "/questionnaire/sixth-number-block/?return_to=calculated-summary",
            ),
        ],
    )
    def test_return_to_calculated_summary_invalid_return_to_block_id(
        self, schema, return_to_block_id, expected_url
    ):
        self.schema = load_schema_from_name(schema)
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="default-section",
                    block_ids=["fifth-number-block"],
                    status=CompletionStatus.IN_PROGRESS,
                )
            ]
        )

        current_location = Location(
            section_id="default-section", block_id="fifth-number-block"
        )

        routing_path = RoutingPath(
            block_ids=["fifth-number-block", "sixth-number-block"],
            section_id="default-section",
        )

        return_location = ReturnLocation(
            return_to="calculated-summary",
            return_to_block_id=return_to_block_id,
        )
        next_location_url = self.router.get_next_location_url(
            current_location,
            routing_path,
            return_location,
        )

        assert expected_url == next_location_url

    @pytest.mark.usefixtures("app")
    @pytest.mark.parametrize(
        "schema",
        ("test_calculated_summary",),
    )
    def test_return_to_calculated_summary_return_to_block_id_not_on_path(self, schema):
        self.schema = load_schema_from_name(schema)
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="default-section",
                    block_ids=["fifth-number-block"],
                    status=CompletionStatus.IN_PROGRESS,
                )
            ]
        )

        current_location = Location(
            section_id="default-section", block_id="fifth-number-block"
        )

        routing_path = RoutingPath(
            block_ids=["fifth-number-block", "sixth-number-block"],
            section_id="default-section",
        )

        return_location = ReturnLocation(
            return_to="calculated-summary",
            return_to_block_id="fourth-number-block",
        )

        next_location_url = self.router.get_next_location_url(
            current_location, routing_path, return_location
        )

        # return_to_block_id is still passed here as although it is not currently on the path it may be in future once incomplete questions are
        # answered so needs to be preserved
        assert (
            "/questionnaire/sixth-number-block/?return_to=calculated-summary&return_to_block_id=fourth-number-block"
            == next_location_url
        )

    @pytest.mark.usefixtures("app")
    def test_return_to_grand_calculated_summary_from_answer(
        self, grand_calculated_summary_progress_store, grand_calculated_summary_schema
    ):
        """
        If going from GCS ->  CS -> answer -> CS -> GCS this tests going from CS -> GCS having just come from an answer
        """
        self.schema = grand_calculated_summary_schema
        self.progress_store = grand_calculated_summary_progress_store

        current_location = Location(
            section_id="section-1", block_id="first-number-block"
        )

        routing_path = RoutingPath(
            block_ids=["distance-calculated-summary-1"],
            section_id="section-1",
        )

        return_location = ReturnLocation(
            return_to="calculated-summary,grand-calculated-summary",
            return_to_answer_id="distance-calculated-summary-1",
            return_to_block_id="distance-calculated-summary-1,distance-grand-calculated-summary",
        )

        next_location_url = self.router.get_next_location_url(
            current_location, routing_path, return_location
        )

        expected_previous_url = url_for(
            "questionnaire.block",
            return_to="grand-calculated-summary",
            block_id="distance-calculated-summary-1",
            return_to_block_id="distance-grand-calculated-summary",
            _anchor="distance-calculated-summary-1",
        )

        assert expected_previous_url == next_location_url

    @pytest.mark.usefixtures("app")
    def test_return_to_calculated_summary_from_answer_when_multiple_answers(self):
        """
        If going from GCS ->  CS -> answer -> CS -> GCS this tests going from CS -> GCS having just come from an answer
        """
        self.schema = load_schema_from_name(
            "test_grand_calculated_summary_overlapping_answers"
        )
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="introduction-section",
                    block_ids=[
                        "introduction-block",
                    ],
                    status=CompletionStatus.COMPLETED,
                ),
                ProgressDict(
                    section_id="section-1",
                    block_ids=[
                        "block-1",
                        "block-2",
                        "calculated-summary-1",
                        "calculated-summary-2",
                        "block-3",
                        "calculated-summary-3",
                    ],
                    status=CompletionStatus.COMPLETED,
                ),
            ]
        )

        current_location = Location(section_id="section-1", block_id="block-1")

        routing_path = RoutingPath(
            block_ids=[
                "block-1",
                "block-2",
                "calculated-summary-1",
                "calculated-summary-2",
                "block-3",
                "calculated-summary-3",
            ],
            section_id="section-1",
        )

        return_location = ReturnLocation(
            return_to="calculated-summary,grand-calculated-summary",
            return_to_answer_id="q1-a1,calculated-summary-1",
            return_to_block_id="calculated-summary-1,grand-calculated-summary-shopping",
        )

        next_location_url = self.router.get_next_location_url(
            current_location, routing_path, return_location
        )

        assert (
            next_location_url
            == "/questionnaire/calculated-summary-1/?return_to=grand-calculated-summary&return_to_block_id=grand-calculated-summary-shopping&"
               "return_to_answer_id=calculated-summary-1#q1-a1"
        )

    @pytest.mark.usefixtures("app")
    def test_return_to_grand_calculated_summary_from_answer_when_multiple_answers(self):
        """
        If going from GCS ->  CS -> answer -> CS -> GCS this tests going from CS -> GCS having just come from an answer
        """
        self.schema = load_schema_from_name(
            "test_grand_calculated_summary_overlapping_answers"
        )
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="introduction-section",
                    block_ids=[
                        "introduction-block",
                    ],
                    status=CompletionStatus.COMPLETED,
                ),
                ProgressDict(
                    section_id="section-1",
                    block_ids=[
                        "block-1",
                        "block-2",
                        "calculated-summary-1",
                        "calculated-summary-2",
                        "block-3",
                        "calculated-summary-3",
                    ],
                    status=CompletionStatus.COMPLETED,
                ),
            ]
        )

        current_location = Location(
            section_id="section-1", block_id="calculated-summary-1"
        )

        routing_path = RoutingPath(
            block_ids=[
                "block-1",
                "block-2",
                "calculated-summary-1",
                "calculated-summary-2",
                "block-3",
                "calculated-summary-3",
            ],
            section_id="section-1",
        )

        return_location = ReturnLocation(
            return_to="grand-calculated-summary",
            return_to_answer_id="calculated-summary-1",
            return_to_block_id="grand-calculated-summary-shopping",
        )

        next_location_url = self.router.get_next_location_url(
            current_location, routing_path, return_location
        )

        assert (
            next_location_url
            == "/questionnaire/grand-calculated-summary-shopping/#calculated-summary-1"
        )

    @pytest.mark.usefixtures("app")
    def test_return_to_grand_calculated_summary_from_calculated_summary(
        self, grand_calculated_summary_progress_store, grand_calculated_summary_schema
    ):
        """
        If going from GCS ->  CS -> GCS this tests going from CS -> GCS having just come from the grand calculated summary
        """
        self.schema = grand_calculated_summary_schema
        self.progress_store = grand_calculated_summary_progress_store

        current_location = Location(
            section_id="section-1", block_id="distance-calculated-summary-1"
        )

        routing_path = RoutingPath(
            block_ids=["distance-calculated-summary-1"],
            section_id="section-1",
        )

        return_location = ReturnLocation(
            return_to="grand-calculated-summary",
            return_to_answer_id="distance-calculated-summary-1",
            return_to_block_id="distance-grand-calculated-summary",
        )
        next_location_url = self.router.get_next_location_url(
            current_location,
            routing_path,
            return_location,
        )

        expected_previous_url = url_for(
            "questionnaire.block",
            block_id="distance-grand-calculated-summary",
            _anchor="distance-calculated-summary-1",
        )

        assert expected_previous_url == next_location_url

    @pytest.mark.parametrize(
        "section_id,block_id,list_name,list_item_id,return_to_list_item_id",
        [
            (
                "base-costs-section",
                "calculated-summary-base-cost",
                None,
                None,
                "ZIrqqR",
            ),
            (
                "vehicle-details-section",
                "calculated-summary-running-costs",
                "vehicles",
                "ZIrqqR",
                None,
            ),
        ],
    )
    @pytest.mark.usefixtures("app")
    def test_return_to_repeating_grand_calculated_summary_from_calculated_summary(
        self,
        section_id,
        block_id,
        list_name,
        list_item_id,
        return_to_list_item_id,
        grand_calculated_summary_in_repeating_section_schema,
    ):
        """
        This tests that if you use a change link from a repeating GCS to return to:
        either a non-repeating CS in another section or a repeating CS in the same section,
        the continue button for the CS has a next location url of the original repeating GCS.
        """
        self.schema = grand_calculated_summary_in_repeating_section_schema
        self.list_store = ListStore([{"items": ["ZIrqqR"], "name": "vehicles"}])

        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="base-costs-section",
                    block_ids=[
                        "any-cost",
                        "finance-cost",
                        "calculated-summary-base-cost",
                    ],
                    status=CompletionStatus.COMPLETED,
                ),
                ProgressDict(
                    section_id="vehicle-details-section",
                    block_ids=[
                        "vehicle-maintenance-block",
                        "vehicle-fuel-block",
                        "calculated-summary-running-cost",
                        "grand-calculated-summary-vehicle",
                    ],
                    status=CompletionStatus.COMPLETED,
                    list_item_id="ZIrqqR",
                ),
            ]
        )
        current_location = Location(
            section_id=section_id,
            block_id=block_id,
            list_name=list_name,
            list_item_id=list_item_id,
        )
        routing_path = RoutingPath(
            block_ids=[
                "vehicle-maintenance-block",
                "vehicle-fuel-block",
                "calculated-summary-running-cost",
                "grand-calculated-summary-vehicle",
            ],
            section_id="vehicle-details-section",
            list_name="vehicles",
            list_item_id="ZIrqqR",
        )
        return_location = ReturnLocation(
            return_to="grand-calculated-summary",
            return_to_block_id="grand-calculated-summary-vehicle",
            return_to_list_item_id=return_to_list_item_id,
        )
        next_location_url = self.router.get_next_location_url(
            current_location, routing_path, return_location
        )
        expected_next_url = url_for(
            "questionnaire.block",
            list_name="vehicles",
            list_item_id="ZIrqqR",
            block_id="grand-calculated-summary-vehicle",
        )

        assert expected_next_url == next_location_url

    @pytest.mark.parametrize(
        "return_to_block_id",
        ("grand-calculated-summary-1", "grand-calculated-summary-2"),
    )
    @pytest.mark.usefixtures("app")
    def test_return_to_grand_calculated_summary_from_incomplete_section(
        self, return_to_block_id
    ):
        """
        This tests that if you try to return to a grand calculated summary from an incomplete section
        (or the same section but before the dependencies of the grand calculated summary are complete)
        you are routed to the next block in the incomplete section rather than the grand calculated summary
        """
        self.schema = load_schema_from_name(
            "test_grand_calculated_summary_repeating_answers"
        )
        # calculated summary 3 is not complete yet
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="section-1",
                    block_ids=[
                        "block-1",
                        "block-2",
                        "calculated-summary-1",
                        "block-3",
                        "calculated-summary-2",
                    ],
                    status=CompletionStatus.IN_PROGRESS,
                )
            ]
        )

        current_location = Location(section_id="section-1", block_id="block-2")
        routing_path = RoutingPath(
            block_ids=[
                "block-1",
                "block-2",
                "calculated-summary-1",
                "block-3",
                "calculated-summary-2",
                "calculated-summary-3",
                "grand-calculated-summary-1",
            ],
            section_id="section-1",
        )
        return_location = ReturnLocation(
            return_to="grand-calculated-summary",
            return_to_answer_id="calculated-summary-1",
            return_to_block_id=return_to_block_id,
        )
        next_location_url = self.router.get_next_location_url(
            current_location,
            routing_path,
            return_location,
        )

        # because calculated summary 3 isn't done, should go there before jumping to the grand calculated summary
        # test from grand-calculated-summary-1 which is in the same section, and grand-calculated-summary-2 which is in another
        expected_next_url = url_for(
            "questionnaire.block",
            return_to="grand-calculated-summary",
            return_to_block_id=return_to_block_id,
            return_to_answer_id=return_location.return_to_answer_id,
            block_id="calculated-summary-3",
        )

        assert expected_next_url == next_location_url

    @pytest.mark.usefixtures("app")
    def test_return_to_calculated_summary_from_incomplete_section(
        self, grand_calculated_summary_schema
    ):
        """
        This tests that if you try to return to a calculated summary section from an incomplete section
        you are routed to the next block in the incomplete section rather than the calculated summary
        """
        self.schema = grand_calculated_summary_schema
        # second-number block not complete yet
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="section-1",
                    block_ids=[
                        "first-number-block",
                        "distance-calculated-summary-1",
                    ],
                    status=CompletionStatus.IN_PROGRESS,
                )
            ]
        )

        current_location = Location(
            section_id="section-1", block_id="first-number-block"
        )
        routing_path = RoutingPath(
            block_ids=[
                "first-number-block",
                "second-number-block",
                "distance-calculated-summary-1",
                "number-calculated-summary-1",
            ],
            section_id="section-1",
        )
        return_location = ReturnLocation(
            return_to="calculated-summary,grand-calculated-summary",
            return_to_answer_id="first-number-block",
            return_to_block_id="distance-calculated-summary-1,distance-grand-calculated-summary",
        )
        # the test is being done as part of a two-step return to but its identical functionally
        next_location_url = self.router.get_next_location_url(
            current_location,
            routing_path,
            return_location,
        )

        # should take you to the second-number-block before going back to the calculated summary
        expected_next_url = url_for(
            "questionnaire.block",
            return_to="calculated-summary,grand-calculated-summary",
            return_to_block_id="distance-calculated-summary-1,distance-grand-calculated-summary",
            return_to_answer_id="first-number-block",
            block_id="second-number-block",
        )

        assert expected_next_url == next_location_url

    @pytest.mark.parametrize(
        "schema,section,block_id,return_to,return_to_block_id,routing_path_block_ids,next_incomplete_block_id",
        [
            (
                "test_list_collector_repeating_blocks_section_summary",
                "section-companies",
                "responsible-party",
                "section-summary",
                None,
                [
                    "responsible-party",
                    "any-other-companies-or-branches",
                    "any-companies-or-branches",
                    "any-other-trading-details",
                ],
                "any-other-companies-or-branches",
            ),
            (
                "test_list_collector_repeating_blocks_section_summary",
                "section-companies",
                "any-other-companies-or-branches",
                "submit",
                None,
                [
                    "responsible-party",
                    "any-other-companies-or-branches",
                    "any-companies-or-branches",
                    "any-other-trading-details",
                ],
                "any-other-trading-details",
            ),
            (
                "test_new_calculated_summary_repeating_and_static_answers",
                "section-1",
                "list-collector",
                "section-1",
                None,
                [
                    "any-supermarket",
                    "list-collector",
                    "dynamic-answer",
                    "extra-spending-block",
                    "extra-spending-method-block",
                    "calculated-summary-spending",
                    "calculated-summary-visits",
                ],
                "extra-spending-method-block",
            ),
            (
                "test_new_calculated_summary_repeating_and_static_answers",
                "section-1",
                "dynamic-answer",
                "section-1",
                "calculated-summary-visits",
                [
                    "any-supermarket",
                    "list-collector",
                    "dynamic-answer",
                    "extra-spending-block",
                    "extra-spending-method-block",
                    "calculated-summary-spending",
                ],
                "calculated-summary-spending",
            ),
        ],
    )
    @pytest.mark.usefixtures("app")
    def test_return_to_inaccessible_summary_routes_to_next_incomplete_block(
        self,
        schema,
        section,
        block_id,
        return_to,
        return_to_block_id,
        routing_path_block_ids,
        next_incomplete_block_id,
    ):
        """
        This tests that if you try to return to a section/final/calculated summary which is not yet accessible
        then you route to the next incomplete block in the section with all return to parameters preserved
        """
        self.schema = load_schema_from_name(schema)
        current_location = Location(section_id=section, block_id=block_id)
        routing_path = RoutingPath(block_ids=routing_path_block_ids, section_id=section)

        # make a copy where next_incomplete_block_id is not yet completed
        completed_block_ids = [*routing_path_block_ids]
        completed_block_ids.remove(next_incomplete_block_id)

        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id=section,
                    block_ids=completed_block_ids,
                    status=CompletionStatus.IN_PROGRESS,
                )
            ]
        )

        return_location = ReturnLocation(
            return_to=return_to,
            return_to_block_id=return_to_block_id,
        )

        next_location_url = self.router.get_next_location_url(
            current_location, routing_path, return_location
        )

        expected_next_url = url_for(
            "questionnaire.block",
            return_to=return_to,
            return_to_block_id=return_to_block_id,
            block_id=next_incomplete_block_id,
        )

        assert expected_next_url == next_location_url


class TestRouterNextLocationLinearFlow(RouterTestCase):
    @pytest.mark.usefixtures("app")
    def test_redirects_to_submit_page_when_questionnaire_complete(
        self,
    ):
        self.schema = load_schema_from_name("test_textfield")
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="default-section",
                    list_item_id=None,
                    status=CompletionStatus.COMPLETED,
                    block_ids=["name-block"],
                )
            ]
        )

        current_location = Location(section_id="default-section", block_id="name-block")
        routing_path = RoutingPath(
            block_ids=["name-block"], section_id="default-section"
        )
        return_location = ReturnLocation()
        next_location = self.router.get_next_location_url(
            current_location, routing_path, return_location
        )

        assert url_for("questionnaire.submit_questionnaire") == next_location

    @pytest.mark.usefixtures("app")
    def test_return_to_final_summary_questionnaire_and_section_is_complete(self):
        self.schema = load_schema_from_name(
            "test_routing_to_questionnaire_end_single_section"
        )
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="test-section",
                    list_item_id=None,
                    status=CompletionStatus.COMPLETED,
                    block_ids=["test-forced"],
                )
            ]
        )
        current_location = Location(section_id="test-section", block_id="test-forced")
        routing_path = RoutingPath(block_ids=["test-forced"], section_id="test-section")
        return_location = ReturnLocation(return_to="final-summary")
        next_location = self.router.get_next_location_url(
            current_location, routing_path, return_location
        )

        assert url_for("questionnaire.submit_questionnaire") == next_location

    @pytest.mark.usefixtures("app")
    def test_return_to_final_summary_section_is_in_progress(self):
        self.schema = load_schema_from_name("test_submit_with_summary")
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="default-section",
                    list_item_id=None,
                    status=CompletionStatus.IN_PROGRESS,
                    block_ids=["radio", "dessert", "dessert-confirmation"],
                )
            ]
        )
        current_location = Location(
            section_id="default-section", block_id="dessert-confirmation"
        )
        routing_path = RoutingPath(
            block_ids=["radio", "dessert", "dessert-confirmation", "numbers"],
            section_id="default-section",
        )
        return_location = ReturnLocation(return_to="final-summary")
        next_location = self.router.get_next_location_url(
            current_location, routing_path, return_location
        )

        assert "/questionnaire/numbers/?return_to=final-summary" in next_location

    @pytest.mark.usefixtures("app")
    def test_return_to_final_summary_questionnaire_is_not_complete(self):
        self.schema = load_schema_from_name(
            "test_routing_to_questionnaire_end_multiple_sections"
        )
        self.answer_store = AnswerStore([{"answer_id": "test-answer", "value": "Yes"}])
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="test-section",
                    list_item_id=None,
                    status=CompletionStatus.COMPLETED,
                    block_ids=["test-forced"],
                )
            ]
        )

        current_location = Location(section_id="test-section", block_id="test-forced")
        routing_path = RoutingPath(block_ids=["test-forced"], section_id="test-section")
        return_location = ReturnLocation(return_to="final-summary")
        next_location = self.router.get_next_location_url(
            current_location, routing_path, return_location
        )
        expected_location = Location(
            section_id="test-section-2",
            block_id="test-optional",
            list_item_id=None,
        )

        assert expected_location.url() == next_location


class TestRouterPreviousLocation(RouterTestCase):
    @pytest.mark.usefixtures("app")
    def test_within_section(self):
        self.schema = load_schema_from_name("test_checkbox")

        current_location = Location(
            section_id="default-section", block_id="non-mandatory-checkbox"
        )

        routing_path = RoutingPath(
            block_ids=["mandatory-checkbox", "non-mandatory-checkbox"],
            section_id="default-section",
        )
        return_location = ReturnLocation()
        previous_location_url = self.router.get_previous_location_url(
            current_location, routing_path, return_location
        )
        expected_location_url = Location(
            section_id="default-section", block_id="mandatory-checkbox"
        ).url()

        assert expected_location_url == previous_location_url

    @pytest.mark.usefixtures("app")
    def test_return_to_calculated_summary(self):
        self.schema = load_schema_from_name("test_calculated_summary")

        current_location = Location(
            section_id="default-section", block_id="second-number-block"
        )

        routing_path = RoutingPath(
            block_ids=[
                "currency-total-playback-skipped-fourth",
            ],
            section_id="default-section",
        )

        return_location = ReturnLocation(
            return_to="calculated-summary",
            return_to_answer_id="first-number-answer",
            return_to_block_id="currency-total-playback-skipped-fourth",
        )

        previous_location_url = self.router.get_previous_location_url(
            current_location,
            routing_path,
            return_location,
        )

        expected_location = Location(
            section_id="default-section",
            block_id="currency-total-playback-skipped-fourth",
        )

        expected_location_url = url_for(
            "questionnaire.block",
            list_item_id=expected_location.list_item_id,
            block_id=expected_location.block_id,
            _anchor="first-number-answer",
        )

        assert expected_location_url == previous_location_url

    @pytest.mark.usefixtures("app")
    def test_return_to_grand_calculated_summary_from_answer_incomplete_section(
        self, grand_calculated_summary_schema
    ):
        """
        This tests that if you are on a calculated summary, and your return_to_block_id is another calculated summary that you cannot reach yet
        if you click previous, then you are taken to the previous block in the section
        (rather than the first incomplete block of the section which is what next location would return)
        """
        self.schema = grand_calculated_summary_schema
        # trying to go to number-calculated-summary-1 but distance-calculated-summary-1 which comes before is not complete yet
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="section-1",
                    block_ids=[
                        "first-number-block",
                        "second-number-block",
                        "number-calculated-summary-1",
                    ],
                    status=CompletionStatus.IN_PROGRESS,
                )
            ]
        )

        current_location = Location(
            section_id="section-1", block_id="second-number-block"
        )

        routing_path = RoutingPath(
            block_ids=[
                "first-number-block",
                "second-number-block",
                "distance-calculated-summary-1",
                "number-calculated-summary-1",
            ],
            section_id="section-1",
        )

        return_location = ReturnLocation(
            return_to="calculated-summary,grand-calculated-summary",
            return_to_answer_id="second-number-block",
            return_to_block_id="number-calculated-summary-1,number-grand-calculated-summary",
        )
        previous_location_url = self.router.get_previous_location_url(
            current_location,
            routing_path,
            return_location,
        )
        # return to can't go to the distance calculated summary, so go to previous block with return params preserved
        expected_previous_url = url_for(
            "questionnaire.block",
            return_to="calculated-summary,grand-calculated-summary",
            return_to_block_id="number-calculated-summary-1,number-grand-calculated-summary",
            block_id="first-number-block",
            _anchor="second-number-block",
        )

        assert expected_previous_url == previous_location_url

    @pytest.mark.usefixtures("app")
    def test_return_to_grand_calculated_summary_from_calculated_summary_incomplete_section(
        self, grand_calculated_summary_schema
    ):
        """
        This tests that if you are on a calculated summary, and your return_to_block_id is a grand calculated summary
        if you click previous, then you are taken to the previous block in the section
        (rather than the first incomplete block of the section which is what next location would return)
        """
        self.schema = grand_calculated_summary_schema
        # number calculated summary is not complete, so the section is not complete
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="section-1",
                    block_ids=[
                        "first-number-block",
                        "second-number-block",
                        "distance-calculated-summary-1",
                    ],
                    status=CompletionStatus.IN_PROGRESS,
                )
            ]
        )

        current_location = Location(
            section_id="section-1", block_id="distance-calculated-summary-1"
        )

        routing_path = RoutingPath(
            block_ids=[
                "first-number-block",
                "second-number-block",
                "distance-calculated-summary-1",
                "number-calculated-summary-1",
            ],
            section_id="section-1",
        )

        return_location = ReturnLocation(
            return_to="grand-calculated-summary",
            return_to_answer_id="distance-calculated-summary-1",
            return_to_block_id="distance-grand-calculated-summary",
        )
        previous_location_url = self.router.get_previous_location_url(
            current_location, routing_path, return_location
        )
        # return to can't go to the grand calculated summary, so routing is just to the previous block in the section with return params preserved
        expected_previous_url = url_for(
            "questionnaire.block",
            return_to="grand-calculated-summary",
            return_to_block_id="distance-grand-calculated-summary",
            block_id="second-number-block",
            _anchor="distance-calculated-summary-1",
        )

        assert expected_previous_url == previous_location_url

    @pytest.mark.parametrize(
        "return_to, current_block, return_to_block_id, expected_url",
        [
            (
                "grand-calculated-summary",
                "distance-calculated-summary-1",
                "invalid-block",
                "/questionnaire/second-number-block/?return_to=grand-calculated-summary&return_to_block_id=invalid-block#distance-calculated-summary-1",
            ),
            (
                "calculated-summary,invalid",
                "second-number-block",
                "invalid-1,invalid-2",
                "/questionnaire/first-number-block/?return_to=calculated-summary,invalid&return_to_block_id=invalid-1,invalid-2#distance-calculated-summary-1",
            ),
            (
                "invalid",
                "distance-calculated-summary-1",
                "first-number-block",
                "/questionnaire/second-number-block/?return_to=invalid&return_to_block_id=first-number-block#distance-calculated-summary-1",
            ),
        ],
    )
    @pytest.mark.usefixtures("app")
    def test_return_to_grand_calculated_summary_invalid_url(
        self,
        return_to,
        current_block,
        return_to_block_id,
        expected_url,
        grand_calculated_summary_schema,
    ):
        self.schema = grand_calculated_summary_schema

        current_location = Location(section_id="section-1", block_id=current_block)

        routing_path = RoutingPath(
            block_ids=[
                "first-number-block",
                "second-number-block",
                "distance-calculated-summary-1",
                "number-calculated-summary-1",
            ],
            section_id="section-1",
        )

        return_location = ReturnLocation(
            return_to=return_to,
            return_to_answer_id="distance-calculated-summary-1",
            return_to_block_id=return_to_block_id,
        )
        previous_location_url = self.router.get_previous_location_url(
            current_location,
            routing_path,
            return_location,
        )

        assert expected_url == previous_location_url

    @pytest.mark.usefixtures("app")
    def test_return_to_grand_calculated_summary_from_repeating_answer(
        self,
        grand_calculated_summary_repeating_answers_progress_store,
        grand_calculated_summary_repeating_answers_schema,
    ):
        """
        Test returning to a calculated summary from a list repeating question as part of a grand calculated summary change link
        """
        self.schema = grand_calculated_summary_repeating_answers_schema
        self.progress_store = grand_calculated_summary_repeating_answers_progress_store

        parent_location = Location(
            section_id="section-5",
            block_id="any-other-streaming-services",
        )

        routing_path = RoutingPath(
            block_ids=["calculated-summary-6"],
            section_id="section-5",
        )

        return_location = ReturnLocation(
            return_to="calculated-summary,grand-calculated-summary",
            return_to_answer_id="calculated-summary-6",
            return_to_block_id="calculated-summary-6,grand-calculated-summary-3",
        )
        next_location_url = self.router.get_previous_location_url(
            parent_location,
            routing_path,
            return_location,
        )

        expected_previous_url = url_for(
            "questionnaire.block",
            return_to="grand-calculated-summary",
            block_id="calculated-summary-6",
            return_to_block_id="grand-calculated-summary-3",
            _anchor="calculated-summary-6",
        )

        assert expected_previous_url == next_location_url

    @pytest.mark.usefixtures("app")
    def test_return_to_section_summary_section_is_complete(self):
        self.schema = load_schema_from_name("test_section_summary")
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="property-details-section",
                    list_item_id=None,
                    status=CompletionStatus.COMPLETED,
                    block_ids=["insurance-type", "insurance-address", "listed"],
                )
            ]
        )

        current_location = Location(
            section_id="property-details-section", block_id="insurance-type"
        )
        routing_path = RoutingPath(
            block_ids=["insurance-type", "insurance-address", "listed"],
            section_id="default-section",
        )
        return_location = ReturnLocation(
            return_to="section-summary",
            return_to_answer_id="insurance-address-answer",
        )
        previous_location_url = self.router.get_previous_location_url(
            current_location,
            routing_path,
            return_location,
        )

        assert (
            "/questionnaire/sections/property-details-section/#insurance-address-answer"
            in previous_location_url
        )

    @pytest.mark.usefixtures("app")
    def test_return_to_section_summary_section_is_in_progress(self):
        self.schema = load_schema_from_name("test_section_summary")
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="property-details-section",
                    list_item_id=None,
                    status=CompletionStatus.IN_PROGRESS,
                    block_ids=["insurance-type", "insurance-address", "listed"],
                )
            ]
        )

        current_location = Location(
            section_id="property-details-section", block_id="insurance-address"
        )
        routing_path = RoutingPath(
            block_ids=["insurance-type", "insurance-address", "listed"],
            section_id="default-section",
        )
        return_location = ReturnLocation(
            return_to="section-summary",
            return_to_answer_id="insurance-address-answer",
        )
        previous_location_url = self.router.get_previous_location_url(
            current_location,
            routing_path,
            return_location,
        )

        assert (
            "/questionnaire/insurance-type/?return_to=section-summary#insurance-address-answer"
            in previous_location_url
        )

    @pytest.mark.usefixtures("app")
    def test_return_to_final_summary_section_is_complete(self):
        self.schema = load_schema_from_name("test_submit_with_summary")
        self.progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": [
                        "radio",
                        "dessert",
                        "dessert-confirmation",
                        "numbers",
                    ],
                }
            ]
        )

        current_location = Location(section_id="default-section", block_id="radio")
        routing_path = RoutingPath(
            block_ids=["radio", "dessert", "dessert-confirmation", "numbers"],
            section_id="default-section",
        )
        return_location = ReturnLocation(
            return_to="final-summary",
            return_to_answer_id="dessert-answer",
        )
        previous_location = self.router.get_previous_location_url(
            current_location,
            routing_path,
            return_location,
        )

        assert "/questionnaire/submit/#dessert-answer" in previous_location

    @pytest.mark.usefixtures("app")
    def test_return_to_final_summary_section_is_in_progress(self):
        self.schema = load_schema_from_name("test_submit_with_summary")
        self.progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.IN_PROGRESS,
                    "block_ids": [
                        "radio",
                        "dessert",
                        "dessert-confirmation",
                        "numbers",
                    ],
                }
            ]
        )

        current_location = Location(section_id="default-section", block_id="dessert")
        routing_path = RoutingPath(
            block_ids=["radio", "dessert", "dessert-confirmation", "numbers"],
            section_id="default-section",
        )
        return_location = ReturnLocation(
            return_to="final-summary",
            return_to_answer_id="dessert-answer",
        )
        previous_location = self.router.get_previous_location_url(
            current_location,
            routing_path,
            return_location,
        )

        assert (
            "/questionnaire/radio/?return_to=final-summary#dessert-answer"
            in previous_location
        )


class TestRouterPreviousLocationLinearFlow(RouterTestCase):
    @pytest.mark.usefixtures("app")
    def test_is_none_on_first_block_single_section(self):
        self.schema = load_schema_from_name("test_checkbox")
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="default-section",
                    list_item_id=None,
                    status=CompletionStatus.IN_PROGRESS,
                    block_ids=["mandatory-checkbox"],
                )
            ]
        )
        routing_path = RoutingPath(
            block_ids=[
                "mandatory-checkbox",
                "non-mandatory-checkbox",
                "single-checkbox",
            ],
            section_id="default-section",
        )

        current_location = Location(
            section_id="default-section", block_id="mandatory-checkbox"
        )
        return_location = ReturnLocation()

        previous_location_url = self.router.get_previous_location_url(
            current_location,
            routing_path,
            return_location,
        )

        assert previous_location_url is None

    @pytest.mark.usefixtures("app")
    def test_is_none_on_first_block_second_section(self):
        self.schema = load_schema_from_name("test_section_summary")
        self.progress_store = ProgressStore(
            [
                {
                    "section_id": "property-details-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": [
                        "insurance-type",
                        "insurance-address",
                        "listed",
                    ],
                }
            ]
        )

        current_location = Location(
            section_id="house-details-section", block_id="house-type"
        )
        routing_path = RoutingPath(
            block_ids=["house-type"], section_id="house-details-section"
        )
        return_location = ReturnLocation()

        previous_location_url = self.router.get_previous_location_url(
            current_location,
            routing_path,
            return_location,
        )

        assert previous_location_url is None


class TestRouterPreviousLocationHubFlow(RouterTestCase):
    @pytest.mark.usefixtures("app")
    def test_is_not_none_on_first_block_in_section(self):
        self.schema = load_schema_from_name("test_hub_and_spoke")

        current_location = Location(
            section_id="employment-section", block_id="employment-status"
        )

        routing_path = RoutingPath(
            block_ids=["employment-status", "employment-type"],
            section_id="employment-section",
        )

        return_location = ReturnLocation()

        previous_location_url = self.router.get_previous_location_url(
            current_location,
            routing_path,
            return_location,
        )

        assert url_for("questionnaire.get_questionnaire") == previous_location_url


class TestRouterLastLocationLinearFlow(RouterTestCase):
    @pytest.mark.usefixtures("app")
    def test_block_on_path(self):
        self.schema = load_schema_from_name("test_checkbox")
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="default-section",
                    block_ids=[
                        "mandatory-checkbox",
                        "non-mandatory-checkbox",
                        "single-checkbox",
                    ],
                    status=CompletionStatus.COMPLETED,
                )
            ]
        )
        last_location_url = self.router.get_last_location_in_questionnaire_url()
        expected_location_url = Location(
            section_id="default-section", block_id="single-checkbox", list_item_id=None
        ).url()

        assert expected_location_url == last_location_url

    @pytest.mark.usefixtures("app")
    def test_last_block_not_on_path(self):
        self.schema = load_schema_from_name(
            "test_routing_to_questionnaire_end_multiple_sections"
        )
        self.answer_store = AnswerStore(
            [
                {"answer_id": "test-answer", "value": "No"},
                {
                    "answer_id": "test-optional-answer",
                    "value": "I am a completionist",
                },
            ]
        )
        section_id = "test-section"
        last_block_on_path = "test-forced"
        completed_block_not_on_path = "test-optional"
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id=section_id,
                    block_ids=[last_block_on_path, completed_block_not_on_path],
                    status=CompletionStatus.COMPLETED,
                )
            ]
        )

        expected_location_url = Location(
            section_id=section_id,
            block_id=last_block_on_path,
            list_item_id=None,
        ).url()

        last_completed_block_in_progress_store = (
            self.progress_store.get_completed_block_ids(SectionKey(section_id))[-1]
        )

        last_location_url = self.router.get_last_location_in_questionnaire_url()

        assert completed_block_not_on_path == last_completed_block_in_progress_store
        assert expected_location_url == last_location_url

    @pytest.mark.usefixtures("app")
    def test_list_collector_final_summary_returns_to_section_summary(self):
        self.schema = load_schema_from_name("test_list_collector_list_summary")

        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="section",
                    block_ids=[
                        "introduction",
                        "primary-person-list-collector",
                        "list-collector",
                        "visitor-list-collector",
                    ],
                    status=CompletionStatus.COMPLETED,
                )
            ]
        )

        last_location_url = self.router.get_last_location_in_questionnaire_url()

        assert "/questionnaire/sections/section/" == last_location_url


class TestRouterSectionResume(RouterTestCase):
    @pytest.mark.usefixtures("app")
    def test_section_in_progress_returns_url_for_first_incomplete_location(self):
        self.schema = load_schema_from_name("test_section_summary")

        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="property-details-section",
                    list_item_id=None,
                    status=CompletionStatus.IN_PROGRESS,
                    block_ids=["insurance-type"],
                )
            ]
        )

        section_routing_path = RoutingPath(
            block_ids=["insurance-type", "insurance-address"],
            section_id="property-details-section",
        )

        section_resume_url = self.router.get_section_resume_url(
            routing_path=section_routing_path
        )

        assert "questionnaire/insurance-address/?resume=True" in section_resume_url

    @pytest.mark.usefixtures("app")
    def test_section_complete_returns_url_for_first_location(
        self,
    ):
        self.schema = load_schema_from_name("test_hub_complete_sections")
        self.progress_store = ProgressStore(
            [
                ProgressDict(
                    section_id="employment-section",
                    block_ids=["employment-status", "employment-type"],
                    status=CompletionStatus.COMPLETED,
                )
            ],
        )

        routing_path = RoutingPath(
            block_ids=["employment-status", "employment-type"],
            section_id="employment-section",
        )

        section_resume_url = self.router.get_section_resume_url(
            routing_path=routing_path
        )

        assert "questionnaire/employment-status/" in section_resume_url
