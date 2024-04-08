from datetime import datetime, timezone

import pytest

from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.submitter.converter_v2 import (
    DataVersionError,
    NoMetadataException,
    convert_answers_v2,
)
from tests.app.questionnaire.conftest import get_metadata
from tests.app.submitter.conftest import get_questionnaire_store

SUBMITTED_AT = datetime.now(timezone.utc)


def test_convert_answers_v2_flushed_flag_default_is_false(fake_questionnaire_schema):
    questionnaire_store = get_questionnaire_store()

    answer_object = convert_answers_v2(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert not answer_object["flushed"]


def test_convert_answers_v2_flushed_flag_overriden_to_true(fake_questionnaire_schema):
    questionnaire_store = get_questionnaire_store()

    answer_object = convert_answers_v2(
        fake_questionnaire_schema,
        questionnaire_store,
        {},
        SUBMITTED_AT,
        flushed=True,
    )

    assert answer_object["flushed"]


def test_started_at_should_be_set_in_payload_if_present_in_response_metadata(
    fake_questionnaire_schema,
):
    questionnaire_store = get_questionnaire_store()

    answer_object = convert_answers_v2(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert (
        answer_object["started_at"]
        == questionnaire_store.data_stores.response_metadata["started_at"]
    )


def test_started_at_should_not_be_set_in_payload_if_absent_in_response_metadata(
    fake_questionnaire_schema, fake_response_metadata
):
    del fake_response_metadata["started_at"]
    questionnaire_store = get_questionnaire_store()
    questionnaire_store.data_stores.response_metadata = fake_response_metadata

    answer_object = convert_answers_v2(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert "started_at" not in answer_object


def test_submitted_at_should_be_set_in_payload(fake_questionnaire_schema):
    questionnaire_store = get_questionnaire_store()

    answer_object = convert_answers_v2(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert SUBMITTED_AT.isoformat() == answer_object["submitted_at"]


def test_case_id_should_be_set_in_payload(fake_questionnaire_schema):
    questionnaire_store = get_questionnaire_store()

    answer_object = convert_answers_v2(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert answer_object["case_id"] == questionnaire_store.data_stores.metadata.case_id


def test_case_ref_should_be_set_in_payload(fake_questionnaire_schema):
    questionnaire_store = get_questionnaire_store()

    answer_object = convert_answers_v2(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert answer_object["survey_metadata"][
        "case_ref"
    ], questionnaire_store.data_stores.metadata["survey_metadata"]["data"]["case_ref"]


def test_display_address_should_be_set_in_payload_metadata(fake_questionnaire_schema):
    questionnaire_store = get_questionnaire_store()

    payload = convert_answers_v2(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert payload["survey_metadata"][
        "display_address"
    ], questionnaire_store.data_stores.metadata["survey_metadata"]["data"][
        "display_address"
    ]


def test_converter_raises_runtime_error_for_unsupported_version():
    questionnaire_store = get_questionnaire_store()
    questionnaire = {"survey_id": "021", "data_version": "-0.0.1"}

    with pytest.raises(DataVersionError) as err:
        convert_answers_v2(
            QuestionnaireSchema(questionnaire),
            questionnaire_store,
            {},
            SUBMITTED_AT,
        )

    assert "Data version -0.0.1 not supported" in str(err.value)


def test_converter_language_code_not_set_in_payload(
    fake_questionnaire_schema, fake_response_metadata
):
    questionnaire_store = get_questionnaire_store()
    questionnaire_store.data_stores.response_metadata = fake_response_metadata

    answer_object = convert_answers_v2(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert questionnaire_store.data_stores.metadata["language_code"] is None

    assert answer_object["launch_language_code"] == "en"


def test_converter_language_code_set_in_payload(
    fake_questionnaire_schema, fake_response_metadata
):
    questionnaire_store = get_questionnaire_store()
    questionnaire_store.data_stores.metadata = get_metadata(
        extra_metadata={"language_code": "ga"}
    )
    questionnaire_store.data_stores.response_metadata = fake_response_metadata

    answer_object = convert_answers_v2(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert answer_object["launch_language_code"] == "ga"


def test_no_metadata_raises_exception(fake_questionnaire_schema):
    questionnaire_store = get_questionnaire_store()

    questionnaire_store.data_stores.metadata = None

    with pytest.raises(NoMetadataException):
        convert_answers_v2(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )


def test_data_object_set_in_payload(fake_questionnaire_schema, fake_response_metadata):
    questionnaire_store = get_questionnaire_store()
    questionnaire_store.data_stores.response_metadata = fake_response_metadata

    answer_object = convert_answers_v2(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert "data" in answer_object


def test_schema_url_in_metadata_should_be_in_payload(
    fake_metadata_v2_schema_url, fake_questionnaire_schema
):
    questionnaire_store = get_questionnaire_store()
    questionnaire_store.data_stores.metadata = fake_metadata_v2_schema_url

    payload = convert_answers_v2(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert "schema_url" in payload
    assert "schema_name" not in payload
    assert "cir_instrument_id" not in payload
    assert payload["schema_url"] == fake_metadata_v2_schema_url["schema_url"]


def test_cir_instrument_id_in_metadata_should_be_in_payload(
    fake_metadata_v2_cir_instrument_id, fake_questionnaire_schema
):
    questionnaire_store = get_questionnaire_store()
    questionnaire_store.data_stores.metadata = fake_metadata_v2_cir_instrument_id

    payload = convert_answers_v2(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert "schema_url" not in payload
    assert "schema_name" not in payload
    assert "cir_instrument_id" in payload
    assert (
        payload["cir_instrument_id"]
        == fake_metadata_v2_cir_instrument_id["cir_instrument_id"]
    )
