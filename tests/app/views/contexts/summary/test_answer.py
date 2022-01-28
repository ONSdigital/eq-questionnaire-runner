from app.views.contexts.summary.answer import Answer

from tests.app.app_context_test_case import AppContextTestCase


class TestAnswer(AppContextTestCase):
    def setUp(self):
        super().setUp()

    def test_create_answer(self):
        # Given
        answer_schema = {"id": "answer-id", "label": "Answer Label", "type": "date"}
        user_answer = "An answer"

        # When
        answer = Answer(
            answer_schema,
            user_answer,
            "house-type",
            None,
            None,
            "section-summary",
        )

        # Then
        self.assertEqual(answer.id, "answer-id")
        self.assertEqual(answer.label, "Answer Label")
        self.assertEqual(answer.value, user_answer)
        self.assertEqual(
            answer.link,
            "http://test.localdomain/questionnaire/house-type/?return_to=section-summary&return_to_answer_id=answer-id",
        )

    def test_date_answer_type(self):
        # Given
        answer_schema = {"id": "answer-id", "label": "", "type": "date"}
        user_answer = None

        # When
        answer = Answer(answer_schema, user_answer, "1", "2", "3", "section-summary")

        # Then
        self.assertEqual(answer.type, "date")
