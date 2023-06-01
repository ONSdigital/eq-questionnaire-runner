import pytest
from marshmallow import ValidationError

from app.services.supplementary_data import validate_supplementary_data
from app.utilities.supplementary_data_parser import validate_supplementary_data_v1

SUPPLEMENTARY_DATA_PAYLOAD = {
    "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
    "survey_id": "123",
    "data": {
        "schema_version": "v1",
        "identifier": "12346789012A",
        "items": {
            "local_units": [
                {
                    "identifier": "0001",
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
    with pytest.raises(ValidationError):
        validate_supplementary_data(
            supplementary_data={},
            dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
            unit_id="12346789012A",
            survey_id="123",
        )


def test_validate_supplementary_data_payload():
    validated_payload = validate_supplementary_data_v1(
        supplementary_data=SUPPLEMENTARY_DATA_PAYLOAD,
        dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
        unit_id="12346789012A",
        survey_id="123",
    )

    assert validated_payload == SUPPLEMENTARY_DATA_PAYLOAD


def test_validate_supplementary_data_payload_incorrect_dataset_id():
    with pytest.raises(ValidationError):
        validate_supplementary_data_v1(
            supplementary_data=SUPPLEMENTARY_DATA_PAYLOAD,
            dataset_id="331507ca-1039-4624-a342-7cbc3630e217",
            unit_id="12346789012A",
            survey_id="123",
        )


def test_validate_supplementary_data_payload_incorrect_survey_id():
    with pytest.raises(ValidationError):
        validate_supplementary_data_v1(
            supplementary_data=SUPPLEMENTARY_DATA_PAYLOAD,
            dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
            unit_id="12346789012A",
            survey_id="234",
        )


def test_validate_supplementary_data_payload_incorrect_unit_id():
    with pytest.raises(ValidationError):
        validate_supplementary_data_v1(
            supplementary_data=SUPPLEMENTARY_DATA_PAYLOAD,
            dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
            unit_id="000000000001",
            survey_id="123",
        )


def test_supplementary_data_payload_with_no_items_is_validated():
    payload = {
        "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
        "survey_id": "123",
        "data": {
            "schema_version": "v1",
            "identifier": "12346789012A",
        },
    }

    validated_payload = validate_supplementary_data_v1(
        supplementary_data=payload,
        dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
        unit_id="12346789012A",
        survey_id="123",
    )

    assert validated_payload == payload


def test_validate_supplementary_data_payload_missing_survey_id():
    payload = {
        "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
        "data": {
            "schema_version": "v1",
            "identifier": "12346789012A",
        },
    }

    with pytest.raises(ValidationError):
        validate_supplementary_data_v1(
            supplementary_data=payload,
            dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
            unit_id="12346789012A",
            survey_id="123",
        )


def test_validate_supplementary_data_payload_with_unknown_field():
    payload = {
        "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
        "survey_id": "123",
        "some_field": "value",
        "data": {
            "schema_version": "v1",
            "identifier": "12346789012A",
        },
    }

    validated_payload = validate_supplementary_data_v1(
        supplementary_data=payload,
        dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
        unit_id="12346789012A",
        survey_id="123",
    )

    assert validated_payload == payload


def test_validate_supplementary_data_invalid_schema_version():
    payload = {
        "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
        "survey_id": "123",
        "some_field": "value",
        "data": {
            "schema_version": "v2",
            "identifier": "12346789012A",
        },
    }

    with pytest.raises(ValidationError):
        validate_supplementary_data_v1(
            supplementary_data=payload,
            dataset_id="001",
            unit_id="12346789012A",
            survey_id="123",
        )


def test_validate_supplementary_data_payload_missing_identifier_in_items():
    payload = {
        "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
        "survey_id": "123",
        "data": {
            "schema_version": "v1",
            "identifier": "12346789012A",
            "items": {
                "local_units": [
                    {
                        "identifier": "0001",
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

    with pytest.raises(ValidationError):
        validate_supplementary_data_v1(
            supplementary_data=payload,
            dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
            unit_id="12346789012A",
            survey_id="123",
        )
