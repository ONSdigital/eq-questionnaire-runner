# pylint: disable=too-many-lines
from decimal import Decimal

import pytest
from werkzeug.datastructures import MultiDict

from app.data_models import ListStore, ProgressStore, SupplementaryDataStore
from app.data_models.answer_store import Answer, AnswerStore
from app.forms import error_messages
from app.forms.questionnaire_form import generate_form
from app.forms.validators import (
    DateRequired,
    ResponseRequired,
    format_message_with_title,
)
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.utilities.schema import load_schema_from_name
from tests.app.questionnaire.conftest import get_metadata


def error_exists(answer_id, msg, mapped_errors):
    error_id = f"{answer_id}-error"
    return any(
        e_id == error_id and str(msg) in ordered_errors
        for e_id, ordered_errors in mapped_errors
    )


def test_form_ids_match_block_answer_ids(app, answer_store, list_store):
    with app.test_request_context():
        schema = load_schema_from_name("test_textfield")

        question_schema = schema.get_block("name-block").get("question")

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        for answer_id in schema.get_answer_ids_for_block("name-block"):
            assert hasattr(form, answer_id)


def test_form_date_range_populates_data(app, answer_store, list_store):
    with app.test_request_context():
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
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        assert form.data == expected_form_data


def test_date_range_matching_dates_raises_question_error(app, answer_store, list_store):
    with app.test_request_context():
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
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.data, expected_form_data
        assert (
            form.question_errors["date-range-question"]
            == schema.error_messages["INVALID_DATE_RANGE"]
        )


def test_date_range_to_precedes_from_raises_question_error(
    app, answer_store, list_store
):
    with app.test_request_context():
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
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.data == expected_form_data
        assert (
            form.question_errors["date-range-question"]
            == schema.error_messages["INVALID_DATE_RANGE"]
        )


def test_date_range_too_large_period_raises_question_error(
    app, answer_store, list_store
):
    with app.test_request_context():
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
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.data == expected_form_data
        assert form.question_errors["date-range-question"] == schema.error_messages[
            "DATE_PERIOD_TOO_LARGE"
        ] % {"max": "1 month, 20 days"}


def test_date_range_too_small_period_raises_question_error(
    app, answer_store, list_store
):
    with app.test_request_context():
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
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.data == expected_form_data
        assert form.question_errors["date-range-question"] == schema.error_messages[
            "DATE_PERIOD_TOO_SMALL"
        ] % {"min": "23 days"}


def test_date_range_valid_period(app, answer_store, list_store):
    with app.test_request_context():
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
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.data == expected_form_data


def test_date_combined_single_validation(app, answer_store, list_store):
    with app.test_request_context():
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

        test_metadata = {
            "ref_p_start_date": "2017-01-21",
            "ref_p_end_date": "2017-02-21",
        }

        metadata = get_metadata(test_metadata)

        response_metadata = {}

        expected_form_data = {
            "csrf_token": None,
            "date-range-from": "2017-01-01",
            "date-range-to": "2017-03-14",
        }

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.data == expected_form_data
        assert form.errors["date-range-from"]["year"][0] == schema.error_messages[
            "SINGLE_DATE_PERIOD_TOO_EARLY"
        ] % {"min": "1 January 2017"}

        assert form.errors["date-range-to"]["year"][0] == schema.error_messages[
            "SINGLE_DATE_PERIOD_TOO_LATE"
        ] % {"max": "14 March 2017"}


def test_date_combined_range_too_small_validation(app, answer_store, list_store):
    with app.test_request_context():
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

        test_metadata = {
            "ref_p_start_date": "2017-01-20",
            "ref_p_end_date": "2017-02-20",
        }

        metadata = get_metadata(test_metadata)

        expected_form_data = {
            "csrf_token": None,
            "date-range-from": "2017-01-01",
            "date-range-to": "2017-01-10",
        }

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.data == expected_form_data
        assert form.question_errors["date-range-question"] == schema.error_messages[
            "DATE_PERIOD_TOO_SMALL"
        ] % {"min": "10 days"}


def test_date_combined_range_too_large_validation(app, answer_store, list_store):
    with app.test_request_context():
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

        test_metadata = {
            "ref_p_start_date": "2017-01-20",
            "ref_p_end_date": "2017-02-20",
        }

        metadata = get_metadata(test_metadata)

        response_metadata = {}

        expected_form_data = {
            "csrf_token": None,
            "date-range-from": "2017-01-01",
            "date-range-to": "2017-02-21",
        }

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.data == expected_form_data
        assert form.question_errors["date-range-question"] == schema.error_messages[
            "DATE_PERIOD_TOO_LARGE"
        ] % {"max": "50 days"}


def test_date_mm_yyyy_combined_single_validation(app, answer_store, list_store):
    with app.test_request_context():
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

        test_metadata = {
            "ref_p_start_date": "2017-01-01",
            "ref_p_end_date": "2017-02-12",
        }

        metadata = get_metadata(test_metadata)

        response_metadata = {}

        expected_form_data = {
            "csrf_token": None,
            "date-range-from": "2016-11",
            "date-range-to": "2017-06",
        }

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.data == expected_form_data
        assert form.errors["date-range-from"]["year"][0] == schema.error_messages[
            "SINGLE_DATE_PERIOD_TOO_EARLY"
        ] % {"min": "November 2016"}

        assert form.errors["date-range-to"]["year"][0] == schema.error_messages[
            "SINGLE_DATE_PERIOD_TOO_LATE"
        ] % {"max": "June 2017"}


def test_date_mm_yyyy_combined_range_too_small_validation(
    app, answer_store, list_store
):
    with app.test_request_context():
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

        test_metadata = {
            "ref_p_start_date": "2017-01-01",
            "ref_p_end_date": "2017-02-12",
        }

        metadata = get_metadata(test_metadata)

        expected_form_data = {
            "csrf_token": None,
            "date-range-from": "2017-01",
            "date-range-to": "2017-02",
        }

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.data == expected_form_data
        assert form.question_errors["date-range-question"] == schema.error_messages[
            "DATE_PERIOD_TOO_SMALL"
        ] % {"min": "2 months"}


def test_date_mm_yyyy_combined_range_too_large_validation(
    app, answer_store, list_store
):
    with app.test_request_context():
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

        test_metadata = {
            "ref_p_start_date": "2017-01-01",
            "ref_p_end_date": "2017-02-12",
        }

        metadata = get_metadata(test_metadata)

        response_metadata = {}

        expected_form_data = {
            "csrf_token": None,
            "date-range-from": "2017-01",
            "date-range-to": "2017-05",
        }

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.data == expected_form_data
        assert form.question_errors["date-range-question"] == schema.error_messages[
            "DATE_PERIOD_TOO_LARGE"
        ] % {"max": "3 months"}


def test_date_yyyy_combined_single_validation(app, answer_store, list_store):
    with app.test_request_context():
        schema = load_schema_from_name("test_date_validation_yyyy_combined")

        question_schema = schema.get_block("date-range-block").get("question")

        form_data = MultiDict(
            {"date-range-from-year": "2015", "date-range-to-year": "2021"}
        )

        test_metadata = {
            "ref_p_start_date": "2017-01-01",
            "ref_p_end_date": "2017-02-12",
        }

        metadata = get_metadata(test_metadata)

        expected_form_data = {
            "csrf_token": None,
            "date-range-from": "2015",
            "date-range-to": "2021",
        }

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.data == expected_form_data
        assert form.errors["date-range-from"]["year"][0] == schema.error_messages[
            "SINGLE_DATE_PERIOD_TOO_EARLY"
        ] % {"min": "2015"}

        assert form.errors["date-range-to"]["year"][0] == schema.error_messages[
            "SINGLE_DATE_PERIOD_TOO_LATE"
        ] % {"max": "2021"}


def test_date_yyyy_combined_range_too_small_validation(app, answer_store, list_store):
    with app.test_request_context():
        schema = load_schema_from_name("test_date_validation_yyyy_combined")

        question_schema = schema.get_block("date-range-block").get("question")

        form_data = MultiDict(
            {"date-range-from-year": "2016", "date-range-to-year": "2017"}
        )

        test_metadata = {
            "ref_p_start_date": "2017-01-01",
            "ref_p_end_date": "2017-02-12",
        }

        metadata = get_metadata(test_metadata)

        expected_form_data = {
            "csrf_token": None,
            "date-range-from": "2016",
            "date-range-to": "2017",
        }

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.data == expected_form_data
        assert form.question_errors["date-range-question"] == schema.error_messages[
            "DATE_PERIOD_TOO_SMALL"
        ] % {"min": "2 years"}


def test_date_yyyy_combined_range_too_large_validation(app, answer_store, list_store):
    with app.test_request_context():
        schema = load_schema_from_name("test_date_validation_yyyy_combined")

        question_schema = schema.get_block("date-range-block").get("question")

        form_data = MultiDict(
            {"date-range-from-year": "2016", "date-range-to-year": "2020"}
        )

        test_metadata = {
            "ref_p_start_date": "2017-01-01",
            "ref_p_end_date": "2017-02-12",
        }

        metadata = get_metadata(test_metadata)

        expected_form_data = {
            "csrf_token": None,
            "date-range-from": "2016",
            "date-range-to": "2020",
        }

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.data == expected_form_data
        assert form.question_errors["date-range-question"] == schema.error_messages[
            "DATE_PERIOD_TOO_LARGE"
        ] % {"max": "3 years"}


def test_date_raises_ValueError_when_any_date_range_parts_are_falsy(
    app, answer_store, list_store
):
    with app.test_request_context():
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

        metadata = get_metadata()

        response_metadata = {}

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        with pytest.raises(ValueError):
            form.validate()


def test_bespoke_message_for_date_validation_range(
    app, answer_store, list_store, mocker
):
    with app.test_request_context():
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
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        mocker.patch(
            "app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block",
            return_value=[question_schema],
        )
        form.validate()
        assert form.question_errors["date-range-question"] == "Test Message"


def test_invalid_minimum_period_limit_and_single_date_periods(
    app, answer_store, list_store, mocker
):
    with app.test_request_context():
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
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        with pytest.raises(Exception) as exc:
            mocker.patch(
                "app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block",
                return_value=[question_schema],
            )
            form.validate()
        assert "The schema has invalid period_limits for date-range-question" == str(
            exc.value
        )


def test_invalid_maximum_period_limit_and_single_date_periods(
    app, answer_store, list_store, mocker
):
    with app.test_request_context():
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
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        with pytest.raises(Exception) as exc:
            mocker.patch(
                "app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block",
                return_value=[question_schema],
            )
            form.validate()
            assert (
                "The schema has invalid period_limits for date-range-question"
                == str(exc.value)
            )


def test_period_limits_minimum_not_set_and_single_date_periods(
    app, answer_store, list_store, mocker
):
    with app.test_request_context():
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
                    "minimum": {"value": "2018-01-10"},
                },
                {
                    "id": "date-range-to",
                    "label": "Period to",
                    "mandatory": True,
                    "type": "Date",
                    "maximum": {"value": "2018-01-18"},
                },
            ],
        }

        form_data = MultiDict(
            {
                "date-range-from-day": "10",
                "date-range-from-month": "1",
                "date-range-from-year": "2018",
                "date-range-to-day": "11",
                "date-range-to-month": "1",
                "date-range-to-year": "2018",
            }
        )

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        with mocker.patch(
            "app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block",
            return_value=[question_schema],
        ):
            form.validate()

        assert len(form.question_errors) == 0


def test_invalid_date_range_and_single_date_periods(
    app, answer_store, list_store, mocker
):
    with app.test_request_context():
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
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(metadata),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        with pytest.raises(Exception) as exc:
            mocker.patch(
                "app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block",
                return_value=[question_schema],
            )
            form.validate()
        assert (
            "The schema has invalid date answer limits for date-range-question"
            == str(exc.value)
        )


def test_invalid_calculation_type(app, answer_store, list_store, mocker):
    answer_total = Answer(answer_id="total-answer", value=10)

    answer_store.add_or_update(answer_total)

    with app.test_request_context():
        schema = load_schema_from_name("test_validation_sum_against_total_equal")

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
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        with pytest.raises(Exception) as exc:
            mocker.patch(
                "app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block",
                return_value=[question_schema],
            )
            form.validate()
    assert "Invalid calculation_type: subtraction" == str(exc.value)


def test_bespoke_message_for_sum_validation(app, answer_store, list_store, mocker):
    answer_total = Answer(answer_id="total-answer", value=10)

    answer_store.add_or_update(answer_total)

    with app.test_request_context():
        schema = load_schema_from_name("test_validation_sum_against_total_equal")

        question_schema = QuestionnaireSchema.get_mutable_deepcopy(
            schema.get_block("breakdown-block").get("question")
        )

        question_schema["validation"] = {
            "messages": {"TOTAL_SUM_NOT_EQUALS": "Test Message"}
        }

        form_data = MultiDict({"breakdown-1": "3", "breakdown-2": "5"})

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        mocker.patch(
            "app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block",
            return_value=[question_schema],
        )
        form.validate()

    assert form.question_errors["breakdown-question"] == "Test Message"


@pytest.mark.parametrize(
    "schema_name, block, answers, breakdowns, expected_form_data, question, errors_text, value_dict",  # pylint: disable=too-many-locals
    [
        [
            "test_validation_sum_against_total_equal",
            "breakdown-block",
            [Answer(answer_id="total-answer", value=10)],
            {
                "breakdown-1": "",
                "breakdown-2": "5",
                "breakdown-3": "4",
                "breakdown-4": "",
            },
            {
                "csrf_token": None,
                "breakdown-1": None,
                "breakdown-2": Decimal("5"),
                "breakdown-3": Decimal("4"),
                "breakdown-4": None,
            },
            "breakdown-question",
            ["TOTAL_SUM_NOT_EQUALS"],
            {"total": "10"},
        ],
        [
            "test_validation_sum_against_total_equal",
            "breakdown-block",
            [Answer(answer_id="total-answer", value=10)],
            {
                "breakdown-1": "",
                "breakdown-2": "5",
                "breakdown-3": "4",
                "breakdown-4": "1",
            },
            {
                "csrf_token": None,
                "breakdown-1": None,
                "breakdown-2": Decimal("5"),
                "breakdown-3": Decimal("4"),
                "breakdown-4": Decimal("1"),
            },
            "breakdown-question",
            None,
            None,
        ],
        [
            "test_validation_sum_against_total_equal",
            "breakdown-block",
            [Answer(answer_id="total-answer", value=10)],
            {
                "breakdown-1": "",
                "breakdown-2": "",
                "breakdown-3": "",
                "breakdown-4": "",
            },
            {
                "csrf_token": None,
                "breakdown-1": None,
                "breakdown-2": None,
                "breakdown-3": None,
                "breakdown-4": None,
            },
            "breakdown-question",
            ["TOTAL_SUM_NOT_EQUALS"],
            {"total": "10"},
        ],
        [
            "test_validation_sum_against_value_source",
            "breakdown-block",
            [Answer(answer_id="total-answer", value=10)],
            {
                "breakdown-1": "",
                "breakdown-2": "5",
                "breakdown-3": "4",
                "breakdown-4": "1",
            },
            {
                "csrf_token": None,
                "breakdown-1": None,
                "breakdown-2": Decimal("5"),
                "breakdown-3": Decimal("4"),
                "breakdown-4": Decimal("1"),
            },
            "breakdown-question",
            None,
            None,
        ],
        [
            "test_validation_sum_against_value_source",
            "second-breakdown-block",
            [
                Answer(answer_id="breakdown-1", value=5),
                Answer(answer_id="breakdown-2", value=5),
            ],
            {
                "second-breakdown-1": "",
                "second-breakdown-2": "5",
                "second-breakdown-3": "4",
                "second-breakdown-4": "1",
            },
            {
                "csrf_token": None,
                "second-breakdown-1": None,
                "second-breakdown-2": Decimal("5"),
                "second-breakdown-3": Decimal("4"),
                "second-breakdown-4": Decimal("1"),
            },
            "second-breakdown-question",
            None,
            None,
        ],
        [
            "test_validation_sum_against_value_source",
            "breakdown-block",
            [Answer(answer_id="total-answer", value=10)],
            {
                "breakdown-1": "",
                "breakdown-2": "",
                "breakdown-3": "4",
                "breakdown-4": "1",
            },
            {
                "csrf_token": None,
                "breakdown-1": None,
                "breakdown-2": None,
                "breakdown-3": Decimal("4"),
                "breakdown-4": Decimal("1"),
            },
            "breakdown-question",
            ["TOTAL_SUM_NOT_EQUALS"],
            {"total": "10"},
        ],
        [
            "test_validation_sum_against_value_source",
            "second-breakdown-block",
            [
                Answer(answer_id="breakdown-1", value=5),
                Answer(answer_id="breakdown-2", value=5),
            ],
            {
                "second-breakdown-1": "",
                "second-breakdown-2": "",
                "second-breakdown-3": "4",
                "second-breakdown-4": "1",
            },
            {
                "csrf_token": None,
                "second-breakdown-1": None,
                "second-breakdown-2": None,
                "second-breakdown-3": Decimal("4"),
                "second-breakdown-4": Decimal("1"),
            },
            "second-breakdown-question",
            ["TOTAL_SUM_NOT_EQUALS"],
            {"total": "10"},
        ],  # pylint: disable=too-many-locals
    ],
)
def test_calculated_field(
    app,
    answer_store,
    list_store,
    schema_name,
    block,
    answers,
    breakdowns,
    expected_form_data,
    question,
    errors_text,
    value_dict,
):  # pylint: disable=too-many-locals
    for answer in answers:
        answer_store.add_or_update(answer)

    with app.test_request_context():
        schema = load_schema_from_name(schema_name)

        question_schema = schema.get_block(block).get("question")

        location = Location(
            section_id="default-section",
            block_id=block,
            list_item_id=None,
        )

        metadata = get_metadata()

        form_data = MultiDict(breakdowns)

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            location=location,
            metadata=metadata,
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.data == expected_form_data
        if errors_text:
            for error_text in errors_text:
                assert (
                    form.question_errors[question]
                    == schema.error_messages[error_text] % value_dict
                )
        else:
            assert len(form.question_errors) == 0


def test_sum_calculated_field_value_source_calculated_summary_repeat_not_equal_validation_error(
    app, answer_store, mocker
):
    list_store = ListStore([{"name": "people", "items": ["lCIZsS"]}])
    answer_store.add_or_update(
        Answer(
            answer_id="entertainment-spending-answer", value=10, list_item_id="lCIZsS"
        )
    )
    mocker.patch(
        "app.questionnaire.value_source_resolver.ValueSourceResolver._resolve_list_item_id_for_value_source",
        return_value="lCIZsS",
    )

    with app.test_request_context():
        schema = load_schema_from_name(
            "test_validation_sum_against_total_repeating_with_dependent_section"
        )

        question_schema = schema.get_block("second-spending-breakdown-block").get(
            "question"
        )

        form_data = MultiDict(
            {
                "second-spending-breakdown-1": "",
                "second-spending-breakdown-2": "",
                "second-spending-breakdown-3": "4",
                "second-spending-breakdown-4": "1",
            }
        )

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.question_errors[
            "second-spending-breakdown-question"
        ] == schema.error_messages["TOTAL_SUM_NOT_EQUALS"] % {"total": "10"}


def test_multi_calculation(app, answer_store, list_store):
    answer_total = Answer(answer_id="total-answer", value=10)

    answer_store.add_or_update(answer_total)

    with app.test_request_context():
        schema = load_schema_from_name("test_validation_sum_against_total_multiple")

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
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )
        form.validate()

        assert len(form.question_errors) == 0

        # With the data equaling the total question validation should pass
        form_data["breakdown-1"] = "10"

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )
        form.validate()

        assert len(form.question_errors) == 0

        # With the data not equaling zero or the total, question validation should fail
        form_data["breakdown-1"] = "1"

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )
        form.validate()

        assert form.question_errors["breakdown-question"] == schema.error_messages[
            "TOTAL_SUM_NOT_EQUALS"
        ] % {"total": "10"}


def test_generate_form_with_title_and_no_answer_label(app, answer_store, list_store):
    """
    Checks that the form is still generated when there is no answer label but there is a question title
    """
    conditional_answer = Answer(answer_id="behalf-of-answer", value="chad")

    answer_store.add_or_update(conditional_answer)

    with app.test_request_context():
        schema = load_schema_from_name("test_title")

        question_schema = schema.get_block("single-title-block").get("question")

        form_data = MultiDict({"feeling-answer": "Good"})

        expected_form_data = {"csrf_token": None, "feeling-answer": "Good"}

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.data == expected_form_data


def test_form_errors_are_correctly_mapped(app, answer_store, list_store):
    with app.test_request_context():
        schema = load_schema_from_name("test_numbers")

        question_schema = schema.get_block("set-min-max-block").get("question")

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        mapped_errors = form.map_errors()

        assert error_exists(
            "set-minimum", schema.error_messages["MANDATORY_NUMBER"], mapped_errors
        )


def test_form_subfield_errors_are_correctly_mapped(app, answer_store, list_store):
    with app.test_request_context():
        schema = load_schema_from_name("test_date_range")

        question_schema = schema.get_block("date-block").get("question")

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        mapped_errors = form.map_errors()

        assert error_exists(
            "date-range-from-answer",
            schema.error_messages["MANDATORY_DATE"],
            mapped_errors,
        )

        assert error_exists(
            "date-range-to-answer",
            schema.error_messages["MANDATORY_DATE"],
            mapped_errors,
        )


def test_detail_answer_mandatory_only_checked_if_option_selected(
    app, answer_store, list_store
):
    # The detail_answer can only be mandatory if the option it is associated with is answered
    with app.test_request_context():
        schema = load_schema_from_name("test_checkbox_detail_answer_multiple")

        question_schema = schema.get_block("mandatory-checkbox").get("question")

        #  Option is selected therefore the detail answer should be mandatory (schema defined)
        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=MultiDict({"mandatory-checkbox-answer": "Your choice"}),
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        detail_answer_field = getattr(form, "your-choice-answer-mandatory")
        assert isinstance(detail_answer_field.validators[0], ResponseRequired)

        #  Option not selected therefore the detail answer should not be mandatory
        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            data={"mandatory-checkbox-answer": "Ham"},
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        detail_answer_field = getattr(form, "your-choice-answer-mandatory")
        assert detail_answer_field.validators == ()


def test_answer_with_detail_answer_errors_are_correctly_mapped(
    app, answer_store, list_store
):
    with app.test_request_context():
        schema = load_schema_from_name(
            "test_radio_mandatory_with_detail_answer_mandatory"
        )

        question_schema = schema.get_block("radio-mandatory").get("question")

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=MultiDict({"radio-mandatory-answer": "Other"}),
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        mapped_errors = form.map_errors()

        assert error_exists(
            "radio-mandatory-answer",
            schema.error_messages["MANDATORY_TEXTFIELD"],
            mapped_errors,
        )
        assert not error_exists(
            "other-answer-mandatory",
            schema.error_messages["MANDATORY_TEXTFIELD"],
            mapped_errors,
        )


def test_answer_errors_are_interpolated(app, answer_store, list_store):
    with app.test_request_context():
        schema = load_schema_from_name("test_numbers")

        question_schema = schema.get_block("set-min-max-block").get("question")

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=MultiDict({"set-minimum": "-10001"}),
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        answer_errors = form.answer_errors("set-minimum")
        assert (
            schema.error_messages["NUMBER_TOO_SMALL"] % {"min": "-1,000"}
            in answer_errors
        )


def test_mandatory_mutually_exclusive_question_raises_error_when_not_answered(
    app, answer_store, list_store
):
    with app.test_request_context():
        schema = load_schema_from_name("test_mutually_exclusive")

        question_schema = schema.get_block("mutually-exclusive-mandatory-date").get(
            "question"
        )

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=MultiDict(),
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )
        form.validate_mutually_exclusive_question(question_schema)

        assert form.question_errors[
            "mutually-exclusive-mandatory-date-question"
        ] == format_message_with_title(
            error_messages["MANDATORY_QUESTION"], question_schema.get("title")
        )


def test_mandatory_mutually_exclusive_question_raises_error_with_question_text(
    app, list_store
):
    with app.test_request_context():
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
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            schema=schema,
            progress_store=ProgressStore(),
            location=Location(section_id="mutually-exclusive-checkbox-section"),
            supplementary_data_store=SupplementaryDataStore(),
        )
        rendered_schema = renderer.render(
            data_to_render=question_schema, list_item_id=None
        )

        form = generate_form(
            schema=schema,
            question_schema=rendered_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=MultiDict(),
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )
        form.validate_mutually_exclusive_question(question_schema)
        error = form.question_errors["mutually-exclusive-checkbox-question"]

        assert error == format_message_with_title(
            error_messages["MANDATORY_CHECKBOX"],
            "Did you really answer ‘Tuna’ to the previous question?",
        )


def test_mutually_exclusive_question_raises_error_when_both_answered(
    app, answer_store, list_store
):
    with app.test_request_context():
        schema = load_schema_from_name("test_mutually_exclusive")

        question_schema = schema.get_block("mutually-exclusive-date").get("question")

        form_data = MultiDict(
            {
                "date-answer-day": "17",
                "date-answer-month": "9",
                "date-answer-year": "2018",
                "date-exclusive-answer": "I prefer not to say",
            }
        )

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )
        form.validate_mutually_exclusive_question(question_schema)

        assert (
            form.question_errors["mutually-exclusive-date-question"]
            == error_messages["MUTUALLY_EXCLUSIVE"]
        )


def test_date_range_form(app, answer_store, list_store):
    with app.test_request_context():
        schema = load_schema_from_name("test_date_range")
        question_schema = schema.get_block("date-block").get("question")

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        assert hasattr(form, "date-range-from-answer")
        assert hasattr(form, "date-range-to-answer")

        period_from_field = getattr(form, "date-range-from-answer")
        period_to_field = getattr(form, "date-range-to-answer")

        assert isinstance(period_from_field.year.validators[0], DateRequired)
        assert isinstance(period_to_field.year.validators[0], DateRequired)


def test_date_range_form_with_data(app, answer_store, list_store):
    with app.test_request_context():
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
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        assert hasattr(form, "date-range-from-answer")
        assert hasattr(form, "date-range-to-answer")

        period_from_field = getattr(form, "date-range-from-answer")
        period_to_field = getattr(form, "date-range-to-answer")

        assert isinstance(period_from_field.year.validators[0], DateRequired)
        assert isinstance(period_to_field.year.validators[0], DateRequired)

        assert period_from_field.data == "2015-05-01"
        assert period_to_field.data == "2017-09-01"


def test_form_for_radio_other_not_selected(app, answer_store, list_store):
    with app.test_request_context():
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
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        assert hasattr(form, "radio-mandatory-answer")
        other_text_field = getattr(form, "other-answer-mandatory")
        assert other_text_field.data == ""


def test_form_for_radio_other_selected(app, answer_store, list_store):
    with app.test_request_context():
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
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            supplementary_data_store=SupplementaryDataStore(),
        )

        other_text_field = getattr(form, "other-answer-mandatory")
        assert other_text_field.data == "Other text field value"


def test_dynamic_answers_question_validates(app):
    with app.test_request_context():
        schema = load_schema_from_name(
            "test_validation_sum_against_total_dynamic_answers"
        )
        answer_store = AnswerStore([{"answer_id": "total-answer", "value": 100}])
        question_schema = schema.get_block("dynamic-answer").get("question")
        question_schema = QuestionnaireSchema.get_mutable_deepcopy(question_schema)
        question_schema["answers"].append(
            {
                "label": "Percentage of shopping at Tesco",
                "id": "percentage-of-shopping-lCIZsS",
                "mandatory": False,
                "type": "Percentage",
                "maximum": {"value": 100},
                "decimal_places": 0,
                "original_answer_id": "percentage-of-shopping",
                "list_item_id": "lCIZsS",
            }
        )

        list_store = ListStore([{"name": "supermarkets", "items": ["lCIZsS"]}])

        form_data = MultiDict(
            {
                "percentage-of-shopping-lCIZsS": "25",
                "percentage-of-shopping-elsewhere": "75",
            }
        )

        expected_form_data = {
            "csrf_token": None,
            "percentage-of-shopping-lCIZsS": "25",
            "percentage-of-shopping-elsewhere": "75",
        }

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            location=Location(
                section_id="section",
                block_id="dynamic-answer",
                list_name=None,
                list_item_id=None,
            ),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.data, expected_form_data


def test_dynamic_answers_question_raises_validation_error(app):
    with app.test_request_context():
        schema = load_schema_from_name(
            "test_validation_sum_against_total_dynamic_answers"
        )
        answer_store = AnswerStore([{"answer_id": "total-answer", "value": 100}])
        question_schema = schema.get_block("dynamic-answer").get("question")
        question_schema = QuestionnaireSchema.get_mutable_deepcopy(question_schema)
        question_schema["answers"].append(
            {
                "label": "Percentage of shopping at Tesco",
                "id": "percentage-of-shopping-lCIZsS",
                "mandatory": False,
                "type": "Percentage",
                "maximum": {"value": 100},
                "decimal_places": 0,
                "original_answer_id": "percentage-of-shopping",
                "list_item_id": "lCIZsS",
            }
        )

        list_store = ListStore([{"name": "supermarkets", "items": ["lCIZsS"]}])

        form_data = MultiDict(
            {
                "percentage-of-shopping-lCIZsS": "25",
                "percentage-of-shopping-elsewhere": "70",
            }
        )

        form = generate_form(
            schema=schema,
            question_schema=question_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=get_metadata(),
            response_metadata={},
            form_data=form_data,
            progress_store=ProgressStore(),
            location=Location(
                section_id="section",
                block_id="dynamic-answer",
                list_name=None,
                list_item_id=None,
            ),
            supplementary_data_store=SupplementaryDataStore(),
        )

        form.validate()
        assert form.question_errors["dynamic-answer-question"] == schema.error_messages[
            "TOTAL_SUM_NOT_EQUALS"
        ] % {"total": "100"}
