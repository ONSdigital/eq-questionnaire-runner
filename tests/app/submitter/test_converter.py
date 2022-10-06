from datetime import datetime, timezone

import pytest

from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.submitter.converter import convert_answers
from app.submitter.converter_v2 import (
    DataVersionError,
    NoMetadataException,
    convert_answers_v2,
)
from tests.app.submitter.conftest import get_questionnaire_store

SUBMITTED_AT = datetime.now(timezone.utc)


@pytest.mark.parametrize(
    "version",
    (
        "v1",
        "v2",
    ),
)
def test_convert_answers_v2_flushed_flag_default_is_false(
    fake_questionnaire_schema, version
):
    questionnaire_store = get_questionnaire_store(version)

    if version == "v2":
        answer_object = convert_answers_v2(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )
    else:
        answer_object = convert_answers(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )

    assert not answer_object["flushed"]


@pytest.mark.parametrize(
    "version",
    (
        "v1",
        "v2",
    ),
)
def test_convert_answers_v2_flushed_flag_overriden_to_true(
    fake_questionnaire_schema, version
):
    questionnaire_store = get_questionnaire_store(version)

    if version == "v2":
        answer_object = convert_answers_v2(
            fake_questionnaire_schema,
            questionnaire_store,
            {},
            SUBMITTED_AT,
            flushed=True,
        )
    else:
        answer_object = convert_answers(
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
        "v1",
        "v2",
    ),
)
def test_started_at_should_be_set_in_payload_if_present_in_response_metadata(
    fake_questionnaire_schema, version
):
    questionnaire_store = get_questionnaire_store(version)

    if version == "v2":
        answer_object = convert_answers_v2(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )
    else:
        answer_object = convert_answers(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )

    assert (
        answer_object["started_at"]
        == questionnaire_store.response_metadata["started_at"]
    )


@pytest.mark.parametrize(
    "version",
    (
        "v1",
        "v2",
    ),
)
def test_started_at_should_not_be_set_in_payload_if_absent_in_response_metadata(
    fake_questionnaire_schema, fake_response_metadata, version
):
    del fake_response_metadata["started_at"]
    questionnaire_store = get_questionnaire_store(version)
    questionnaire_store.response_metadata = fake_response_metadata

    if version == "v2":
        answer_object = convert_answers_v2(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )
    else:
        answer_object = convert_answers(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )

    assert "started_at" not in answer_object


@pytest.mark.parametrize(
    "version",
    (
        "v1",
        "v2",
    ),
)
def test_submitted_at_should_be_set_in_payload(fake_questionnaire_schema, version):
    questionnaire_store = get_questionnaire_store(version)

    if version == "v2":
        answer_object = convert_answers_v2(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )
    else:
        answer_object = convert_answers(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )

    assert SUBMITTED_AT.isoformat() == answer_object["submitted_at"]


@pytest.mark.parametrize(
    "version",
    (
        "v1",
        "v2",
    ),
)
def test_case_id_should_be_set_in_payload(fake_questionnaire_schema, version):
    questionnaire_store = get_questionnaire_store(version)

    if version == "v2":
        answer_object = convert_answers_v2(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )
    else:
        answer_object = convert_answers(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )

    assert answer_object["case_id"] == questionnaire_store.metadata.case_id


@pytest.mark.parametrize(
    "version",
    (
        "v1",
        "v2",
    ),
)
def test_case_ref_should_be_set_in_payload(fake_questionnaire_schema, version):
    questionnaire_store = get_questionnaire_store(version)

    if version == "v2":
        answer_object = convert_answers_v2(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )

        assert answer_object["survey_metadata"][
            "case_ref"
        ], questionnaire_store.metadata["survey_metadata"]["data"]["case_ref"]
    else:
        answer_object = convert_answers(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )

        assert answer_object["case_ref"], questionnaire_store.metadata["case_ref"]


@pytest.mark.parametrize(
    "version",
    (
        "v1",
        "v2",
    ),
)
def test_display_address_should_be_set_in_payload_metadata(
    fake_questionnaire_schema, version
):
    questionnaire_store = get_questionnaire_store(version)

    if version == "v2":
        payload = convert_answers_v2(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )

        assert payload["survey_metadata"][
            "display_address"
        ], questionnaire_store.metadata["survey_metadata"]["data"]["display_address"]
    else:
        payload = convert_answers(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )

        assert payload["metadata"]["display_address"], questionnaire_store.metadata[
            "display_address"
        ]


@pytest.mark.parametrize(
    "version",
    (
        "v1",
        "v2",
    ),
)
def test_converter_raises_runtime_error_for_unsupported_version(version):
    questionnaire_store = get_questionnaire_store(version)
    questionnaire = {"survey_id": "021", "data_version": "-0.0.1"}

    if version == "v2":
        with pytest.raises(DataVersionError) as err:
            convert_answers_v2(
                QuestionnaireSchema(questionnaire),
                questionnaire_store,
                {},
                SUBMITTED_AT,
            )
    else:
        with pytest.raises(DataVersionError) as err:
            convert_answers(
                QuestionnaireSchema(questionnaire),
                questionnaire_store,
                {},
                SUBMITTED_AT,
            )

    assert "Data version -0.0.1 not supported" in str(err.value)


@pytest.mark.parametrize(
    "version",
    (
        "v1",
        "v2",
    ),
)
def test_converter_language_code_not_set_in_payload(
    fake_questionnaire_schema, fake_response_metadata, version
):
    questionnaire_store = get_questionnaire_store(version)
    questionnaire_store.response_metadata = fake_response_metadata

    if version == "v2":
        answer_object = convert_answers_v2(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )
    else:
        answer_object = convert_answers(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )

    assert questionnaire_store.metadata["language_code"] is None

    assert answer_object["launch_language_code"] == "en"


@pytest.mark.parametrize(
    "version",
    (
        "v1",
        "v2",
    ),
)
def test_converter_language_code_set_in_payload(
    fake_questionnaire_schema, fake_response_metadata, version
):
    questionnaire_store = get_questionnaire_store(version)
    questionnaire_store.metadata = MetadataProxy.from_dict({"language_code": "ga"})
    questionnaire_store.response_metadata = fake_response_metadata

    if version == "v2":
        answer_object = convert_answers_v2(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )
    else:
        answer_object = convert_answers(
            fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
        )

    assert answer_object["launch_language_code"] == "ga"


@pytest.mark.parametrize(
    "version",
    (
        "v1",
        "v2",
    ),
)
def test_no_metadata_raises_exception(fake_questionnaire_schema, version):
    questionnaire_store = get_questionnaire_store(version)

    questionnaire_store.metadata = None

    if version == "v2":
        with pytest.raises(NoMetadataException):
            convert_answers_v2(
                fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
            )
    else:
        with pytest.raises(NoMetadataException):
            convert_answers(
                fake_questionnaire_schema, questionnaire_store, {}, SUBMITTED_AT
            )


def test_instrument_id_is_not_in_payload_collection_if_form_type_absent_in_metadata(
    fake_questionnaire_schema,
):
    questionnaire_store = get_questionnaire_store("v1")

    questionnaire_store.metadata = MetadataProxy.from_dict({"form_type": None})

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
