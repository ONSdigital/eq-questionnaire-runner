from app.data_models.answer_store import AnswerStore
from app.forms import error_messages
from app.forms.field_handlers import get_field_handler
from tests.app.app_context_test_case import AppContextTestCase


class TestFieldFactory(AppContextTestCase):
    def test_invalid_field_type_raises_on_invalid(self):
        metadata = {
            "user_id": "789473423",
            "schema_name": "0000",
            "collection_exercise_sid": "test-sid",
            "period_id": "2016-02-01",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "432423423423",
            "ru_name": "Apple",
            "return_by": "2016-07-07",
            "case_id": "1234567890",
            "case_ref": "1000000000000001",
        }

        # Given
        invalid_field_type = "Football"
        # When / Then
        with self.assertRaises(KeyError):
            get_field_handler(
                {"type": invalid_field_type}, error_messages, AnswerStore(), metadata
            )
