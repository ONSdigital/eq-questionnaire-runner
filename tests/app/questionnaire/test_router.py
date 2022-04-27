from functools import cached_property
from unittest.mock import Mock

import pytest
from flask import url_for

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress_store import CompletionStatus, ProgressStore
from app.questionnaire.location import Location
from app.questionnaire.router import Router
from app.questionnaire.routing_path import RoutingPath
from app.utilities.schema import load_schema_from_name


class RouterTestCase:
    schema = None
    answer_store = AnswerStore()
    list_store = ListStore()
    progress_store = ProgressStore()
    metadata = {}
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
        )


class TestRouter(RouterTestCase):
    def test_enabled_section_ids(self):
        self.schema = load_schema_from_name("test_section_enabled_checkbox")
        self.progress_store = ProgressStore(
            [
                {
                    "section_id": "section-1",
                    "block_ids": ["section-1-block"],
                    "status": CompletionStatus.COMPLETED,
                }
            ]
        )
        self.answer_store = AnswerStore(
            [{"answer_id": "section-1-answer", "value": ["Section 2"]}]
        )

        expected_section_ids = ["section-1", "section-2"]

        assert expected_section_ids == self.router.enabled_section_ids

        self.schema = load_schema_from_name("test_new_section_enabled_checkbox")

        assert expected_section_ids == self.router.enabled_section_ids

    def test_full_routing_path_without_repeating_sections(self):
        self.schema = load_schema_from_name("test_checkbox")
        routing_path = self.router.full_routing_path()

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

        assert expected_path == routing_path


class TestRouterPathCompletion(RouterTestCase):
    def test_is_complete(self):
        self.schema = load_schema_from_name("test_textfield")
        self.progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.IN_PROGRESS,
                    "block_ids": ["name-block"],
                }
            ]
        )

        routing_path = self.router.routing_path(section_id="default-section")
        is_path_complete = self.router.is_path_complete(routing_path)

        assert is_path_complete

    def test_is_not_complete(self):
        self.schema = load_schema_from_name("test_textfield")

        routing_path = self.router.routing_path(section_id="default-section")
        is_path_complete = self.router.is_path_complete(routing_path)

        assert not is_path_complete


class TestRouterQuestionnaireCompletion(RouterTestCase):
    def test_is_complete(self):
        self.schema = load_schema_from_name("test_textfield")
        self.progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["name-block"],
                }
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
        routing_path = RoutingPath(["name-block"], section_id="default-section")
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
        routing_path = RoutingPath(["name-block"], section_id="default-section")
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
        self.schema = load_schema_from_name("test_new_section_enabled_checkbox")

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
            [
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
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.IN_PROGRESS,
                    "block_ids": ["mandatory-checkbox"],
                }
            ]
        )

        current_location = Location(
            section_id="default-section", block_id="mandatory-checkbox"
        )
        routing_path = RoutingPath(
            ["mandatory-checkbox", "non-mandatory-checkbox", "single-checkbox"],
            section_id="default-section",
        )
        next_location = self.router.get_next_location_url(
            current_location, routing_path
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
                {
                    "section_id": "section-1",
                    "list_item_id": None,
                    "status": CompletionStatus.IN_PROGRESS,
                    "block_ids": ["block-1"],
                }
            ]
        )
        current_location = Location(section_id="section-1", block_id="block-1")
        # Simulates routing backwards. Last block in section does not mean section is complete.
        routing_path = RoutingPath(
            ["block-1", "block-2", "block-1"], section_id="section-1"
        )
        next_location = self.router.get_next_location_url(
            current_location, routing_path
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
            ["insurance-type", "insurance-address", "listed"],
            section_id="property-details-section",
        )
        next_location = self.router.get_next_location_url(
            current_location, routing_path, return_to="section-summary"
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
                {
                    "section_id": "property-details-section",
                    "list_item_id": None,
                    "status": CompletionStatus.IN_PROGRESS,
                    "block_ids": ["insurance-type", "insurance-address", "listed"],
                }
            ]
        )
        current_location = Location(
            section_id="property-details-section", block_id="insurance-address"
        )
        routing_path = RoutingPath(
            ["insurance-type", "insurance-address", "address-duration", "listed"],
            section_id="property-details-section",
        )
        next_location = self.router.get_next_location_url(
            current_location, routing_path, return_to="section-summary"
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
                {
                    "section_id": "accommodation-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["proxy"],
                }
            ]
        )
        current_location = Location(
            section_id="accommodation-section", block_id="proxy"
        )
        routing_path = RoutingPath(["proxy"], section_id="default-section")
        next_location = self.router.get_next_location_url(
            current_location, routing_path
        )

        assert "questionnaire/sections/accommodation-section/" in next_location

    @pytest.mark.usefixtures("app")
    def test_section_summary_on_completion_false(self):
        self.schema = load_schema_from_name("test_show_section_summary_on_completion")
        self.progress_store = ProgressStore(
            [
                {
                    "section_id": "employment-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["employment-status"],
                }
            ]
        )
        current_location = Location(
            section_id="employment-section", block_id="employment-type"
        )
        routing_path = RoutingPath(
            ["employment-status", "employment-type"], section_id="employment-section"
        )
        next_location = self.router.get_next_location_url(
            current_location, routing_path
        )
        expected_location_url = url_for("questionnaire.get_questionnaire")

        assert expected_location_url == next_location

    @pytest.mark.usefixtures("app")
    def test_return_to_calculated_summary(self):
        self.schema = load_schema_from_name("test_calculated_summary")

        current_location = Location(
            section_id="default-section", block_id="fifth-number-block"
        )

        routing_path = RoutingPath(
            ["sixth-number-block"],
            section_id="default-section",
        )
        next_location_url = self.router.get_next_location_url(
            current_location,
            routing_path,
            return_to="calculated-summary",
            return_to_block_id="currency-total-playback-skipped-fourth",
        )
        expected_location_url = Location(
            section_id="default-section",
            block_id="currency-total-playback-skipped-fourth",
        ).url()

        assert expected_location_url == next_location_url


class TestRouterNextLocationLinearFlow(RouterTestCase):
    @pytest.mark.usefixtures("app")
    def test_redirects_to_submit_page_when_questionnaire_complete(
        self,
    ):
        self.schema = load_schema_from_name("test_textfield")
        self.progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["name-block"],
                }
            ]
        )

        current_location = Location(section_id="default-section", block_id="name-block")
        routing_path = RoutingPath(["name-block"], section_id="default-section")
        next_location = self.router.get_next_location_url(
            current_location, routing_path
        )

        assert url_for("questionnaire.submit_questionnaire") == next_location

    @pytest.mark.usefixtures("app")
    def test_return_to_final_summary_questionnaire_and_section_is_complete(self):
        self.schema = load_schema_from_name(
            "test_new_routing_to_questionnaire_end_single_section"
        )
        self.progress_store = ProgressStore(
            [
                {
                    "section_id": "test-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["test-forced"],
                }
            ]
        )
        current_location = Location(section_id="test-section", block_id="test-forced")
        routing_path = RoutingPath(["test-forced"], section_id="test-section")
        next_location = self.router.get_next_location_url(
            current_location, routing_path, return_to="final-summary"
        )

        assert url_for("questionnaire.submit_questionnaire") == next_location

    @pytest.mark.usefixtures("app")
    def test_return_to_final_summary_section_is_in_progress(self):
        self.schema = load_schema_from_name("test_submit_with_summary")
        self.progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.IN_PROGRESS,
                    "block_ids": ["radio", "dessert", "dessert-confirmation"],
                }
            ]
        )
        current_location = Location(
            section_id="default-section", block_id="dessert-confirmation"
        )
        routing_path = RoutingPath(
            ["radio", "dessert", "dessert-confirmation", "numbers"],
            section_id="default-section",
        )
        next_location = self.router.get_next_location_url(
            current_location, routing_path, return_to="final-summary"
        )

        assert "/questionnaire/numbers/?return_to=final-summary" in next_location

    @pytest.mark.usefixtures("app")
    def test_return_to_final_summary_questionnaire_is_not_complete(self):
        self.schema = load_schema_from_name(
            "test_new_routing_to_questionnaire_end_multiple_sections"
        )
        self.answer_store = AnswerStore([{"answer_id": "test-answer", "value": "Yes"}])
        self.progress_store = ProgressStore(
            [
                {
                    "section_id": "test-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["test-forced"],
                }
            ]
        )

        current_location = Location(section_id="test-section", block_id="test-forced")
        routing_path = RoutingPath(["test-forced"], section_id="test-section")
        next_location = self.router.get_next_location_url(
            current_location, routing_path, return_to="final-summary"
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
            ["mandatory-checkbox", "non-mandatory-checkbox"],
            section_id="default-section",
        )
        previous_location_url = self.router.get_previous_location_url(
            current_location, routing_path
        )
        expected_location_url = Location(
            section_id="default-section", block_id="mandatory-checkbox"
        ).url()

        assert expected_location_url == previous_location_url

    @pytest.mark.usefixtures("app")
    def test_return_to_calculated_summary(self):
        self.schema = load_schema_from_name("test_calculated_summary")

        current_location = Location(
            section_id="default-section", block_id="fifth-number-block"
        )

        routing_path = RoutingPath(
            ["sixth-number-block"],
            section_id="default-section",
        )
        previous_location_url = self.router.get_previous_location_url(
            current_location,
            routing_path,
            return_to="calculated-summary",
            return_to_block_id="currency-total-playback-skipped-fourth",
        )
        expected_location_url = Location(
            section_id="default-section",
            block_id="currency-total-playback-skipped-fourth",
        ).url()

        assert expected_location_url == previous_location_url

    @pytest.mark.usefixtures("app")
    def test_return_to_section_summary_section_is_complete(self):
        self.schema = load_schema_from_name("test_section_summary")
        self.progress_store = ProgressStore(
            [
                {
                    "section_id": "property-details-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["insurance-type", "insurance-address", "listed"],
                }
            ]
        )

        current_location = Location(
            section_id="property-details-section", block_id="insurance-type"
        )
        routing_path = RoutingPath(
            ["insurance-type", "insurance-address", "listed"],
            section_id="default-section",
        )
        previous_location_url = self.router.get_previous_location_url(
            current_location,
            routing_path,
            return_to="section-summary",
            return_to_answer_id="insurance-address-answer",
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
                {
                    "section_id": "property-details-section",
                    "list_item_id": None,
                    "status": CompletionStatus.IN_PROGRESS,
                    "block_ids": ["insurance-type", "insurance-address", "listed"],
                }
            ]
        )

        current_location = Location(
            section_id="property-details-section", block_id="insurance-address"
        )
        routing_path = RoutingPath(
            ["insurance-type", "insurance-address", "listed"],
            section_id="default-section",
        )
        previous_location_url = self.router.get_previous_location_url(
            current_location,
            routing_path,
            return_to="section-summary",
            return_to_answer_id="insurance-address-answer",
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
            ["radio", "dessert", "dessert-confirmation", "numbers"],
            section_id="default-section",
        )
        previous_location = self.router.get_previous_location_url(
            current_location,
            routing_path,
            return_to="final-summary",
            return_to_answer_id="dessert-answer",
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
            ["radio", "dessert", "dessert-confirmation", "numbers"],
            section_id="default-section",
        )
        previous_location = self.router.get_previous_location_url(
            current_location,
            routing_path,
            return_to="final-summary",
            return_to_answer_id="dessert-answer",
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
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.IN_PROGRESS,
                    "block_ids": ["mandatory-checkbox"],
                }
            ]
        )
        routing_path = RoutingPath(
            ["mandatory-checkbox", "non-mandatory-checkbox", "single-checkbox"],
            section_id="default-section",
        )

        current_location = Location(
            section_id="default-section", block_id="mandatory-checkbox"
        )
        previous_location_url = self.router.get_previous_location_url(
            current_location, routing_path
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
        routing_path = RoutingPath(["house-type"], section_id="house-details-section")
        previous_location_url = self.router.get_previous_location_url(
            current_location, routing_path
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
            ["employment-status", "employment-type"], section_id="employment-section"
        )
        previous_location_url = self.router.get_previous_location_url(
            current_location, routing_path
        )

        assert url_for("questionnaire.get_questionnaire") == previous_location_url


class TestRouterLastLocationLinearFlow(RouterTestCase):
    @pytest.mark.usefixtures("app")
    def test_block_on_path(self):
        self.schema = load_schema_from_name("test_checkbox")
        self.progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "block_ids": [
                        "mandatory-checkbox",
                        "non-mandatory-checkbox",
                        "single-checkbox",
                    ],
                    "status": CompletionStatus.COMPLETED,
                }
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
            "test_new_routing_to_questionnaire_end_multiple_sections"
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
                {
                    "section_id": section_id,
                    "block_ids": [last_block_on_path, completed_block_not_on_path],
                    "status": CompletionStatus.COMPLETED,
                }
            ]
        )

        expected_location_url = Location(
            section_id=section_id,
            block_id=last_block_on_path,
            list_item_id=None,
        ).url()

        last_completed_block_in_progress_store = (
            self.progress_store.get_completed_block_ids(
                section_id=section_id, list_item_id=None
            )[-1]
        )

        last_location_url = self.router.get_last_location_in_questionnaire_url()

        assert completed_block_not_on_path == last_completed_block_in_progress_store
        assert expected_location_url == last_location_url


class TestRouterSectionResume(RouterTestCase):
    @pytest.mark.usefixtures("app")
    def test_section_in_progress_returns_url_for_first_incomplete_location(self):
        self.schema = load_schema_from_name("test_section_summary")

        self.progress_store = ProgressStore(
            [
                {
                    "section_id": "property-details-section",
                    "list_item_id": None,
                    "status": CompletionStatus.IN_PROGRESS,
                    "block_ids": ["insurance-type"],
                }
            ]
        )

        section_routing_path = RoutingPath(
            ["insurance-type", "insurance-address"],
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
                {
                    "section_id": "employment-section",
                    "block_ids": ["employment-status", "employment-type"],
                    "status": CompletionStatus.COMPLETED,
                }
            ],
        )

        routing_path = RoutingPath(
            ["employment-status", "employment-type"], section_id="employment-section"
        )

        section_resume_url = self.router.get_section_resume_url(
            routing_path=routing_path
        )

        assert "questionnaire/employment-status/" in section_resume_url
