from copy import deepcopy

import pytest
from freezegun import freeze_time
from marshmallow import ValidationError

from app.utilities.metadata_parser_v2 import (
    validate_questionnaire_claims,
    validate_runner_claims_v2,
)
from tests.app.parser.conftest import (
    get_metadata,
    get_metadata_full,
    get_metadata_social,
)


def test_spaces_are_stripped_from_string_fields():
    metadata = get_metadata()
    metadata["collection_exercise_sid"] = "  stripped     "

    output = validate_runner_claims_v2(metadata)

    assert output["collection_exercise_sid"] == "stripped"


def test_empty_strings_are_not_valid():
    metadata = get_metadata()
    metadata["schema_name"] = ""

    with pytest.raises(ValidationError):
        validate_runner_claims_v2(metadata)


def test_validation_does_not_change_metadata(
    fake_questionnaire_metadata_requirements_full,
):
    metadata = get_metadata_full()

    fake_metadata_copy = deepcopy(metadata)

    questionnaire_claims = metadata["survey_metadata"]["data"]

    validate_questionnaire_claims(
        questionnaire_claims, fake_questionnaire_metadata_requirements_full
    )

    assert metadata == fake_metadata_copy


def test_validation_no_error_when_optional_field_not_passed():
    metadata = get_metadata_full()

    field_specification = [
        {"name": "optional_field", "type": "string", "optional": True}
    ]

    validate_questionnaire_claims(metadata, field_specification)


def test_validation_field_required_by_default():
    metadata = get_metadata_full()

    field_specification = [{"name": "required_field", "type": "string"}]

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(metadata, field_specification)


def test_minimum_length():
    metadata = get_metadata_full()

    field_specification = [{"name": "some_field", "type": "string", "min_length": 5}]

    questionnaire_claims = metadata["survey_metadata"]["data"]

    questionnaire_claims["some_field"] = "123456"

    validate_questionnaire_claims(questionnaire_claims, field_specification)

    questionnaire_claims["some_field"] = "1"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(questionnaire_claims, field_specification)


def test_maximum_length():
    metadata = get_metadata_full()

    field_specification = [{"name": "some_field", "type": "string", "max_length": 5}]

    questionnaire_claims = metadata["survey_metadata"]["data"]

    questionnaire_claims["some_field"] = "1234"

    validate_questionnaire_claims(questionnaire_claims, field_specification)

    questionnaire_claims["some_field"] = "123456"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(questionnaire_claims, field_specification)


def test_min_and_max_length():
    metadata = get_metadata_full()

    field_specification = [
        {"name": "some_field", "type": "string", "min_length": 4, "max_length": 5}
    ]

    questionnaire_claims = metadata["survey_metadata"]["data"]

    questionnaire_claims["some_field"] = "1234"

    validate_questionnaire_claims(questionnaire_claims, field_specification)

    questionnaire_claims["some_field"] = "123456"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(questionnaire_claims, field_specification)

    questionnaire_claims["some_field"] = "123"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(questionnaire_claims, field_specification)


def test_length_equals():
    metadata = get_metadata_full()

    field_specification = [{"name": "some_field", "type": "string", "length": 4}]

    questionnaire_claims = metadata["survey_metadata"]["data"]

    questionnaire_claims["some_field"] = "1234"

    validate_questionnaire_claims(questionnaire_claims, field_specification)

    questionnaire_claims["some_field"] = "123456"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(questionnaire_claims, field_specification)

    questionnaire_claims["some_field"] = "123"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(questionnaire_claims, field_specification)


def test_uuid_deserialisation():
    metadata = get_metadata_full()

    claims = validate_runner_claims_v2(metadata)

    assert isinstance(claims["tx_id"], str)


def test_unknown_claims_are_not_deserialized():
    metadata = get_metadata_full()

    metadata["unknown_key"] = "some value"
    claims = validate_runner_claims_v2(metadata)
    assert "unknown_key" not in claims


def test_minimum_length_on_runner_metadata():
    metadata = get_metadata_full()

    validate_runner_claims_v2(metadata)

    metadata["collection_exercise_sid"] = ""
    with pytest.raises(ValidationError):
        validate_runner_claims_v2(metadata)


def test_deserialisation_iso_8601_dates():
    """Runner cannot currently handle date objects in metadata"""
    metadata = get_metadata_full()

    field_specification = [{"name": "birthday", "type": "date"}]

    questionnaire_claims = metadata["survey_metadata"]["data"]

    questionnaire_claims["birthday"] = "2019-11-1"
    claims = validate_questionnaire_claims(questionnaire_claims, field_specification)

    assert isinstance(claims["birthday"], str)


@freeze_time("2021-11-15T15:34:54+00:00")
@pytest.mark.parametrize(
    "date_string",
    [
        ("2021-11-22T15:34:54+00:00"),
        ("2021-11-22T15:34:54Z"),
    ],
)
def test_deserialisation_iso_8601_date(date_string):
    metadata = get_metadata_full()

    metadata["response_expires_at"] = date_string

    claims = validate_runner_claims_v2(metadata)

    assert claims["response_expires_at"] == "2021-11-22T15:34:54+00:00"


def test_deserialisation_iso_8601_datetime_past_datetime_raises_ValidationError():
    metadata = get_metadata_full()

    metadata["response_expires_at"] = "1900-11-22T15:34:54+00:00"
    with pytest.raises(ValidationError):
        validate_runner_claims_v2(metadata)


@freeze_time("2021-11-15T15:34:54+00:00")
def test_deserialisation_iso_8601_datetime_bad_datetime_raises_ValidationError():
    metadata = get_metadata_full()

    metadata["response_expires_at"] = "2021-11-22"
    with pytest.raises(ValidationError):
        validate_runner_claims_v2(metadata)


def test_empty_schema_name_and_schema_url_and_cir_instrument_id_not_valid_v2():
    metadata = get_metadata_full()
    del metadata["schema_name"]

    with pytest.raises(ValidationError) as exc:
        validate_runner_claims_v2(metadata)

    assert (
        "Neither schema_name, schema_url or cir_instrument_id has been set in metadata"
        in str(exc)
    )


@pytest.mark.parametrize(
    "options",
    [
        {
            "schema_name": "test_name",
            "cir_instrument_id": "f0519981-426c-8b93-75c0-bfc40c66fe25",
        },
        {
            "schema_url": "http://test.json",
            "cir_instrument_id": "f0519981-426c-8b93-75c0-bfc40c66fe25",
        },
        {
            "schema_name": "test_name",
            "schema_url": "http://test.json",
            "cir_instrument_id": "f0519981-426c-8b93-75c0-bfc40c66fe25",
        },
        {"schema_name": "test_name", "schema_url": "http://test.json"},
    ],
)
def test_too_many_of_schema_name_schema_url_and_cir_instrument_id_not_valid_v2(options):
    metadata = get_metadata_full()
    del metadata["schema_name"]

    metadata.update(options)
    provided = ", ".join(options)

    with pytest.raises(ValidationError) as exc:
        validate_runner_claims_v2(metadata)

    assert (
        f"Only one of schema_name, schema_url or cir_instrument_id should be specified in metadata, but {provided} were provided"
        in str(exc)
    )


def test_valid_v2_social_claims():
    metadata = get_metadata_social()

    fake_metadata_copy = deepcopy(metadata)

    claims = validate_runner_claims_v2(metadata)

    assert claims == fake_metadata_copy


def test_invalid_v2_social_claims_missing_receipting_key_raises_error():
    metadata = get_metadata_social()

    del metadata["survey_metadata"]["data"]["qid"]

    with pytest.raises(ValidationError):
        validate_runner_claims_v2(metadata)
