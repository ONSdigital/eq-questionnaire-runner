from unittest.mock import patch

import pytest

from app.data_model.answer_store import Answer, AnswerStore
from app.data_model.list_store import ListStore
from app.data_model.progress_store import ProgressStore, CompletionStatus
from app.questionnaire.location import Location
from app.questionnaire.path_finder import PathFinder
from app.utilities.schema import load_schema_from_name
from tests.app.app_context_test_case import AppContextTestCase


class TestPathFinder(AppContextTestCase):
    answer_store = AnswerStore()
    list_store = ListStore()
    progress_store = ProgressStore()
    metadata = {}

    def test_simple_path(self):
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
        path_finder = PathFinder(
            schema, self.answer_store, self.list_store, progress_store, self.metadata
        )

        section_id = schema.get_section_id_for_block_id("name-block")
        routing_path = path_finder.routing_path(section_id=section_id)

        assumed_routing_path = [
            Location(section_id="default-section", block_id="name-block"),
            Location(section_id="default-section", block_id="summary"),
        ]

        self.assertEqual(routing_path, assumed_routing_path)

    def test_introduction_in_path_when_in_schema(self):
        schema = load_schema_from_name("test_introduction")
        current_section = schema.get_section("introduction-section")

        path_finder = PathFinder(
            schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        blocks = [
            b.block_id
            for b in path_finder.routing_path(section_id=current_section["id"])
        ]

        self.assertIn("introduction", blocks)

    def test_introduction_not_in_path_when_not_in_schema(self):
        schema = load_schema_from_name("test_checkbox")
        current_section = schema.get_section("default-section")
        path_finder = PathFinder(
            schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )

        with patch("app.questionnaire.rules.evaluate_when_rules", return_value=False):
            blocks = [
                b.block_id
                for b in path_finder.routing_path(section_id=current_section["id"])
            ]

        self.assertNotIn("introduction", blocks)

    def test_routing_path_with_conditional_path(self):
        schema = load_schema_from_name("test_routing_number_equals")
        section_id = schema.get_section_id_for_block_id("number-question")
        expected_path = [
            Location(section_id="default-section", block_id="number-question"),
            Location(section_id="default-section", block_id="correct-answer"),
            Location(section_id="default-section", block_id="summary"),
        ]

        answer = Answer(answer_id="answer", value=123)
        answer_store = AnswerStore()
        answer_store.add_or_update(answer)
        progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["number-question"],
                }
            ]
        )
        path_finder = PathFinder(
            schema, answer_store, self.list_store, progress_store, self.metadata
        )

        routing_path = path_finder.routing_path(section_id=section_id)

        self.assertEqual(routing_path, expected_path)

    def test_routing_basic_and_conditional_path(self):
        # Given
        schema = load_schema_from_name("test_routing_number_equals")
        section_id = schema.get_section_id_for_block_id("number-question")
        expected_path = [
            Location(section_id="default-section", block_id="number-question"),
            Location(section_id="default-section", block_id="correct-answer"),
            Location(section_id="default-section", block_id="summary"),
        ]

        answer_1 = Answer(answer_id="answer", value=123)

        answer_store = AnswerStore()
        answer_store.add_or_update(answer_1)

        # When
        path_finder = PathFinder(
            schema, answer_store, self.list_store, self.progress_store, self.metadata
        )
        routing_path = path_finder.routing_path(section_id=section_id)

        # Then
        self.assertEqual(routing_path, expected_path)

    def test_routing_path_with_complete_introduction(self):
        schema = load_schema_from_name("test_introduction")
        section_id = schema.get_section_id_for_block_id("introduction")
        progress_store = ProgressStore(
            [
                {
                    "section_id": "introduction-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["introduction"],
                }
            ]
        )
        expected_routing_path = [
            Location(section_id="introduction-section", block_id="introduction"),
            Location(
                section_id="introduction-section",
                block_id="general-business-information-completed",
            ),
            Location(section_id="introduction-section", block_id="confirmation"),
        ]

        path_finder = PathFinder(
            schema, self.answer_store, self.list_store, progress_store, self.metadata
        )
        routing_path = path_finder.routing_path(section_id=section_id)

        self.assertEqual(routing_path, expected_routing_path)

    def test_routing_path(self):
        schema = load_schema_from_name("test_summary")
        section_id = schema.get_section_id_for_block_id("dessert-block")
        expected_path = [
            Location(section_id="default-section", block_id="radio"),
            Location(section_id="default-section", block_id="test-number-block"),
            Location(section_id="default-section", block_id="dessert-block"),
            Location(section_id="default-section", block_id="summary"),
        ]

        progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["radio", "test-number-block", "dessert-block"],
                }
            ]
        )
        path_finder = PathFinder(
            schema, self.answer_store, self.list_store, progress_store, self.metadata
        )
        routing_path = path_finder.routing_path(section_id=section_id)

        self.assertEqual(routing_path, expected_path)

    def test_routing_path_with_repeating_sections(self):
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
                }
            ]
        )
        path_finder = PathFinder(
            schema, self.answer_store, self.list_store, progress_store, self.metadata
        )

        repeating_section_id = "personal-details-section"
        routing_path = path_finder.routing_path(
            section_id=repeating_section_id, list_item_id="abc123"
        )

        expected_path = [
            Location(
                section_id="personal-details-section",
                block_id="proxy",
                list_name="people",
                list_item_id="abc123",
            ),
            Location(
                section_id="personal-details-section",
                block_id="date-of-birth",
                list_name="people",
                list_item_id="abc123",
            ),
            Location(
                section_id="personal-details-section",
                block_id="confirm-dob",
                list_name="people",
                list_item_id="abc123",
            ),
            Location(
                section_id="personal-details-section",
                block_id="sex",
                list_name="people",
                list_item_id="abc123",
            ),
            Location(
                section_id="personal-details-section",
                block_id="personal-summary",
                list_name="people",
                list_item_id="abc123",
            ),
        ]

        self.assertEqual(routing_path, expected_path)

    def test_routing_path_empty_routing_rules(self):
        schema = load_schema_from_name("test_checkbox")
        section_id = schema.get_section_id_for_block_id("mandatory-checkbox")
        expected_path = [
            Location(section_id="default-section", block_id="mandatory-checkbox"),
            Location(section_id="default-section", block_id="non-mandatory-checkbox"),
            Location(section_id="default-section", block_id="summary"),
        ]

        answer_1 = Answer(answer_id="mandatory-checkbox-answer", value="Cheese")
        answer_2 = Answer(answer_id="non-mandatory-checkbox-answer", value="deep pan")

        answer_store = AnswerStore()
        answer_store.add_or_update(answer_1)
        answer_store.add_or_update(answer_2)

        progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["mandatory-checkbox"],
                }
            ]
        )

        path_finder = PathFinder(
            schema, answer_store, self.list_store, progress_store, self.metadata
        )
        routing_path = path_finder.routing_path(section_id=section_id)

        self.assertEqual(routing_path, expected_path)

    def test_routing_path_with_conditional_value_not_in_metadata(self):
        schema = load_schema_from_name("test_metadata_routing")
        section_id = schema.get_section_id_for_block_id("block1")
        expected_path = [
            Location(section_id="default-section", block_id="block1"),
            Location(section_id="default-section", block_id="block2"),
            Location(section_id="default-section", block_id="block3"),
            Location(section_id="default-section", block_id="summary"),
        ]

        progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["block1"],
                }
            ]
        )

        path_finder = PathFinder(
            schema, self.answer_store, self.list_store, progress_store, self.metadata
        )
        routing_path = path_finder.routing_path(section_id=section_id)

        self.assertEqual(routing_path, expected_path)

    def test_routing_path_should_skip_block(self):
        # Given
        schema = load_schema_from_name("test_skip_condition_block")
        section_id = schema.get_section_id_for_block_id("should-skip")
        answer_store = AnswerStore()
        answer_store.add_or_update(
            Answer(answer_id="do-you-want-to-skip-answer", value="Yes")
        )

        progress_store = ProgressStore(
            [
                {
                    "section_id": "introduction-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["do-you-want-to-skip"],
                }
            ]
        )

        # When
        path_finder = PathFinder(
            schema, answer_store, self.list_store, progress_store, self.metadata
        )
        routing_path = path_finder.routing_path(section_id=section_id)

        # Then
        expected_routing_path = [
            Location(section_id="default-section", block_id="do-you-want-to-skip"),
            Location(section_id="default-section", block_id="a-non-skipped-block"),
            Location(section_id="default-section", block_id="summary"),
        ]

        with patch(
            "app.questionnaire.path_finder.evaluate_skip_conditions", return_value=True
        ):
            self.assertEqual(routing_path, expected_routing_path)

    def test_routing_path_should_skip_group(self):
        # Given
        schema = load_schema_from_name("test_skip_condition_group")

        section_id = schema.get_section_id_for_block_id("do-you-want-to-skip")
        answer_store = AnswerStore()
        answer_store.add_or_update(
            Answer(answer_id="do-you-want-to-skip-answer", value="Yes")
        )
        progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["do-you-want-to-skip"],
                }
            ]
        )

        # When
        path_finder = PathFinder(
            schema, answer_store, self.list_store, progress_store, self.metadata
        )
        routing_path = path_finder.routing_path(section_id=section_id)

        # Then
        expected_routing_path = [
            Location(section_id="default-section", block_id="do-you-want-to-skip"),
            Location(section_id="default-section", block_id="last-group-block"),
            Location(section_id="default-section", block_id="summary"),
        ]

        with patch(
            "app.questionnaire.path_finder.evaluate_skip_conditions", return_value=True
        ):
            self.assertEqual(routing_path, expected_routing_path)

    def test_routing_path_should_not_skip_group(self):
        # Given
        schema = load_schema_from_name("test_skip_condition_group")

        section_id = schema.get_section_id_for_block_id("do-you-want-to-skip")
        answer_store = AnswerStore()
        answer_store.add_or_update(
            Answer(answer_id="do-you-want-to-skip-answer", value="No")
        )
        progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": ["do-you-want-to-skip"],
                }
            ]
        )

        # When
        path_finder = PathFinder(
            schema, answer_store, self.list_store, progress_store, self.metadata
        )
        routing_path = path_finder.routing_path(section_id=section_id)

        # Then
        expected_routing_path = [
            Location(section_id="default-section", block_id="do-you-want-to-skip"),
            Location(section_id="default-section", block_id="should-skip"),
            Location(section_id="default-section", block_id="last-group-block"),
            Location(section_id="default-section", block_id="summary"),
        ]

        with patch(
            "app.questionnaire.path_finder.evaluate_skip_conditions", return_value=False
        ):
            self.assertEqual(routing_path, expected_routing_path)

    def test_get_routing_path_when_first_block_in_group_skipped(self):
        # Given
        schema = load_schema_from_name("test_skip_condition_group")
        answer_store = AnswerStore()
        answer_store.add_or_update(
            Answer(answer_id="do-you-want-to-skip-answer", value="Yes")
        )

        # When
        path_finder = PathFinder(
            schema, answer_store, self.list_store, self.progress_store, self.metadata
        )

        # Then
        expected_route = [
            {
                "block_id": "do-you-want-to-skip-block",
                "group_id": "do-you-want-to-skip-group",
            },
            {"block_id": "summary", "group_id": "should-skip-group"},
        ]

        section_id = schema.get_section_id_for_block_id("summary")
        pytest.xfail(
            reason="Known bug when skipping last group due to summary bundled into it"
        )

        self.assertEqual(
            path_finder.routing_path(section_id=section_id), expected_route
        )

    def test_build_path_with_group_routing(self):
        # Given i have answered the routing question
        schema = load_schema_from_name("test_routing_group")
        section_id = schema.get_section_id_for_block_id("group2-block")

        answer_store = AnswerStore()
        answer_store.add_or_update(
            Answer(answer_id="which-group-answer", value="group2")
        )

        # When i build the path
        path_finder = PathFinder(
            schema, answer_store, self.list_store, self.progress_store, self.metadata
        )
        path = path_finder.routing_path(section_id=section_id)

        # Then it should route me straight to Group2 and not Group1
        self.assertNotIn(Location(section_id=section_id, block_id="group1-block"), path)
        self.assertIn(Location(section_id=section_id, block_id="group2-block"), path)

    def test_remove_answer_and_block_if_routing_backwards(self):
        schema = load_schema_from_name("test_confirmation_question")
        section_id = schema.get_section_id_for_block_id("confirm-zero-employees-block")

        # All blocks completed
        progress_store = ProgressStore(
            [
                {
                    "section_id": "default-section",
                    "list_item_id": None,
                    "status": CompletionStatus.COMPLETED,
                    "block_ids": [
                        "number-of-employees-total-block",
                        "confirm-zero-employees-block",
                    ],
                }
            ]
        )

        answer_store = AnswerStore()
        number_of_employees_answer = Answer(
            answer_id="number-of-employees-total", value=0
        )
        confirm_zero_answer = Answer(
            answer_id="confirm-zero-employees-answer", value="No I need to change this"
        )
        answer_store.add_or_update(number_of_employees_answer)
        answer_store.add_or_update(confirm_zero_answer)

        path_finder = PathFinder(
            schema, answer_store, self.list_store, progress_store, self.metadata
        )

        self.assertEqual(
            len(
                path_finder.progress_store.get_completed_block_ids(
                    section_id="default-section"
                )
            ),
            2,
        )
        self.assertEqual(len(path_finder.answer_store), 2)

        routing_path = path_finder.routing_path(section_id=section_id)

        expected_path = [
            Location(
                section_id="default-section", block_id="number-of-employees-total-block"
            ),
            Location(
                section_id="default-section", block_id="confirm-zero-employees-block"
            ),
            Location(
                section_id="default-section", block_id="number-of-employees-total-block"
            ),
        ]
        self.assertEqual(routing_path, expected_path)

        self.assertEqual(
            path_finder.progress_store.get_completed_block_ids(
                section_id="default-section"
            ),
            [progress_store.get_completed_block_ids(section_id="default-section")[0]],
        )
        self.assertEqual(len(path_finder.answer_store), 1)
