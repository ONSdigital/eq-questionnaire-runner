# pylint: disable=too-many-lines
from decimal import Decimal

from mock import patch
from werkzeug.datastructures import MultiDict

from app.data_models.answer_store import Answer, AnswerStore
from app.data_models.list_store import ListStore
from app.forms import error_messages
from app.forms.questionnaire_form import generate_form
from app.forms.validators import (
    DateRequired,
    ResponseRequired,
    format_message_with_title,
)
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.utilities.schema import load_schema_from_name
from tests.app.app_context_test_case import AppContextTestCase


# pylint: disable=no-member
# wtforms Form parents are not discoverable in the 2.3.3 implementation
class TestQuestionnaireForm(
    AppContextTestCase
):  # noqa: C901  pylint: disable=too-many-public-methods
    @staticmethod
    def _error_exists(answer_id, msg, mapped_errors):
        error_id = f"{answer_id}-error"
        return any(
            e_id == error_id and str(msg) in ordered_errors
            for e_id, ordered_errors in mapped_errors
        )

    def test_form_ids_match_block_answer_ids(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_textfield")

            question_schema = schema.get_block("name-block").get("question")

            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
            )

            for answer_id in schema.get_answer_ids_for_block("name-block"):
                self.assertTrue(hasattr(form, answer_id))

    def test_form_date_range_populates_data(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_range")

            question_schema = schema.get_block("date-block").get("question")

            form_data = MultiDict(
                {
                    "date-range-from-answer-day": "01",
                    "date-range-from-answer-month": "3",
                    "date-range-from-answer-year": "2016",
                    "date-range-to-answer-day": "31",
                    "date-range-to-answer-month": "3",
                    "date-range-to-answer-year": "2016",
                }
            )

            expected_form_data = {
                "csrf_token": None,
                "date-range-from-answer": "2016-03-01",
                "date-range-to-answer": "2016-03-31",
            }
            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )

            self.assertEqual(form.data, expected_form_data)

    def test_date_range_matching_dates_raises_question_error(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_range")

            question_schema = schema.get_block("date-block").get("question")

            form_data = MultiDict(
                {
                    "date-range-from-answer-day": "25",
                    "date-range-from-answer-month": "12",
                    "date-range-from-answer-year": "2016",
                    "date-range-to-answer-day": "25",
                    "date-range-to-answer-month": "12",
                    "date-range-to-answer-year": "2016",
                }
            )

            expected_form_data = {
                "csrf_token": None,
                "date-range-from-answer": "2016-12-25",
                "date-range-to-answer": "2016-12-25",
            }
            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(
                form.question_errors["date-range-question"],
                schema.error_messages["INVALID_DATE_RANGE"],
            )

    def test_date_range_to_precedes_from_raises_question_error(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_range")

            question_schema = schema.get_block("date-block").get("question")

            form_data = MultiDict(
                {
                    "date-range-from-answer-day": "25",
                    "date-range-from-answer-month": "12",
                    "date-range-from-answer-year": "2016",
                    "date-range-to-answer-day": "24",
                    "date-range-to-answer-month": "12",
                    "date-range-to-answer-year": "2016",
                }
            )

            expected_form_data = {
                "csrf_token": None,
                "date-range-from-answer": "2016-12-25",
                "date-range-to-answer": "2016-12-24",
            }

            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(
                form.question_errors["date-range-question"],
                schema.error_messages["INVALID_DATE_RANGE"],
                AnswerStore(),
            )

    def test_date_range_too_large_period_raises_question_error(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_validation_range")

            question_schema = schema.get_block("date-range-block").get("question")

            form_data = MultiDict(
                {
                    "date-range-from-day": "25",
                    "date-range-from-month": "12",
                    "date-range-from-year": "2016",
                    "date-range-to-day": "24",
                    "date-range-to-month": "12",
                    "date-range-to-year": "2017",
                }
            )

            expected_form_data = {
                "csrf_token": None,
                "date-range-from": "2016-12-25",
                "date-range-to": "2017-12-24",
            }
            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(
                form.question_errors["date-range-question"],
                schema.error_messages["DATE_PERIOD_TOO_LARGE"]
                % {"max": "1 month, 20 days"},
                AnswerStore(),
            )

    def test_date_range_too_small_period_raises_question_error(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_validation_range")

            question_schema = schema.get_block("date-range-block").get("question")

            form_data = MultiDict(
                {
                    "date-range-from-day": "25",
                    "date-range-from-month": "12",
                    "date-range-from-year": "2016",
                    "date-range-to-day": "26",
                    "date-range-to-month": "12",
                    "date-range-to-year": "2016",
                }
            )

            expected_form_data = {
                "csrf_token": None,
                "date-range-from": "2016-12-25",
                "date-range-to": "2016-12-26",
            }
            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(
                form.question_errors["date-range-question"],
                schema.error_messages["DATE_PERIOD_TOO_SMALL"] % {"min": "23 days"},
                AnswerStore(),
            )

    def test_date_range_valid_period(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_validation_range")

            question_schema = schema.get_block("date-range-block")["question"]

            form_data = MultiDict(
                {
                    "date-range-from-day": "25",
                    "date-range-from-month": "12",
                    "date-range-from-year": "2016",
                    "date-range-to-day": "26",
                    "date-range-to-month": "01",
                    "date-range-to-year": "2017",
                }
            )

            expected_form_data = {
                "csrf_token": None,
                "date-range-from": "2016-12-25",
                "date-range-to": "2017-01-26",
            }
            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )

            form.validate()
            self.assertEqual(form.data, expected_form_data)

    def test_date_combined_single_validation(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_validation_combined")

            question_schema = schema.get_block("date-range-block")["question"]

            form_data = MultiDict(
                {
                    "date-range-from-day": "01",
                    "date-range-from-month": "1",
                    "date-range-from-year": "2017",
                    "date-range-to-day": "14",
                    "date-range-to-month": "3",
                    "date-range-to-year": "2017",
                }
            )

            metadata = {
                "ref_p_start_date": "2017-01-21",
                "ref_p_end_date": "2017-02-21",
            }

            response_metadata = {}

            expected_form_data = {
                "csrf_token": None,
                "date-range-from": "2017-01-01",
                "date-range-to": "2017-03-14",
            }
            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata,
                response_metadata,
                form_data=form_data,
            )

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(
                form.errors["date-range-from"]["year"][0],
                schema.error_messages["SINGLE_DATE_PERIOD_TOO_EARLY"]
                % {"min": "1 January 2017"},
            )

            self.assertEqual(
                form.errors["date-range-to"]["year"][0],
                schema.error_messages["SINGLE_DATE_PERIOD_TOO_LATE"]
                % {"max": "14 March 2017"},
            )

    def test_date_combined_range_too_small_validation(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_validation_combined")

            question_schema = schema.get_block("date-range-block").get("question")

            form_data = MultiDict(
                {
                    "date-range-from-day": "01",
                    "date-range-from-month": 1,
                    "date-range-from-year": "2017",
                    "date-range-to-day": "10",
                    "date-range-to-month": 1,
                    "date-range-to-year": "2017",
                }
            )

            metadata = {
                "ref_p_start_date": "2017-01-20",
                "ref_p_end_date": "2017-02-20",
            }

            expected_form_data = {
                "csrf_token": None,
                "date-range-from": "2017-01-01",
                "date-range-to": "2017-01-10",
            }
            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata,
                response_metadata={},
                form_data=form_data,
            )

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(
                form.question_errors["date-range-question"],
                schema.error_messages["DATE_PERIOD_TOO_SMALL"] % {"min": "10 days"},
            )

    def test_date_combined_range_too_large_validation(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_validation_combined")

            question_schema = schema.get_block("date-range-block").get("question")

            form_data = MultiDict(
                {
                    "date-range-from-day": "01",
                    "date-range-from-month": 1,
                    "date-range-from-year": "2017",
                    "date-range-to-day": "21",
                    "date-range-to-month": 2,
                    "date-range-to-year": "2017",
                }
            )

            metadata = {
                "ref_p_start_date": "2017-01-20",
                "ref_p_end_date": "2017-02-20",
            }

            response_metadata = {}

            expected_form_data = {
                "csrf_token": None,
                "date-range-from": "2017-01-01",
                "date-range-to": "2017-02-21",
            }
            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata,
                response_metadata,
                form_data=form_data,
            )

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(
                form.question_errors["date-range-question"],
                schema.error_messages["DATE_PERIOD_TOO_LARGE"] % {"max": "50 days"},
            )

    def test_date_mm_yyyy_combined_single_validation(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_validation_mm_yyyy_combined")

            question_schema = schema.get_block("date-range-block").get("question")

            form_data = MultiDict(
                {
                    "date-range-from-month": 11,
                    "date-range-from-year": "2016",
                    "date-range-to-month": 6,
                    "date-range-to-year": "2017",
                }
            )

            metadata = {
                "ref_p_start_date": "2017-01-01",
                "ref_p_end_date": "2017-02-12",
            }

            response_metadata = {}

            expected_form_data = {
                "csrf_token": None,
                "date-range-from": "2016-11",
                "date-range-to": "2017-06",
            }
            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata,
                response_metadata,
                form_data=form_data,
            )

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(
                form.errors["date-range-from"]["year"][0],
                schema.error_messages["SINGLE_DATE_PERIOD_TOO_EARLY"]
                % {"min": "November 2016"},
            )

            self.assertEqual(
                form.errors["date-range-to"]["year"][0],
                schema.error_messages["SINGLE_DATE_PERIOD_TOO_LATE"]
                % {"max": "June 2017"},
            )

    def test_date_mm_yyyy_combined_range_too_small_validation(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_validation_mm_yyyy_combined")

            question_schema = schema.get_block("date-range-block").get("question")

            form_data = MultiDict(
                {
                    "date-range-from-month": 1,
                    "date-range-from-year": "2017",
                    "date-range-to-month": 2,
                    "date-range-to-year": "2017",
                }
            )

            metadata = {
                "ref_p_start_date": "2017-01-01",
                "ref_p_end_date": "2017-02-12",
            }

            expected_form_data = {
                "csrf_token": None,
                "date-range-from": "2017-01",
                "date-range-to": "2017-02",
            }
            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata,
                response_metadata={},
                form_data=form_data,
            )

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(
                form.question_errors["date-range-question"],
                schema.error_messages["DATE_PERIOD_TOO_SMALL"] % {"min": "2 months"},
            )

    def test_date_mm_yyyy_combined_range_too_large_validation(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_validation_mm_yyyy_combined")

            question_schema = schema.get_block("date-range-block").get("question")

            form_data = MultiDict(
                {
                    "date-range-from-month": 1,
                    "date-range-from-year": "2017",
                    "date-range-to-month": 5,
                    "date-range-to-year": "2017",
                }
            )

            metadata = {
                "ref_p_start_date": "2017-01-01",
                "ref_p_end_date": "2017-02-12",
            }

            response_metadata = {}

            expected_form_data = {
                "csrf_token": None,
                "date-range-from": "2017-01",
                "date-range-to": "2017-05",
            }
            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata,
                response_metadata,
                form_data=form_data,
            )

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(
                form.question_errors["date-range-question"],
                schema.error_messages["DATE_PERIOD_TOO_LARGE"] % {"max": "3 months"},
            )

    def test_date_yyyy_combined_single_validation(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_validation_yyyy_combined")

            question_schema = schema.get_block("date-range-block").get("question")

            form_data = MultiDict(
                {"date-range-from-year": "2015", "date-range-to-year": "2021"}
            )

            metadata = {
                "ref_p_start_date": "2017-01-01",
                "ref_p_end_date": "2017-02-12",
            }

            expected_form_data = {
                "csrf_token": None,
                "date-range-from": "2015",
                "date-range-to": "2021",
            }
            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata,
                response_metadata={},
                form_data=form_data,
            )

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(
                form.errors["date-range-from"]["year"][0],
                schema.error_messages["SINGLE_DATE_PERIOD_TOO_EARLY"] % {"min": "2015"},
            )

            self.assertEqual(
                form.errors["date-range-to"]["year"][0],
                schema.error_messages["SINGLE_DATE_PERIOD_TOO_LATE"] % {"max": "2021"},
            )

    def test_date_yyyy_combined_range_too_small_validation(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_validation_yyyy_combined")

            question_schema = schema.get_block("date-range-block").get("question")

            form_data = MultiDict(
                {"date-range-from-year": "2016", "date-range-to-year": "2017"}
            )

            metadata = {
                "ref_p_start_date": "2017-01-01",
                "ref_p_end_date": "2017-02-12",
            }

            expected_form_data = {
                "csrf_token": None,
                "date-range-from": "2016",
                "date-range-to": "2017",
            }
            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata,
                response_metadata={},
                form_data=form_data,
            )

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(
                form.question_errors["date-range-question"],
                schema.error_messages["DATE_PERIOD_TOO_SMALL"] % {"min": "2 years"},
            )

    def test_date_yyyy_combined_range_too_large_validation(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_validation_yyyy_combined")

            question_schema = schema.get_block("date-range-block").get("question")

            form_data = MultiDict(
                {"date-range-from-year": "2016", "date-range-to-year": "2020"}
            )

            metadata = {
                "ref_p_start_date": "2017-01-01",
                "ref_p_end_date": "2017-02-12",
            }

            expected_form_data = {
                "csrf_token": None,
                "date-range-from": "2016",
                "date-range-to": "2020",
            }
            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata,
                response_metadata={},
                form_data=form_data,
            )

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(
                form.question_errors["date-range-question"],
                schema.error_messages["DATE_PERIOD_TOO_LARGE"] % {"max": "3 years"},
            )

    def test_date_raises_ValueError_when_any_date_range_parts_are_falsy(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_validation_combined")

            question_schema = schema.get_block("date-range-block")["question"]

            form_data = MultiDict(
                {
                    "date-range-from-day": "01",
                    "date-range-from-month": "1",
                    "date-range-from-year": "2017",
                    "date-range-to-day": "14",
                    "date-range-to-month": "3",
                    "date-range-to-year": "2017",
                }
            )

            metadata = {"ref_p_start_date": "2017-01-21"}

            response_metadata = {}

            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata,
                response_metadata,
                form_data=form_data,
            )

            with self.assertRaises(ValueError):
                form.validate()

    def test_bespoke_message_for_date_validation_range(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_validation_range")

            question_schema = {
                "id": "date-range-question",
                "type": "DateRange",
                "validation": {"messages": {"DATE_PERIOD_TOO_SMALL": "Test Message"}},
                "period_limits": {"minimum": {"days": 20}},
                "answers": [
                    {
                        "id": "date-range-from",
                        "label": "Period from",
                        "mandatory": True,
                        "type": "Date",
                    },
                    {
                        "id": "date-range-to",
                        "label": "Period to",
                        "mandatory": True,
                        "type": "Date",
                    },
                ],
            }

            form_data = MultiDict(
                {
                    "date-range-from-day": "25",
                    "date-range-from-month": "1",
                    "date-range-from-year": "2018",
                    "date-range-to-day": "26",
                    "date-range-to-month": "1",
                    "date-range-to-year": "2018",
                }
            )

            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )

            with patch(
                "app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block",
                return_value=[question_schema],
            ):
                form.validate()
                self.assertIn(
                    form.question_errors["date-range-question"], "Test Message"
                )

    def test_invalid_minimum_period_limit_and_single_date_periods(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_validation_range")

            question_schema = {
                "id": "date-range-question",
                "type": "DateRange",
                "period_limits": {"minimum": {"months": 2}},
                "answers": [
                    {
                        "id": "date-range-from",
                        "label": "Period from",
                        "mandatory": True,
                        "type": "Date",
                        "minimum": {"value": "2018-01-10", "offset_by": {"days": -5}},
                    },
                    {
                        "id": "date-range-to",
                        "label": "Period to",
                        "mandatory": True,
                        "type": "Date",
                        "maximum": {"value": "2018-01-10", "offset_by": {"days": 5}},
                    },
                ],
            }

            form_data = MultiDict(
                {
                    "date-range-from-day": "8",
                    "date-range-from-month": "1",
                    "date-range-from-year": "2018",
                    "date-range-to-day": "13",
                    "date-range-to-month": "1",
                    "date-range-to-year": "2018",
                }
            )

            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )

            with self.assertRaises(Exception) as ite:
                with patch(
                    "app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block",
                    return_value=[question_schema],
                ):
                    form.validate()
                    self.assertEqual(
                        "The schema has invalid period_limits for date-range-question",
                        str(ite.exception),
                    )

    def test_invalid_maximum_period_limit_and_single_date_periods(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_validation_range")

            question_schema = {
                "id": "date-range-question",
                "type": "DateRange",
                "period_limits": {"maximum": {"days": 8}},
                "answers": [
                    {
                        "id": "date-range-from",
                        "label": "Period from",
                        "mandatory": True,
                        "type": "Date",
                        "minimum": {"value": "2018-01-10", "offset_by": {"days": -5}},
                    },
                    {
                        "id": "date-range-to",
                        "label": "Period to",
                        "mandatory": True,
                        "type": "Date",
                        "maximum": {"value": "2018-01-10", "offset_by": {"days": 5}},
                    },
                ],
            }

            form_data = MultiDict(
                {
                    "date-range-from-day": "6",
                    "date-range-from-month": "1",
                    "date-range-from-year": "2018",
                    "date-range-to-day": "15",
                    "date-range-to-month": "1",
                    "date-range-to-year": "2018",
                }
            )

            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )

            with self.assertRaises(Exception) as ite:
                with patch(
                    "app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block",
                    return_value=[question_schema],
                ):
                    form.validate()
                    self.assertEqual(
                        "The schema has invalid period_limits for date-range-question",
                        str(ite.exception),
                    )

    def test_invalid_date_range_and_single_date_periods(self):
        with self.app_request_context():
            answer_store = AnswerStore()
            test_answer_id = Answer(answer_id="date", value="2017-03-20")
            answer_store.add_or_update(test_answer_id)

            schema = load_schema_from_name("test_date_validation_range")

            question_schema = {
                "id": "date-range-question",
                "type": "DateRange",
                "answers": [
                    {
                        "id": "date-range-from",
                        "label": "Period from",
                        "mandatory": True,
                        "type": "Date",
                        "minimum": {"value": "2018-01-10", "offset_by": {"days": -5}},
                    },
                    {
                        "id": "date-range-to",
                        "label": "Period to",
                        "mandatory": True,
                        "type": "Date",
                        "maximum": {
                            "value": {"identifier": "date", "source": "answers"},
                            "offset_by": {"days": 5},
                        },
                    },
                ],
            }

            form_data = MultiDict(
                {
                    "date-range-from-day": "6",
                    "date-range-from-month": "1",
                    "date-range-from-year": "2018",
                    "date-range-to-day": "15",
                    "date-range-to-month": "1",
                    "date-range-to-year": "2018",
                }
            )

            metadata = {"schema_name": "test_date_validation_range"}

            form = generate_form(
                schema,
                question_schema,
                answer_store,
                ListStore(),
                metadata=metadata,
                response_metadata={},
                form_data=form_data,
            )

            with self.assertRaises(Exception) as ite:
                with patch(
                    "app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block",
                    return_value=[question_schema],
                ):
                    form.validate()
                    self.assertEqual(
                        "The schema has invalid date answer limits for date-range-question",
                        str(ite.exception),
                    )

    def test_invalid_calculation_type(self):
        store = AnswerStore()

        answer_total = Answer(answer_id="total-answer", value=10)

        store.add_or_update(answer_total)

        with self.app_request_context():
            schema = load_schema_from_name("test_sum_equal_validation_against_total")

            question_schema = QuestionnaireSchema.get_mutable_deepcopy(
                schema.get_block("breakdown-block").get("question")
            )

            question_schema["calculations"] = [
                {
                    "calculation_type": "subtraction",
                    "answer_id": "total-answer",
                    "answers_to_calculate": ["breakdown-1", "breakdown-2"],
                    "conditions": ["equals"],
                }
            ]

            form_data = MultiDict({"breakdown-1": "3", "breakdown-2": "5"})

            form = generate_form(
                schema,
                question_schema,
                store,
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )

            with self.assertRaises(Exception) as ite:
                with patch(
                    "app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block",
                    return_value=[question_schema],
                ):
                    form.validate()
            self.assertEqual(
                "Invalid calculation_type: subtraction", str(ite.exception)
            )

    def test_bespoke_message_for_sum_validation(self):
        store = AnswerStore()

        answer_total = Answer(answer_id="total-answer", value=10)

        store.add_or_update(answer_total)

        with self.app_request_context():
            schema = load_schema_from_name("test_sum_equal_validation_against_total")

            question_schema = QuestionnaireSchema.get_mutable_deepcopy(
                schema.get_block("breakdown-block").get("question")
            )

            question_schema["validation"] = {
                "messages": {"TOTAL_SUM_NOT_EQUALS": "Test Message"}
            }

            form_data = MultiDict({"breakdown-1": "3", "breakdown-2": "5"})

            form = generate_form(
                schema,
                question_schema,
                store,
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )

            with patch(
                "app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block",
                return_value=[question_schema],
            ):
                form.validate()
                self.assertIn(
                    form.question_errors["breakdown-question"], "Test Message"
                )

    def test_empty_calculated_field(self):
        store = AnswerStore()

        answer_total = Answer(answer_id="total-answer", value=10)

        store.add_or_update(answer_total)

        with self.app_request_context():
            schema = load_schema_from_name("test_sum_equal_validation_against_total")

            question_schema = schema.get_block("breakdown-block").get("question")

            form_data = MultiDict(
                {
                    "breakdown-1": "",
                    "breakdown-2": "5",
                    "breakdown-3": "4",
                    "breakdown-4": "",
                }
            )

            expected_form_data = {
                "csrf_token": None,
                "breakdown-1": None,
                "breakdown-2": Decimal("5"),
                "breakdown-3": Decimal("4"),
                "breakdown-4": None,
            }
            form = generate_form(
                schema,
                question_schema,
                store,
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(
                form.question_errors["breakdown-question"],
                schema.error_messages["TOTAL_SUM_NOT_EQUALS"] % {"total": "10"},
                AnswerStore(),
            )

    def test_sum_calculated_field(self):
        store = AnswerStore()

        answer_total = Answer(answer_id="total-answer", value=10)

        store.add_or_update(answer_total)

        with self.app_request_context():
            schema = load_schema_from_name("test_sum_equal_validation_against_total")

            question_schema = schema.get_block("breakdown-block").get("question")

            form_data = MultiDict(
                {
                    "breakdown-1": "",
                    "breakdown-2": "5",
                    "breakdown-3": "4",
                    "breakdown-4": "1",
                }
            )

            expected_form_data = {
                "csrf_token": None,
                "breakdown-1": None,
                "breakdown-2": Decimal("5"),
                "breakdown-3": Decimal("4"),
                "breakdown-4": Decimal("1"),
            }
            form = generate_form(
                schema,
                question_schema,
                store,
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )

            form.validate()
            self.assertEqual(form.data, expected_form_data)

    def test_get_calculation_total_with_no_input(self):
        store = AnswerStore()

        answer_total = Answer(answer_id="total-answer", value=10)

        store.add_or_update(answer_total)

        with self.app_request_context():
            schema = load_schema_from_name("test_sum_equal_validation_against_total")

            question_schema = schema.get_block("breakdown-block").get("question")

            form_data = MultiDict(
                {
                    "breakdown-1": "",
                    "breakdown-2": "",
                    "breakdown-3": "",
                    "breakdown-4": "",
                }
            )

            expected_form_data = {
                "csrf_token": None,
                "breakdown-1": None,
                "breakdown-2": None,
                "breakdown-3": None,
                "breakdown-4": None,
            }
            form = generate_form(
                schema,
                question_schema,
                store,
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(
                form.question_errors["breakdown-question"],
                schema.error_messages["TOTAL_SUM_NOT_EQUALS"] % {"total": "10"},
                AnswerStore(),
            )

    def test_multi_calculation(self):
        store = AnswerStore()
        list_store = ListStore()
        answer_total = Answer(answer_id="total-answer", value=10)

        store.add_or_update(answer_total)

        with self.app_request_context():
            schema = load_schema_from_name("test_sum_multi_validation_against_total")

            question_schema = schema.get_block("breakdown-block").get("question")

            form_data = MultiDict(
                {
                    "breakdown-1": "",
                    "breakdown-2": "",
                    "breakdown-3": "",
                    "breakdown-4": "",
                }
            )

            # With no answers question validation should pass
            form = generate_form(
                schema,
                question_schema,
                store,
                list_store,
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )
            form.validate()

            self.assertEqual(len(form.question_errors), 0)

            # With the data equaling the total question validation should pass
            form_data["breakdown-1"] = "10"

            form = generate_form(
                schema,
                question_schema,
                store,
                list_store,
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )
            form.validate()

            self.assertEqual(len(form.question_errors), 0)

            # With the data not equaling zero or the total, question validation should fail
            form_data["breakdown-1"] = "1"

            form = generate_form(
                schema,
                question_schema,
                store,
                list_store,
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )
            form.validate()

            self.assertEqual(
                form.question_errors["breakdown-question"],
                schema.error_messages["TOTAL_SUM_NOT_EQUALS"] % {"total": "10"},
            )

    def test_generate_form_with_title_and_no_answer_label(self):
        """
        Checks that the form is still generated when there is no answer label but there is a question title
        """
        store = AnswerStore()

        conditional_answer = Answer(answer_id="behalf-of-answer", value="chad")

        store.add_or_update(conditional_answer)

        with self.app_request_context():
            schema = load_schema_from_name("test_title")

            question_schema = schema.get_block("single-title-block").get("question")

            form_data = MultiDict({"feeling-answer": "Good"})

            expected_form_data = {"csrf_token": None, "feeling-answer": "Good"}

            with patch(
                "app.questionnaire.path_finder.evaluate_goto", return_value=False
            ):
                form = generate_form(
                    schema,
                    question_schema,
                    store,
                    ListStore(),
                    metadata={},
                    response_metadata={},
                    form_data=form_data,
                )

            form.validate()
            assert form.data == expected_form_data

    def test_form_errors_are_correctly_mapped(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_numbers")

            question_schema = schema.get_block("set-min-max-block").get("question")

            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
            )

            form.validate()
            mapped_errors = form.map_errors()

            self.assertTrue(
                self._error_exists(
                    "set-minimum",
                    schema.error_messages["MANDATORY_NUMBER"],
                    mapped_errors,
                )
            )

    def test_form_subfield_errors_are_correctly_mapped(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_range")

            question_schema = schema.get_block("date-block").get("question")

            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
            )

            form.validate()
            mapped_errors = form.map_errors()

            self.assertTrue(
                self._error_exists(
                    "date-range-from-answer",
                    schema.error_messages["MANDATORY_DATE"],
                    mapped_errors,
                )
            )
            self.assertTrue(
                self._error_exists(
                    "date-range-to-answer",
                    schema.error_messages["MANDATORY_DATE"],
                    mapped_errors,
                )
            )

    def test_detail_answer_mandatory_only_checked_if_option_selected(self):
        # The detail_answer can only be mandatory if the option it is associated with is answered
        with self.app_request_context():
            schema = load_schema_from_name("test_checkbox_detail_answer_multiple")

            question_schema = schema.get_block("mandatory-checkbox").get("question")

            #  Option is selected therefore the detail answer should be mandatory (schema defined)
            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=MultiDict({"mandatory-checkbox-answer": "Your choice"}),
            )

            detail_answer_field = getattr(form, "your-choice-answer-mandatory")
            self.assertIsInstance(detail_answer_field.validators[0], ResponseRequired)

            #  Option not selected therefore the detail answer should not be mandatory
            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                data={"mandatory-checkbox-answer": "Ham"},
            )

            detail_answer_field = getattr(form, "your-choice-answer-mandatory")
            self.assertEqual(detail_answer_field.validators, ())

    def test_answer_with_detail_answer_errors_are_correctly_mapped(self):
        with self.app_request_context():
            schema = load_schema_from_name(
                "test_radio_mandatory_with_detail_answer_mandatory"
            )

            question_schema = schema.get_block("radio-mandatory").get("question")

            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=MultiDict({"radio-mandatory-answer": "Other"}),
            )

            form.validate()
            mapped_errors = form.map_errors()

            self.assertTrue(
                self._error_exists(
                    "radio-mandatory-answer",
                    schema.error_messages["MANDATORY_TEXTFIELD"],
                    mapped_errors,
                )
            )
            self.assertFalse(
                self._error_exists(
                    "other-answer-mandatory",
                    schema.error_messages["MANDATORY_TEXTFIELD"],
                    mapped_errors,
                )
            )

    def test_answer_errors_are_interpolated(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_numbers")

            question_schema = schema.get_block("set-min-max-block").get("question")

            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=MultiDict({"set-minimum": "-1"}),
            )

            form.validate()
            answer_errors = form.answer_errors("set-minimum")
            self.assertIn(
                schema.error_messages["NUMBER_TOO_SMALL"] % {"min": "0"}, answer_errors
            )

    def test_mandatory_mutually_exclusive_question_raises_error_when_not_answered(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_mutually_exclusive")

            question_schema = schema.get_block("mutually-exclusive-mandatory-date").get(
                "question"
            )

            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=MultiDict(),
            )
            form.validate_mutually_exclusive_question(question_schema)

            self.assertEqual(
                form.question_errors["mutually-exclusive-mandatory-date-question"],
                format_message_with_title(
                    error_messages["MANDATORY_QUESTION"], question_schema.get("title")
                ),
            )

    def test_mandatory_mutually_exclusive_question_raises_error_with_question_text(
        self,
    ):
        with self.app_request_context():
            schema = load_schema_from_name("test_question_title_in_error")

            question_schema = schema.get_block("mutually-exclusive-checkbox").get(
                "question"
            )
            answer_store = AnswerStore(
                [{"answer_id": "mandatory-checkbox-answer", "value": ["Tuna"]}]
            )

            renderer = PlaceholderRenderer(
                language="en",
                answer_store=answer_store,
                list_store=ListStore(),
                metadata={},
                response_metadata={},
                schema=schema,
            )
            rendered_schema = renderer.render(question_schema, None)

            form = generate_form(
                schema,
                rendered_schema,
                answer_store,
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=MultiDict(),
            )
            form.validate_mutually_exclusive_question(question_schema)
            error = form.question_errors["mutually-exclusive-checkbox-question"]

            assert error == format_message_with_title(
                error_messages["MANDATORY_CHECKBOX"],
                "Did you really answer ‘Tuna’ to the previous question?",
            )

    def test_mutually_exclusive_question_raises_error_when_both_answered(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_mutually_exclusive")

            question_schema = schema.get_block("mutually-exclusive-date").get(
                "question"
            )

            form_data = MultiDict(
                {
                    "date-answer-day": "17",
                    "date-answer-month": "9",
                    "date-answer-year": "2018",
                    "date-exclusive-answer": "I prefer not to say",
                }
            )

            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )
            form.validate_mutually_exclusive_question(question_schema)

            self.assertEqual(
                form.question_errors["mutually-exclusive-date-question"],
                error_messages["MUTUALLY_EXCLUSIVE"],
            )

    def test_date_range_form(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_range")
            question_schema = schema.get_block("date-block").get("question")

            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
            )

            self.assertTrue(hasattr(form, "date-range-from-answer"))
            self.assertTrue(hasattr(form, "date-range-to-answer"))

            period_from_field = getattr(form, "date-range-from-answer")
            period_to_field = getattr(form, "date-range-to-answer")

            self.assertIsInstance(period_from_field.year.validators[0], DateRequired)
            self.assertIsInstance(period_to_field.year.validators[0], DateRequired)

    def test_date_range_form_with_data(self):
        with self.app_request_context():
            schema = load_schema_from_name("test_date_range")
            question_schema = schema.get_block("date-block").get("question")

            form_data = MultiDict(
                {
                    "date-range-from-answer-day": "1",
                    "date-range-from-answer-month": "05",
                    "date-range-from-answer-year": "2015",
                    "date-range-to-answer-day": "1",
                    "date-range-to-answer-month": "09",
                    "date-range-to-answer-year": "2017",
                }
            )

            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )

            self.assertTrue(hasattr(form, "date-range-from-answer"))
            self.assertTrue(hasattr(form, "date-range-to-answer"))

            period_from_field = getattr(form, "date-range-from-answer")
            period_to_field = getattr(form, "date-range-to-answer")

            self.assertIsInstance(period_from_field.year.validators[0], DateRequired)
            self.assertIsInstance(period_to_field.year.validators[0], DateRequired)

            self.assertEqual(period_from_field.data, "2015-05-01")
            self.assertEqual(period_to_field.data, "2017-09-01")

    def test_form_for_radio_other_not_selected(self):
        with self.app_request_context():
            schema = load_schema_from_name(
                "test_radio_mandatory_with_detail_answer_mandatory"
            )

            question_schema = schema.get_block("radio-mandatory").get("question")

            form_data = MultiDict(
                {
                    "radio-mandatory-answer": "Bacon",
                    "other-answer-mandatory": "Old other text",
                }
            )

            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )

            self.assertTrue(hasattr(form, "radio-mandatory-answer"))
            other_text_field = getattr(form, "other-answer-mandatory")
            self.assertEqual(other_text_field.data, "")

    def test_form_for_radio_other_selected(self):
        with self.app_request_context():
            schema = load_schema_from_name(
                "test_radio_mandatory_with_detail_answer_mandatory"
            )

            question_schema = schema.get_block("radio-mandatory").get("question")

            form_data = MultiDict(
                {
                    "radio-mandatory-answer": "Other",
                    "other-answer-mandatory": "Other text field value",
                }
            )
            form = generate_form(
                schema,
                question_schema,
                AnswerStore(),
                ListStore(),
                metadata=None,
                response_metadata={},
                form_data=form_data,
            )

            other_text_field = getattr(form, "other-answer-mandatory")
            self.assertEqual(other_text_field.data, "Other text field value")
