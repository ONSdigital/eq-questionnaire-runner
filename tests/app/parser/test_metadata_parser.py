from copy import deepcopy

import pytest
from freezegun import freeze_time
from marshmallow import ValidationError

from app.authentication.auth_payload_versions import AuthPayloadVersion
from app.utilities.metadata_parser import validate_runner_claims
from app.utilities.metadata_parser_v2 import (
    validate_questionnaire_claims,
    validate_runner_claims_v2,
)
from tests.app.parser.conftest import (
    get_metadata,
    get_metadata_full,
    get_metadata_social,
)


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_spaces_are_stripped_from_string_fields(version):
    metadata = get_metadata(version)
    metadata["collection_exercise_sid"] = "  stripped     "

    validator = (
        validate_runner_claims_v2
        if version is AuthPayloadVersion.V2
        else validate_runner_claims
    )
    output = validator(metadata)

    assert output["collection_exercise_sid"] == "stripped"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_empty_strings_are_not_valid(version):
    metadata = get_metadata(version)
    metadata["schema_name"] = ""

    validator = (
        validate_runner_claims_v2
        if version is AuthPayloadVersion.V2
        else validate_runner_claims
    )

    with pytest.raises(ValidationError):
        validator(metadata)


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_validation_does_not_change_metadata(
    version, fake_questionnaire_metadata_requirements_full
):
    metadata = get_metadata_full(version)

    fake_metadata_copy = deepcopy(metadata)

    if version is AuthPayloadVersion.V2:
        questionnaire_claims = metadata["survey_metadata"]["data"]
    else:
        questionnaire_claims = metadata

    validate_questionnaire_claims(
        questionnaire_claims, fake_questionnaire_metadata_requirements_full
    )

    assert metadata == fake_metadata_copy


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_validation_no_error_when_optional_field_not_passed(version):
    metadata = get_metadata_full(version)

    field_specification = [
        {"name": "optional_field", "type": "string", "optional": True}
    ]

    validate_questionnaire_claims(metadata, field_specification)


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_validation_field_required_by_default(version):
    metadata = get_metadata_full(version)

    field_specification = [{"name": "required_field", "type": "string"}]

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(metadata, field_specification)


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_minimum_length(version):
    metadata = get_metadata_full(version)

    field_specification = [{"name": "some_field", "type": "string", "min_length": 5}]

    if version is AuthPayloadVersion.V2:
        questionnaire_claims = metadata["survey_metadata"]["data"]
    else:
        questionnaire_claims = metadata

    questionnaire_claims["some_field"] = "123456"

    validate_questionnaire_claims(questionnaire_claims, field_specification)

    questionnaire_claims["some_field"] = "1"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(questionnaire_claims, field_specification)


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_maximum_length(version):
    metadata = get_metadata_full(version)

    field_specification = [{"name": "some_field", "type": "string", "max_length": 5}]

    if version is AuthPayloadVersion.V2:
        questionnaire_claims = metadata["survey_metadata"]["data"]
    else:
        questionnaire_claims = metadata

    questionnaire_claims["some_field"] = "1234"

    validate_questionnaire_claims(questionnaire_claims, field_specification)

    questionnaire_claims["some_field"] = "123456"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(questionnaire_claims, field_specification)


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_min_and_max_length(version):
    metadata = get_metadata_full(version)

    field_specification = [
        {"name": "some_field", "type": "string", "min_length": 4, "max_length": 5}
    ]

    if version is AuthPayloadVersion.V2:
        questionnaire_claims = metadata["survey_metadata"]["data"]
    else:
        questionnaire_claims = metadata

    questionnaire_claims["some_field"] = "1234"

    validate_questionnaire_claims(questionnaire_claims, field_specification)

    questionnaire_claims["some_field"] = "123456"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(questionnaire_claims, field_specification)

    questionnaire_claims["some_field"] = "123"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(questionnaire_claims, field_specification)


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_length_equals(version):
    metadata = get_metadata_full(version)

    field_specification = [{"name": "some_field", "type": "string", "length": 4}]

    if version is AuthPayloadVersion.V2:
        questionnaire_claims = metadata["survey_metadata"]["data"]
    else:
        questionnaire_claims = metadata

    questionnaire_claims["some_field"] = "1234"

    validate_questionnaire_claims(questionnaire_claims, field_specification)

    questionnaire_claims["some_field"] = "123456"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(questionnaire_claims, field_specification)

    questionnaire_claims["some_field"] = "123"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(questionnaire_claims, field_specification)


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_uuid_deserialisation(version):
    metadata = get_metadata_full(version)

    validator = (
        validate_runner_claims_v2
        if version is AuthPayloadVersion.V2
        else validate_runner_claims
    )
    claims = validator(metadata)

    assert isinstance(claims["tx_id"], str)


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_unknown_claims_are_not_deserialized(version):
    metadata = get_metadata_full(version)

    validator = (
        validate_runner_claims_v2
        if version is AuthPayloadVersion.V2
        else validate_runner_claims
    )
    metadata["unknown_key"] = "some value"
    claims = validator(metadata)
    assert "unknown_key" not in claims


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_minimum_length_on_runner_metadata(version):
    metadata = get_metadata_full(version)

    validator = (
        validate_runner_claims_v2
        if version is AuthPayloadVersion.V2
        else validate_runner_claims
    )
    validator(metadata)

    metadata["collection_exercise_sid"] = ""
    with pytest.raises(ValidationError):
        validate_runner_claims(metadata)


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_deserialisation_iso_8601_dates(version):
    """Runner cannot currently handle date objects in metadata"""
    metadata = get_metadata_full(version)

    field_specification = [{"name": "birthday", "type": "date"}]

    if version is AuthPayloadVersion.V2:
        questionnaire_claims = metadata["survey_metadata"]["data"]
    else:
        questionnaire_claims = metadata

    questionnaire_claims["birthday"] = "2019-11-1"
    claims = validate_questionnaire_claims(questionnaire_claims, field_specification)

    assert isinstance(claims["birthday"], str)


@freeze_time("2021-11-15T15:34:54+00:00")
@pytest.mark.parametrize(
    "date_string, version",
    [
        ("2021-11-22T15:34:54+00:00", None),
        ("2021-11-22T15:34:54+00:00", AuthPayloadVersion.V2),
        ("2021-11-22T15:34:54Z", None),
        ("2021-11-22T15:34:54Z", AuthPayloadVersion.V2),
    ],
)
def test_deserialisation_iso_8601_date(date_string, version):
    metadata = get_metadata_full(version)

    metadata["response_expires_at"] = date_string

    validator = (
        validate_runner_claims_v2
        if version is AuthPayloadVersion.V2
        else validate_runner_claims
    )
    claims = validator(metadata)

    assert claims["response_expires_at"] == "2021-11-22T15:34:54+00:00"


@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_deserialisation_iso_8601_datetime_past_datetime_raises_ValidationError(
    version,
):
    metadata = get_metadata_full(version)

    validator = (
        validate_runner_claims_v2
        if version is AuthPayloadVersion.V2
        else validate_runner_claims
    )

    metadata["response_expires_at"] = "1900-11-22T15:34:54+00:00"
    with pytest.raises(ValidationError):
        validator(metadata)


@freeze_time("2021-11-15T15:34:54+00:00")
@pytest.mark.parametrize(
    "version",
    (
        None,
        AuthPayloadVersion.V2,
    ),
)
def test_deserialisation_iso_8601_datetime_bad_datetime_raises_ValidationError(
    version,
):
    metadata = get_metadata_full(version)

    validator = (
        validate_runner_claims_v2
        if version is AuthPayloadVersion.V2
        else validate_runner_claims
    )

    metadata["response_expires_at"] = "2021-11-22"
    with pytest.raises(ValidationError):
        validator(metadata)


def test_empty_schema_name_and_schema_url_and_cir_instrument_id_not_valid_v2():
    metadata = get_metadata_full(AuthPayloadVersion.V2)
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
    metadata = get_metadata_full(AuthPayloadVersion.V2)
    del metadata["schema_name"]

    metadata.update(options)

    with pytest.raises(ValidationError) as exc:
        validate_runner_claims_v2(metadata)

    assert (
        "Only one of schema_name, schema_url or cir_instrument_id should be specified in metadata"
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


def test_business_params_without_schema_name_v1(fake_business_metadata_runner):
    claims = validate_runner_claims(fake_business_metadata_runner)

    assert claims["schema_name"] == "mbs_0253"


def test_when_response_id_is_missing_v1(fake_business_metadata_runner):
    expected = (
        f"{fake_business_metadata_runner['ru_ref']}"
        f"{fake_business_metadata_runner['collection_exercise_sid']}"
        f"{fake_business_metadata_runner['eq_id']}"
        f"{fake_business_metadata_runner['form_type']}"
    )
    del fake_business_metadata_runner["response_id"]
    claims = validate_runner_claims(fake_business_metadata_runner)
    assert claims["response_id"] == expected


def test_when_response_id_is_present_v1(fake_business_metadata_runner):
    claims = validate_runner_claims(fake_business_metadata_runner)
    assert claims["response_id"] == fake_business_metadata_runner["response_id"]


@pytest.mark.parametrize(
    "metadata", ["eq_id", "form_type", "ru_ref", "collection_exercise_sid"]
)
def test_response_id_for_missing_metadata_v1(metadata, fake_business_metadata_runner):
    fake_business_metadata_runner["schema_name"] = "schema_name"
    del fake_business_metadata_runner["response_id"]
    del fake_business_metadata_runner[metadata]
    with pytest.raises(ValidationError):
        validate_runner_claims(fake_business_metadata_runner)


def test_response_id_for_empty_value_v1(fake_business_metadata_runner):
    expected = (
        f"{fake_business_metadata_runner['ru_ref']}"
        f"{fake_business_metadata_runner['collection_exercise_sid']}"
        f"{fake_business_metadata_runner['eq_id']}"
        f"{fake_business_metadata_runner['form_type']}"
    )
    fake_business_metadata_runner["response_id"] = ""
    claims = validate_runner_claims(fake_business_metadata_runner)
    assert claims["response_id"] == expected
