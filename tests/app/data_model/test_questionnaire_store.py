from unittest import TestCase
from unittest.mock import MagicMock

from app.data_models import QuestionnaireStore
from app.data_models.answer_store import AnswerStore
from app.data_models.progress_store import CompletionStatus, ProgressStore
from app.utilities.json import json_dumps, json_loads

from tests.app.conftest import RESPONSE_EXPIRY


def get_basic_input():
    return {
        "METADATA": {"test": True},
        "ANSWERS": [{"answer_id": "test", "value": "test"}],
        "LISTS": [],
        "PROGRESS": [
            {
                "section_id": "a-test-section",
                "list_item_id": "abc123",
                "status": CompletionStatus.COMPLETED,
                "block_ids": ["a-test-block"],
            }
        ],
        "RESPONSE_METADATA": {"test-meta": "test"},
    }


def get_input_answers_dict():
    return {
        "METADATA": {"test": True},
        "ANSWERS": {"test": [{"answer_id": "test", "value": "test"}]},
        "PROGRESS": [
            {
                "section_id": "a-test-section",
                "list_item_id": None,
                "status": CompletionStatus.COMPLETED,
                "block_ids": ["a-test-block"],
            }
        ],
        "RESPONSE_METADATA": {"test-meta": "test"},
    }


class TestQuestionnaireStore(TestCase):
    def setUp(self):
        def get_user_data():
            """Fake get_user_data implementation for storage"""
            return (
                self.input_data,
                "ce_sid",
                1,
                None,
                RESPONSE_EXPIRY,
            )

        def set_output_data(data, collection_exercise_sid, submitted_at, expires_at):
            self.output_data = data
            self.collection_exercise_sid = collection_exercise_sid
            self.submitted_at = submitted_at
            self.expires_at = expires_at

        # Storage class mocking
        self.storage = MagicMock()
        self.storage.get_user_data = MagicMock(side_effect=get_user_data)
        self.storage.save = MagicMock(side_effect=set_output_data)

        self.input_data = "{}"
        self.output_data = ""
        self.collection_exercise_sid = None
        self.submitted_at = None
        self.output_version = None
        self.expires_at = None

    def test_questionnaire_store_json_loads(self):
        # Given
        expected = get_basic_input()
        self.input_data = json_dumps(expected)
        # When
        store = QuestionnaireStore(self.storage)
        # Then
        self.assertEqual(store.metadata.copy(), expected["METADATA"])
        self.assertEqual(store.response_metadata, expected["RESPONSE_METADATA"])
        self.assertEqual(store.answer_store, AnswerStore(expected["ANSWERS"]))

        expected_completed_block_ids = expected["PROGRESS"][0]["block_ids"][0]

        self.assertEqual(
            len(
                store.progress_store.get_completed_block_ids("a-test-section", "abc123")
            ),
            1,
        )
        self.assertEqual(
            store.progress_store.get_completed_block_ids("a-test-section", "abc123")[0],
            expected_completed_block_ids,
        )

    def test_questionnaire_store_ignores_extra_json(self):
        # Given
        expected = get_basic_input()
        expected[
            "NOT_A_LEGAL_TOP_LEVEL_KEY"
        ] = "woop_woop_thats_the_sound_of_the_police"
        self.input_data = json_dumps(expected)
        # When
        store = QuestionnaireStore(self.storage)
        # Then
        self.assertEqual(store.metadata.copy(), expected["METADATA"])
        self.assertEqual(store.response_metadata, expected["RESPONSE_METADATA"])
        self.assertEqual(store.answer_store, AnswerStore(expected["ANSWERS"]))

        expected_completed_block_ids = expected["PROGRESS"][0]["block_ids"][0]

        self.assertEqual(
            len(
                store.progress_store.get_completed_block_ids("a-test-section", "abc123")
            ),
            1,
        )
        self.assertEqual(
            store.progress_store.get_completed_block_ids("a-test-section", "abc123")[0],
            expected_completed_block_ids,
        )

    def test_questionnaire_store_missing_keys(self):
        # Given
        expected = get_basic_input()
        del expected["PROGRESS"]
        self.input_data = json_dumps(expected)
        # When
        store = QuestionnaireStore(self.storage)
        # Then
        self.assertEqual(store.metadata.copy(), expected["METADATA"])
        self.assertEqual(store.response_metadata, expected["RESPONSE_METADATA"])
        self.assertEqual(store.answer_store, AnswerStore(expected["ANSWERS"]))
        self.assertEqual(store.progress_store.serialize(), [])

    def test_questionnaire_store_updates_storage(self):
        # Given
        expected = get_basic_input()
        store = QuestionnaireStore(self.storage)
        store.set_metadata(expected["METADATA"])
        store.answer_store = AnswerStore(expected["ANSWERS"])
        store.response_metadata = expected["RESPONSE_METADATA"]
        store.progress_store = ProgressStore(expected["PROGRESS"])

        # When
        store.save()  # See setUp - populates self.output_data

        # Then
        self.assertEqual(expected, json_loads(self.output_data))

    def test_questionnaire_store_errors_on_invalid_object(self):
        # Given
        class NotSerializable:
            pass

        non_serializable_metadata = {"test": NotSerializable()}

        expected = get_basic_input()
        store = QuestionnaireStore(self.storage)
        store.set_metadata(non_serializable_metadata)
        store.response_metadata = expected["RESPONSE_METADATA"]
        store.answer_store = AnswerStore(expected["ANSWERS"])
        store.progress_store = ProgressStore(expected["PROGRESS"])

        # When / Then
        self.assertRaises(TypeError, store.save)

    def test_questionnaire_store_deletes(self):
        # Given
        expected = get_basic_input()
        store = QuestionnaireStore(self.storage)
        store.set_metadata(expected["METADATA"])
        store.response_metadata = expected["RESPONSE_METADATA"]
        store.answer_store = AnswerStore(expected["ANSWERS"])
        store.progress_store = ProgressStore(expected["PROGRESS"])

        # When
        store.delete()  # See setUp - populates self.output_data

        # Then
        self.assertNotIn("a-test-section", store.progress_store)
        self.assertEqual(store.metadata.copy(), {})
        self.assertEqual(len(store.answer_store), 0)
        self.assertEqual(store.response_metadata, {})

    def test_questionnaire_store_raises_when_writing_to_metadata(self):
        store = QuestionnaireStore(self.storage)

        with self.assertRaises(TypeError):
            store.metadata["no"] = "writing"
