from datetime import datetime, timezone

import pytest

from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.submitter.converter import convert_answers
from app.submitter.converter_v2 import DataVersionError

SUBMITTED_AT = datetime.now(timezone.utc)


def test_convert_answers_flushed_flag_default_is_false(
    fake_questionnaire_schema, fake_questionnaire_store
):
    answer_object = convert_answers(
        fake_questionnaire_schema, fake_questionnaire_store, {}, SUBMITTED_AT
    )

    assert not answer_object["flushed"]


def test_ref_period_end_date_is_not_in_output(
    fake_questionnaire_schema, fake_questionnaire_store
):
    answer_object = convert_answers(
        fake_questionnaire_schema, fake_questionnaire_store, {}, SUBMITTED_AT
    )
    assert "ref_period_end_date" not in answer_object["metadata"]

    del fake_questionnaire_store.metadata["ref_p_end_date"]
    answer_object = convert_answers(
        fake_questionnaire_schema, fake_questionnaire_store, {}, SUBMITTED_AT
    )
    assert "ref_period_end_date" not in answer_object["metadata"]


def test_ref_period_start_and_end_date_is_in_output(
    fake_questionnaire_schema, fake_questionnaire_store
):
    answer_object = convert_answers(
        fake_questionnaire_schema, fake_questionnaire_store, {}, SUBMITTED_AT
    )
    assert answer_object["metadata"]["ref_period_start_date"] == "2016-02-02"
    assert answer_object["metadata"]["ref_period_end_date"] == "2016-03-03"


def test_convert_answers_flushed_flag_overriden_to_true(
    fake_questionnaire_schema, fake_questionnaire_store
):
    answer_object = convert_answers(
        fake_questionnaire_schema,
        fake_questionnaire_store,
        {},
        SUBMITTED_AT,
        flushed=True,
    )

    assert answer_object["flushed"]


def test_started_at_should_be_set_in_payload_if_present_in_response_metadata(
    fake_questionnaire_schema, fake_questionnaire_store
):
    answer_object = convert_answers(
        fake_questionnaire_schema, fake_questionnaire_store, {}, SUBMITTED_AT
    )

    assert (
        answer_object["started_at"]
        == fake_questionnaire_store.response_metadata["started_at"]
    )


def test_started_at_should_not_be_set_in_payload_if_absent_in_response_metadata(
    fake_questionnaire_schema,
    fake_questionnaire_store,
    fake_response_metadata,
    fake_metadata,
):
    del fake_response_metadata["started_at"]

    fake_questionnaire_store.set_metadata(fake_metadata)
    fake_questionnaire_store.response_metadata = fake_response_metadata

    answer_object = convert_answers(
        fake_questionnaire_schema, fake_questionnaire_store, {}, SUBMITTED_AT
    )

    assert "started_at" not in answer_object


def test_submitted_at_should_be_set_in_payload(
    fake_questionnaire_schema, fake_questionnaire_store
):
    answer_object = convert_answers(
        fake_questionnaire_schema, fake_questionnaire_store, {}, SUBMITTED_AT
    )

    assert SUBMITTED_AT.isoformat() == answer_object["submitted_at"]


def test_case_id_should_be_set_in_payload(
    fake_questionnaire_schema, fake_questionnaire_store
):
    answer_object = convert_answers(
        fake_questionnaire_schema, fake_questionnaire_store, {}, SUBMITTED_AT
    )

    assert answer_object["case_id"] == fake_questionnaire_store.metadata["case_id"]


def test_case_ref_should_be_set_in_payload(
    fake_questionnaire_schema, fake_questionnaire_store
):
    answer_object = convert_answers(
        fake_questionnaire_schema, fake_questionnaire_store, {}, SUBMITTED_AT
    )

    assert answer_object["case_ref"], fake_questionnaire_store.metadata["case_ref"]


def test_display_address_should_be_set_in_payload_metadata(
    fake_questionnaire_schema, fake_questionnaire_store
):
    payload = convert_answers(
        fake_questionnaire_schema, fake_questionnaire_store, {}, SUBMITTED_AT
    )

    assert payload["metadata"]["display_address"], fake_questionnaire_store.metadata[
        "display_address"
    ]


def test_instrument_id_is_not_in_payload_collection_if_form_type_absent_in_metadata(
    fake_questionnaire_schema, fake_questionnaire_store, fake_metadata
):
    del fake_metadata["form_type"]
    fake_questionnaire_store.set_metadata(fake_metadata)
    payload = convert_answers(
        fake_questionnaire_schema, fake_questionnaire_store, {}, SUBMITTED_AT
    )

    assert "instrument_id" not in payload["collection"]


def test_instrument_id_should_be_set_in_payload_collection_if_form_type_in_metadata(
    fake_questionnaire_schema, fake_questionnaire_store
):
    payload = convert_answers(
        fake_questionnaire_schema, fake_questionnaire_store, {}, SUBMITTED_AT
    )

    assert payload["collection"]["instrument_id"], "I"


def test_converter_raises_runtime_error_for_unsupported_version(
    fake_questionnaire_store,
):
    questionnaire = {"survey_id": "021", "data_version": "-0.0.1"}

    with pytest.raises(DataVersionError) as err:
        convert_answers(
            QuestionnaireSchema(questionnaire),
            fake_questionnaire_store,
            {},
            SUBMITTED_AT,
        )

    assert "Data version -0.0.1 not supported" in str(err.value)


def test_converter_language_code_not_set_in_payload(
    fake_questionnaire_schema,
    fake_questionnaire_store,
    fake_response_metadata,
    fake_metadata,
):
    fake_questionnaire_store.set_metadata(fake_metadata)
    fake_questionnaire_store.response_metadata = fake_response_metadata

    answer_object = convert_answers(
        fake_questionnaire_schema, fake_questionnaire_store, {}, SUBMITTED_AT
    )

    assert fake_questionnaire_store.metadata["language_code"] is None

    assert answer_object["launch_language_code"] == "en"


def test_converter_language_code_set_in_payload(
    fake_questionnaire_schema,
    fake_questionnaire_store,
    fake_response_metadata,
    fake_metadata,
):
    fake_metadata["language_code"] = "ga"
    fake_questionnaire_store.set_metadata(fake_metadata)
    fake_questionnaire_store.response_metadata = fake_response_metadata

    answer_object = convert_answers(
        fake_questionnaire_schema, fake_questionnaire_store, {}, SUBMITTED_AT
    )

    assert answer_object["launch_language_code"] == "ga"
