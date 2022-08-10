from copy import deepcopy

import pytest
from freezegun import freeze_time
from marshmallow import ValidationError

from app.utilities.metadata_parser_v2 import (
    validate_questionnaire_claims_v2,
    validate_runner_claims_v2,
)


def test_spaces_are_stripped_from_string_fields(fake_metadata_runner_v2):
    fake_metadata_runner_v2["collection_exercise_sid"] = "  stripped     "

    output = validate_runner_claims_v2(fake_metadata_runner_v2)

    assert output["collection_exercise_sid"] == "stripped"


def test_empty_strings_are_not_valid(fake_metadata_runner_v2):
    fake_metadata_runner_v2["collection_exercise_sid"] = ""

    with pytest.raises(ValidationError):
        validate_runner_claims_v2(fake_metadata_runner_v2)


def test_validation_does_not_change_metadata(
    fake_metadata_full_v2_business, fake_questionnaire_metadata_requirements_full
):
    fake_metadata_copy = deepcopy(fake_metadata_full_v2_business)
    validate_questionnaire_claims_v2(
        fake_metadata_full_v2_business, fake_questionnaire_metadata_requirements_full
    )

    assert fake_metadata_full_v2_business == fake_metadata_copy


def test_validation_no_error_when_optional_field_not_passed(fake_metadata_runner_v2):
    field_specification = [
        {"name": "optional_field", "type": "string", "optional": True}
    ]

    validate_questionnaire_claims_v2(fake_metadata_runner_v2, field_specification)


def test_validation_field_required_by_default(fake_metadata_runner_v2):
    field_specification = [{"name": "required_field", "type": "string"}]

    with pytest.raises(ValidationError):
        validate_questionnaire_claims_v2(fake_metadata_runner_v2, field_specification)


def test_minimum_length(fake_metadata_runner_v2):
    field_specification = [{"name": "some_field", "type": "string", "min_length": 5}]

    fake_metadata_runner_v2["survey_metadata"]["data"]["some_field"] = "123456"

    validate_questionnaire_claims_v2(fake_metadata_runner_v2, field_specification)

    fake_metadata_runner_v2["survey_metadata"]["data"]["some_field"] = "1"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims_v2(fake_metadata_runner_v2, field_specification)


def test_maximum_length(fake_metadata_runner_v2):
    field_specification = [{"name": "some_field", "type": "string", "max_length": 5}]

    fake_metadata_runner_v2["survey_metadata"]["data"]["some_field"] = "1234"

    validate_questionnaire_claims_v2(fake_metadata_runner_v2, field_specification)

    fake_metadata_runner_v2["survey_metadata"]["data"]["some_field"] = "123456"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims_v2(fake_metadata_runner_v2, field_specification)


def test_min_and_max_length(fake_metadata_runner_v2):
    field_specification = [
        {"name": "some_field", "type": "string", "min_length": 4, "max_length": 5}
    ]

    fake_metadata_runner_v2["survey_metadata"]["data"]["some_field"] = "1234"

    validate_questionnaire_claims_v2(fake_metadata_runner_v2, field_specification)

    fake_metadata_runner_v2["survey_metadata"]["data"]["some_field"] = "123456"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims_v2(fake_metadata_runner_v2, field_specification)

    fake_metadata_runner_v2["survey_metadata"]["data"]["some_field"] = "123"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims_v2(fake_metadata_runner_v2, field_specification)


def test_length_equals(fake_metadata_runner_v2):
    field_specification = [{"name": "some_field", "type": "string", "length": 4}]

    fake_metadata_runner_v2["survey_metadata"]["data"]["some_field"] = "1234"

    validate_questionnaire_claims_v2(fake_metadata_runner_v2, field_specification)

    fake_metadata_runner_v2["survey_metadata"]["data"]["some_field"] = "123456"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims_v2(fake_metadata_runner_v2, field_specification)

    fake_metadata_runner_v2["survey_metadata"]["data"]["some_field"] = "123"

    with pytest.raises(ValidationError):
        validate_questionnaire_claims_v2(fake_metadata_runner_v2, field_specification)


def test_uuid_deserialisation(fake_metadata_runner_v2):
    claims = validate_runner_claims_v2(fake_metadata_runner_v2)

    assert isinstance(claims["tx_id"], str)


def test_unknown_claims_are_not_deserialized(fake_metadata_runner_v2):
    fake_metadata_runner_v2["unknown_key"] = "some value"
    claims = validate_runner_claims_v2(fake_metadata_runner_v2)
    assert "unknown_key" not in claims


def test_minimum_length_on_runner_metadata(fake_metadata_runner_v2):
    validate_runner_claims_v2(fake_metadata_runner_v2)

    fake_metadata_runner_v2["collection_exercise_sid"] = ""
    with pytest.raises(ValidationError):
        validate_runner_claims_v2(fake_metadata_runner_v2)


def test_deserialisation_iso_8601_dates(fake_metadata_runner_v2):
    """Runner cannot currently handle date objects in metadata"""
    field_specification = [{"name": "birthday", "type": "date"}]

    fake_metadata_runner_v2["survey_metadata"]["data"]["birthday"] = "2019-11-1"
    claims = validate_questionnaire_claims_v2(
        fake_metadata_runner_v2, field_specification
    )

    assert isinstance(claims["birthday"], str)


@freeze_time("2021-11-15T15:34:54+00:00")
@pytest.mark.parametrize(
    "date_string",
    ["2021-11-22T15:34:54+00:00", "2021-11-22T15:34:54Z"],
)
def test_deserialisation_iso_8601_date(date_string, fake_metadata_runner_v2):
    fake_metadata_runner_v2["response_expires_at"] = date_string
    claims = validate_runner_claims_v2(fake_metadata_runner_v2)
    assert claims["response_expires_at"] == "2021-11-22T15:34:54+00:00"


def test_deserialisation_iso_8601_datetime_past_datetime_raises_ValidationError(
    fake_metadata_runner_v2,
):
    fake_metadata_runner_v2["response_expires_at"] = "1900-11-22T15:34:54+00:00"
    with pytest.raises(ValidationError):
        validate_runner_claims_v2(fake_metadata_runner_v2)


@freeze_time("2021-11-15T15:34:54+00:00")
def test_deserialisation_iso_8601_datetime_bad_datetime_raises_ValidationError(
    fake_metadata_runner_v2,
):
    fake_metadata_runner_v2["response_expires_at"] = "2021-11-22"
    with pytest.raises(ValidationError):
        validate_runner_claims_v2(fake_metadata_runner_v2)
