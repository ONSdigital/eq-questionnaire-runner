from datetime import datetime, timezone

import pytest

from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.submitter.converter_v2 import DataVersionError, convert_answers_v2

SUBMITTED_AT = datetime.now(timezone.utc)


def test_convert_answers_v2_flushed_flag_default_is_false(
    fake_questionnaire_schema, fake_questionnaire_store_v2
):
    answer_object = convert_answers_v2(
        fake_questionnaire_schema, fake_questionnaire_store_v2, {}, SUBMITTED_AT
    )

    assert not answer_object["flushed"]


def test_convert_answers_v2_flushed_flag_overriden_to_true(
    fake_questionnaire_schema, fake_questionnaire_store_v2
):
    answer_object = convert_answers_v2(
        fake_questionnaire_schema,
        fake_questionnaire_store_v2,
        {},
        SUBMITTED_AT,
        flushed=True,
    )

    assert answer_object["flushed"]


def test_started_at_should_be_set_in_payload_if_present_in_response_metadata(
    fake_questionnaire_schema, fake_questionnaire_store_v2
):
    answer_object = convert_answers_v2(
        fake_questionnaire_schema, fake_questionnaire_store_v2, {}, SUBMITTED_AT
    )

    assert (
        answer_object["started_at"]
        == fake_questionnaire_store_v2.response_metadata["started_at"]
    )


def test_started_at_should_not_be_set_in_payload_if_absent_in_response_metadata(
    fake_questionnaire_schema,
    fake_questionnaire_store_v2,
    fake_response_metadata,
    fake_metadata_v2,
):
    del fake_response_metadata["started_at"]

    fake_questionnaire_store_v2.set_metadata(fake_metadata_v2)
    fake_questionnaire_store_v2.response_metadata = fake_response_metadata

    answer_object = convert_answers_v2(
        fake_questionnaire_schema, fake_questionnaire_store_v2, {}, SUBMITTED_AT
    )

    assert "started_at" not in answer_object


def test_submitted_at_should_be_set_in_payload(
    fake_questionnaire_schema, fake_questionnaire_store_v2
):
    answer_object = convert_answers_v2(
        fake_questionnaire_schema, fake_questionnaire_store_v2, {}, SUBMITTED_AT
    )

    assert SUBMITTED_AT.isoformat() == answer_object["submitted_at"]


def test_case_id_should_be_set_in_payload(
    fake_questionnaire_schema, fake_questionnaire_store_v2
):
    answer_object = convert_answers_v2(
        fake_questionnaire_schema, fake_questionnaire_store_v2, {}, SUBMITTED_AT
    )

    assert answer_object["case_id"] == fake_questionnaire_store_v2.metadata["case_id"]


def test_case_ref_should_be_set_in_payload(
    fake_questionnaire_schema, fake_questionnaire_store_v2
):
    answer_object = convert_answers_v2(
        fake_questionnaire_schema, fake_questionnaire_store_v2, {}, SUBMITTED_AT
    )

    assert answer_object["survey_metadata"][
        "case_ref"
    ], fake_questionnaire_store_v2.metadata["survey_metadata"]["data"]["case_ref"]


def test_display_address_should_be_set_in_payload_metadata(
    fake_questionnaire_schema, fake_questionnaire_store_v2
):
    payload = convert_answers_v2(
        fake_questionnaire_schema, fake_questionnaire_store_v2, {}, SUBMITTED_AT
    )

    assert payload["survey_metadata"][
        "display_address"
    ], fake_questionnaire_store_v2.metadata["survey_metadata"]["data"][
        "display_address"
    ]


def test_converter_raises_runtime_error_for_unsupported_version(
    fake_questionnaire_store_v2,
):
    questionnaire = {"survey_id": "021", "data_version": "-0.0.1"}

    with pytest.raises(DataVersionError) as err:
        convert_answers_v2(
            QuestionnaireSchema(questionnaire),
            fake_questionnaire_store_v2,
            {},
            SUBMITTED_AT,
        )

    assert "Data version -0.0.1 not supported" in str(err.value)


def test_converter_language_code_not_set_in_payload(
    fake_questionnaire_schema,
    fake_questionnaire_store_v2,
    fake_response_metadata,
    fake_metadata_v2,
):
    fake_questionnaire_store_v2.set_metadata(fake_metadata_v2)
    fake_questionnaire_store_v2.response_metadata = fake_response_metadata

    answer_object = convert_answers_v2(
        fake_questionnaire_schema, fake_questionnaire_store_v2, {}, SUBMITTED_AT
    )

    assert fake_questionnaire_store_v2.metadata["language_code"] is None

    assert answer_object["launch_language_code"] == "en"


def test_converter_language_code_set_in_payload(
    fake_questionnaire_schema,
    fake_questionnaire_store_v2,
    fake_response_metadata,
    fake_metadata_v2,
):
    fake_metadata_v2["language_code"] = "ga"
    fake_questionnaire_store_v2.set_metadata(fake_metadata_v2)
    fake_questionnaire_store_v2.response_metadata = fake_response_metadata

    answer_object = convert_answers_v2(
        fake_questionnaire_schema, fake_questionnaire_store_v2, {}, SUBMITTED_AT
    )

    assert answer_object["launch_language_code"] == "ga"
