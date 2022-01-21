from copy import deepcopy

import pytest
from freezegun import freeze_time
from marshmallow import ValidationError

from app.utilities.metadata_parser import (
    validate_questionnaire_claims,
    validate_runner_claims,
)


def test_spaces_are_stripped_from_string_fields(fake_metadata_runner):
    fake_metadata_runner["collection_exercise_sid"] = "  stripped     "

    output = validate_runner_claims(fake_metadata_runner)

    assert output["collection_exercise_sid"] == "stripped"


def test_empty_strings_are_not_valid(fake_metadata_runner):
    fake_metadata_runner["schema_name"] = ""

    with pytest.raises(ValidationError):
        validate_runner_claims(fake_metadata_runner)


def test_validation_does_not_change_metadata(
    fake_metadata_full, fake_questionnaire_metadata_requirements_full
):
    fake_metadata_copy = deepcopy(fake_metadata_full)
    validate_questionnaire_claims(
        fake_metadata_full, fake_questionnaire_metadata_requirements_full
    )

    assert fake_metadata_full == fake_metadata_copy


def test_validation_no_error_when_optional_field_not_passed(fake_metadata_runner):
    field_specification = [
        {"name": "optional_field", "type": "string", "optional": True}
    ]

    validate_questionnaire_claims(fake_metadata_runner, field_specification)


def test_validation_field_required_by_default(fake_metadata_runner):
    field_specification = [{"name": "required_field", "type": "string"}]

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(fake_metadata_runner, field_specification)


def test_minimum_length(fake_metadata_runner):
    field_specification = [{"name": "some_field", "type": "string", "min_length": 5}]

    fake_metadata_runner["some_field"] = "123456"

    validate_questionnaire_claims(fake_metadata_runner, field_specification)

    fake_metadata_runner["some_field"] = "1"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(fake_metadata_runner, field_specification)


def test_maximum_length(fake_metadata_runner):
    field_specification = [{"name": "some_field", "type": "string", "max_length": 5}]

    fake_metadata_runner["some_field"] = "1234"

    validate_questionnaire_claims(fake_metadata_runner, field_specification)

    fake_metadata_runner["some_field"] = "123456"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(fake_metadata_runner, field_specification)


def test_min_and_max_length(fake_metadata_runner):
    field_specification = [
        {"name": "some_field", "type": "string", "min_length": 4, "max_length": 5}
    ]

    fake_metadata_runner["some_field"] = "1234"

    validate_questionnaire_claims(fake_metadata_runner, field_specification)

    fake_metadata_runner["some_field"] = "123456"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(fake_metadata_runner, field_specification)

    fake_metadata_runner["some_field"] = "123"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(fake_metadata_runner, field_specification)


def test_length_equals(fake_metadata_runner):
    field_specification = [{"name": "some_field", "type": "string", "length": 4}]

    fake_metadata_runner["some_field"] = "1234"

    validate_questionnaire_claims(fake_metadata_runner, field_specification)

    fake_metadata_runner["some_field"] = "123456"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(fake_metadata_runner, field_specification)

    fake_metadata_runner["some_field"] = "123"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(fake_metadata_runner, field_specification)


def test_uuid_deserialisation(fake_metadata_runner):
    claims = validate_runner_claims(fake_metadata_runner)

    assert isinstance(claims["tx_id"], str)


def test_unknown_claims_are_not_deserialized(fake_metadata_runner):
    fake_metadata_runner["unknown_key"] = "some value"
    claims = validate_runner_claims(fake_metadata_runner)
    assert "unknown_key" not in claims


def test_minimum_length_on_runner_metadata(fake_metadata_runner):
    validate_runner_claims(fake_metadata_runner)

    fake_metadata_runner["schema_name"] = ""
    with pytest.raises(ValidationError):
        validate_runner_claims(fake_metadata_runner)


def test_deserialisation_iso_8601_dates(fake_metadata_runner):
    """Runner cannot currently handle date objects in metadata"""
    field_specification = [{"name": "birthday", "type": "date"}]

    fake_metadata_runner["birthday"] = "2019-11-1"
    claims = validate_questionnaire_claims(fake_metadata_runner, field_specification)

    assert isinstance(claims["birthday"], str)


@freeze_time("2021-11-15T15:34:54+00:00")
@pytest.mark.parametrize(
    "date_string",
    ["2021-11-22T15:34:54+00:00", "2021-11-22T15:34:54Z"],
)
def test_deserialisation_iso_8601_date(date_string, fake_metadata_runner):
    fake_metadata_runner["response_expires_at"] = date_string
    claims = validate_runner_claims(fake_metadata_runner)
    assert claims["response_expires_at"] == "2021-11-22T15:34:54+00:00"


def test_deserialisation_iso_8601_datetime_past_datetime_raises_ValidationError(
    fake_metadata_runner,
):
    fake_metadata_runner["response_expires_at"] = "1900-11-22T15:34:54+00:00"
    with pytest.raises(ValidationError):
        validate_runner_claims(fake_metadata_runner)


@freeze_time("2021-11-15T15:34:54+00:00")
def test_deserialisation_iso_8601_datetime_bad_datetime_raises_ValidationError(
    fake_metadata_runner,
):
    fake_metadata_runner["response_expires_at"] = "2021-11-22"
    with pytest.raises(ValidationError):
        validate_runner_claims(fake_metadata_runner)


def test_business_params_without_schema_name(fake_business_metadata_runner):
    claims = validate_runner_claims(fake_business_metadata_runner)

    assert claims["schema_name"] == "mbs_0253"


def test_when_response_id_is_missing(fake_business_metadata_runner):
    expected = (
        f"{fake_business_metadata_runner['ru_ref']}"
        f"{fake_business_metadata_runner['collection_exercise_sid']}"
        f"{fake_business_metadata_runner['eq_id']}"
        f"{fake_business_metadata_runner['form_type']}"
    )
    del fake_business_metadata_runner["response_id"]
    claims = validate_runner_claims(fake_business_metadata_runner)
    assert claims["response_id"] == expected


def test_when_response_id_is_present(fake_business_metadata_runner):
    claims = validate_runner_claims(fake_business_metadata_runner)
    assert claims["response_id"] == fake_business_metadata_runner["response_id"]


@pytest.mark.parametrize(
    "metadata", ["eq_id", "form_type", "ru_ref", "collection_exercise_sid"]
)
def test_response_id_for_missing_metadata(metadata, fake_business_metadata_runner):
    fake_business_metadata_runner["schema_name"] = "schema_name"
    del fake_business_metadata_runner["response_id"]
    del fake_business_metadata_runner[metadata]
    with pytest.raises(ValidationError):
        validate_runner_claims(fake_business_metadata_runner)
