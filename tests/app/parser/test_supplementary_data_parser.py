from contextlib import contextmanager
from copy import deepcopy

import pytest
from marshmallow import ValidationError

from app.services.supplementary_data import validate_supplementary_data
from app.utilities.supplementary_data_parser import validate_supplementary_data_v1


@contextmanager
def not_raises(exception):
    try:
        yield
    except exception as validation_error:
        raise pytest.fail(f"{validation_error} RAISED")


SUPPLEMENTARY_DATA_PAYLOAD = {
    "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
    "survey_id": "123",
    "data": {
        "schema_version": "v1",
        "identifier": "12345678901",
        "items": {
            "local_units": [
                {
                    "identifier": 1,
                    "lu_name": "TEST NAME. 1",
                    "lu_address": [
                        "FIRST ADDRESS 1",
                        "FIRST ADDRESS 2",
                        "TOWN",
                        "COUNTY",
                        "POST CODE",
                    ],
                },
                {
                    "identifier": "0002",
                    "lu_name": "TEST NAME 2",
                    "lu_address": [
                        "SECOND ADDRESS 1",
                        "SECOND ADDRESS 1",
                        "TOWN",
                        "COUNTY",
                        "POSTCODE",
                    ],
                },
            ]
        },
    },
}


def test_invalid_supplementary_data_payload_raises_error():
    with pytest.raises(ValidationError) as error:
        validate_supplementary_data(
            supplementary_data={},
            dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
            identifier="12345678901",
            survey_id="123",
        )

    assert str(error.value) == "Invalid supplementary data"


def test_invalid_supplementary_dataset_version_raises_error():
    with pytest.raises(ValidationError) as error:
        validate_supplementary_data_v1(
            supplementary_data=SUPPLEMENTARY_DATA_PAYLOAD,
            dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
            identifier="12345678901",
            survey_id="123",
            sds_schema_version="v6",
        )

    assert (
        str(error.value)
        == "{'_schema': ['The Supplementary Dataset Schema Version does not match the version set in the Questionnaire Schema']}"
    )


def test_valid_supplementary_dataset_version_does_not_raise_error():
    with not_raises(ValidationError):
        validated_payload = validate_supplementary_data_v1(
            supplementary_data=SUPPLEMENTARY_DATA_PAYLOAD,
            dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
            identifier="12345678901",
            survey_id="123",
            sds_schema_version="v1",
        )

    assert validated_payload == SUPPLEMENTARY_DATA_PAYLOAD


def test_validate_supplementary_data_payload():
    validated_payload = validate_supplementary_data_v1(
        supplementary_data=SUPPLEMENTARY_DATA_PAYLOAD,
        dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
        identifier="12345678901",
        survey_id="123",
    )

    assert validated_payload == SUPPLEMENTARY_DATA_PAYLOAD


def test_validate_supplementary_data_payload_incorrect_dataset_id():
    with pytest.raises(ValidationError) as error:
        validate_supplementary_data_v1(
            supplementary_data=SUPPLEMENTARY_DATA_PAYLOAD,
            dataset_id="331507ca-1039-4624-a342-7cbc3630e217",
            identifier="12345678901",
            survey_id="123",
        )

    assert (
        str(error.value)
        == "{'_schema': ['Supplementary data did not return the specified Dataset ID']}"
    )


def test_validate_supplementary_data_payload_incorrect_survey_id():
    with pytest.raises(ValidationError) as error:
        validate_supplementary_data_v1(
            supplementary_data=SUPPLEMENTARY_DATA_PAYLOAD,
            dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
            identifier="12345678901",
            survey_id="234",
        )

    assert (
        str(error.value)
        == "{'_schema': ['Supplementary data did not return the specified Survey ID']}"
    )


def test_validate_supplementary_data_payload_incorrect_identifier():
    with pytest.raises(ValidationError) as error:
        validate_supplementary_data_v1(
            supplementary_data=SUPPLEMENTARY_DATA_PAYLOAD,
            dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
            identifier="000000000001",
            survey_id="123",
        )

    assert (
        str(error.value)
        == "{'data': {'_schema': ['Supplementary data did not return the specified Identifier']}}"
    )


def test_supplementary_data_payload_with_no_items_is_validated():
    payload = {
        "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
        "survey_id": "123",
        "data": {
            "schema_version": "v1",
            "identifier": "12345678901",
        },
    }

    validated_payload = validate_supplementary_data_v1(
        supplementary_data=payload,
        dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
        identifier="12345678901",
        survey_id="123",
    )

    assert validated_payload == payload


def test_validate_supplementary_data_payload_missing_survey_id():
    payload = {
        "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
        "data": {
            "schema_version": "v1",
            "identifier": "12345678901",
        },
    }

    with pytest.raises(ValidationError) as error:
        validate_supplementary_data_v1(
            supplementary_data=payload,
            dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
            identifier="12345678901",
            survey_id="123",
        )

    assert str(error.value) == "{'survey_id': ['Missing data for required field.']}"


def test_validate_supplementary_data_payload_with_unknown_field():
    payload = {
        "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
        "survey_id": "123",
        "some_field": "value",
        "data": {
            "schema_version": "v1",
            "identifier": "12345678901",
        },
    }

    validated_payload = validate_supplementary_data_v1(
        supplementary_data=payload,
        dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
        identifier="12345678901",
        survey_id="123",
    )

    assert validated_payload == payload


def test_validate_supplementary_data_payload_missing_identifier_in_items():
    payload = deepcopy(SUPPLEMENTARY_DATA_PAYLOAD)
    payload["data"]["items"]["local_units"][0].pop("identifier")

    with pytest.raises(ValidationError) as error:
        validate_supplementary_data_v1(
            supplementary_data=payload,
            dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
            identifier="12345678901",
            survey_id="123",
        )

    assert str(error.value) == "{'identifier': ['Missing data for required field.']}"


@pytest.mark.parametrize("invalid_identifier", ["", ["invalid"], -1, {}])
def test_validate_supplementary_data_payload_invalid_identifier(invalid_identifier):
    payload = deepcopy(SUPPLEMENTARY_DATA_PAYLOAD)
    payload["data"]["items"]["local_units"][0]["identifier"] = invalid_identifier

    with pytest.raises(ValidationError) as error:
        validate_supplementary_data_v1(
            supplementary_data=payload,
            dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
            identifier="12345678901",
            survey_id="123",
        )

    assert (
        str(error.value)
        == "{'identifier': ['Item identifier must be a non-empty string or non-negative integer']}"
    )
