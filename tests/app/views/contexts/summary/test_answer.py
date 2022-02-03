from app.views.contexts.summary.answer import Answer
from tests.app.app_context_test_case import AppContextTestCase


class TestAnswer(AppContextTestCase):
    def test_create_answer(self):
        answer_schema = {"id": "answer-id", "label": "Answer Label", "type": "date"}
        user_answer = "An answer"

        answer = Answer(
            answer_schema=answer_schema,
            answer_value=user_answer,
            block_id="house-type",
            list_name="answer-list",
            list_item_id="answer-item-id",
            return_to="section-summary",
        )

        self.assertEqual(answer.id, "answer-id")
        self.assertEqual(answer.label, "Answer Label")
        self.assertEqual(answer.value, "An answer")
        self.assertEqual(answer.type, "date")

        self.assertEqual(
            answer.link,
            "http://test.localdomain/questionnaire/answer-list/answer-item-id/house-type/?return_to=section-summary&return_to_answer_id=answer-id#answer-id",
        )

    def test_date_answer_type(self):
        # Given
        answer_schema = {"id": "answer-id", "label": "", "type": "date"}
        user_answer = None

        # When
        answer = Answer(
            answer_schema=answer_schema,
            answer_value=user_answer,
            block_id="house-type",
            list_name="answer-list",
            list_item_id="answer-item-id",
            return_to="section-summary",
        )

        # Then
        self.assertEqual(answer.type, "date")
