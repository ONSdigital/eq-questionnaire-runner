from datetime import datetime, timezone

import pytest

from app.authentication.auth_payload_versions import AuthPayloadVersion
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.submitter.converter import convert_answers
from app.submitter.converter_v2 import (
    DataVersionError,
    NoMetadataException,
    convert_answers_v2,
)
from tests.app.questionnaire.conftest import get_metadata
from tests.app.submitter.conftest import get_questionnaire_store

SUBMITTED_AT = datetime.now(timezone.utc)


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_convert_answers_v2_flushed_flag_default_is_false(
    fake_questionnaire_schema, version
):
    questionnaire_store = get_questionnaire_store(version)

    converter = (
        convert_answers_v2 if version is AuthPayloadVersion.V2 else convert_answers
    )

    answer_object = converter(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert not answer_object["flushed"]


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_convert_answers_v2_flushed_flag_overriden_to_true(
    fake_questionnaire_schema, version
):
    questionnaire_store = get_questionnaire_store(version)

    converter = (
        convert_answers_v2 if version is AuthPayloadVersion.V2 else convert_answers
    )

    answer_object = converter(
        fake_questionnaire_schema,
        questionnaire_store,
        {},
        SUBMITTED_AT,
        flushed=True,
    )

    assert answer_object["flushed"]


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_started_at_should_be_set_in_payload_if_present_in_response_metadata(
    fake_questionnaire_schema, version
):
    questionnaire_store = get_questionnaire_store(version)

    converter = (
        convert_answers_v2 if version is AuthPayloadVersion.V2 else convert_answers
    )

    answer_object = converter(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert (
        answer_object["started_at"]
        == questionnaire_store.stores.response_metadata["started_at"]
    )


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_started_at_should_not_be_set_in_payload_if_absent_in_response_metadata(
    fake_questionnaire_schema, fake_response_metadata, version
):
    del fake_response_metadata["started_at"]
    questionnaire_store = get_questionnaire_store(version)
    questionnaire_store.stores.response_metadata = fake_response_metadata

    converter = (
        convert_answers_v2 if version is AuthPayloadVersion.V2 else convert_answers
    )

    answer_object = converter(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert "started_at" not in answer_object


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_submitted_at_should_be_set_in_payload(fake_questionnaire_schema, version):
    questionnaire_store = get_questionnaire_store(version)

    converter = (
        convert_answers_v2 if version is AuthPayloadVersion.V2 else convert_answers
    )

    answer_object = converter(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert SUBMITTED_AT.isoformat() == answer_object["submitted_at"]


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_case_id_should_be_set_in_payload(fake_questionnaire_schema, version):
    questionnaire_store = get_questionnaire_store(version)

    converter = (
        convert_answers_v2 if version is AuthPayloadVersion.V2 else convert_answers
    )

    answer_object = converter(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert answer_object["case_id"] == questionnaire_store.stores.metadata.case_id


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_case_ref_should_be_set_in_payload(fake_questionnaire_schema, version):
    questionnaire_store = get_questionnaire_store(version)

    converter = (
        convert_answers_v2 if version is AuthPayloadVersion.V2 else convert_answers
    )

    answer_object = converter(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    if version is AuthPayloadVersion.V2:
        assert answer_object["survey_metadata"][
            "case_ref"
        ], questionnaire_store.stores.metadata["survey_metadata"]["data"]["case_ref"]
    else:
        assert answer_object["case_ref"], questionnaire_store.stores.metadata[
            "case_ref"
        ]


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_display_address_should_be_set_in_payload_metadata(
    fake_questionnaire_schema, version
):
    questionnaire_store = get_questionnaire_store(version)

    converter = (
        convert_answers_v2 if version is AuthPayloadVersion.V2 else convert_answers
    )

    payload = converter(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    if version is AuthPayloadVersion.V2:
        assert payload["survey_metadata"][
            "display_address"
        ], questionnaire_store.stores.metadata["survey_metadata"]["data"][
            "display_address"
        ]
    else:
        assert payload["metadata"][
            "display_address"
        ], questionnaire_store.stores.metadata["display_address"]


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_converter_raises_runtime_error_for_unsupported_version(version):
    questionnaire_store = get_questionnaire_store(version)
    questionnaire = {"survey_id": "021", "data_version": "-0.0.1"}

    converter = (
        convert_answers_v2 if version is AuthPayloadVersion.V2 else convert_answers
    )

    with pytest.raises(DataVersionError) as err:
        converter(
            QuestionnaireSchema(questionnaire),
            questionnaire_store,
            {},
            SUBMITTED_AT,
        )

    assert "Data version -0.0.1 not supported" in str(err.value)


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_converter_language_code_not_set_in_payload(
    fake_questionnaire_schema, fake_response_metadata, version
):
    questionnaire_store = get_questionnaire_store(version)
    questionnaire_store.stores.response_metadata = fake_response_metadata

    converter = (
        convert_answers_v2 if version is AuthPayloadVersion.V2 else convert_answers
    )

    answer_object = converter(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert questionnaire_store.stores.metadata["language_code"] is None

    assert answer_object["launch_language_code"] == "en"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_converter_language_code_set_in_payload(
    fake_questionnaire_schema, fake_response_metadata, version
):
    questionnaire_store = get_questionnaire_store(version)
    questionnaire_store.stores.metadata = get_metadata({"language_code": "ga"})
    questionnaire_store.stores.response_metadata = fake_response_metadata

    converter = (
        convert_answers_v2 if version is AuthPayloadVersion.V2 else convert_answers
    )

    answer_object = converter(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert answer_object["launch_language_code"] == "ga"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_no_metadata_raises_exception(fake_questionnaire_schema, version):
    questionnaire_store = get_questionnaire_store(version)

    questionnaire_store.stores.metadata = None

    converter = (
        convert_answers_v2 if version is AuthPayloadVersion.V2 else convert_answers
    )

    with pytest.raises(NoMetadataException):
        converter(fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT)


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_data_object_set_in_payload(
    fake_questionnaire_schema, fake_response_metadata, version
):
    questionnaire_store = get_questionnaire_store(version)
    questionnaire_store.stores.response_metadata = fake_response_metadata

    converter = (
        convert_answers_v2 if version is AuthPayloadVersion.V2 else convert_answers
    )

    answer_object = converter(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert "data" in answer_object


def test_instrument_id_is_not_in_payload_collection_if_form_type_absent_in_metadata(
    fake_questionnaire_schema,
):
    questionnaire_store = get_questionnaire_store("v1")

    questionnaire_store.stores.metadata = get_metadata({"form_type": None})

    payload = convert_answers(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert "instrument_id" not in payload["collection"]


def test_instrument_id_should_be_set_in_payload_collection_if_form_type_in_metadata(
    fake_questionnaire_schema,
):
    questionnaire_store = get_questionnaire_store("v1")

    payload = convert_answers(
        fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
    )

    assert payload["collection"]["instrument_id"], "I"
