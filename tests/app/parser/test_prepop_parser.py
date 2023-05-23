import pytest
from marshmallow import ValidationError

from app.routes.session import validate_prepop_data
from app.utilities.prepop_parser import validate_prepop_data_v1

PREPOP_PAYLOAD = {
    "dataset_id": "001",
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


def test_invalid_prepop_data_payload_raises_error():
    with pytest.raises(ValidationError):
        validate_prepop_data(prepop_data={}, dataset_id="001", ru_ref="12346789012A")


def test_validate_prepop_payload():
    validated_payload = validate_prepop_data_v1(
        prepop_data=PREPOP_PAYLOAD, dataset_id="001", ru_ref="12346789012A"
    )

    assert validated_payload == PREPOP_PAYLOAD


def test_validate_prepop_payload_incorrect_dataset_id():
    with pytest.raises(ValidationError):
        validate_prepop_data_v1(
            prepop_data=PREPOP_PAYLOAD, dataset_id="002", ru_ref="12346789012A"
        )


def test_validate_prepop_payload_incorrect_ru_ref():
    with pytest.raises(ValidationError):
        validate_prepop_data_v1(
            prepop_data=PREPOP_PAYLOAD, dataset_id="001", ru_ref="000000000001"
        )


def test_prepop_payload_with_no_items_is_validated():
    payload = {
        "dataset_id": "001",
        "survey_id": "123",
        "data": {
            "schema_version": "v1",
            "identifier": "12346789012A",
        },
    }

    validated_payload = validate_prepop_data_v1(
        prepop_data=payload, dataset_id="001", ru_ref="12346789012A"
    )

    assert validated_payload == payload


def test_validate_prepop_payload_missing_survey_id():
    payload = {
        "dataset_id": "001",
        "data": {
            "schema_version": "v1",
            "identifier": "12346789012A",
        },
    }

    with pytest.raises(ValidationError):
        validate_prepop_data_v1(
            prepop_data=payload, dataset_id="001", ru_ref="12346789012A"
        )


def test_validate_prepop_payload_with_unknown_field():
    payload = {
        "dataset_id": "001",
        "survey_id": "123",
        "some_field": "value",
        "data": {
            "schema_version": "v1",
            "identifier": "12346789012A",
        },
    }

    validated_payload = validate_prepop_data_v1(
        prepop_data=payload, dataset_id="001", ru_ref="12346789012A"
    )

    assert validated_payload == payload


def test_validate_prepop_invalid_schema_version():
    payload = {
        "dataset_id": "001",
        "survey_id": "123",
        "some_field": "value",
        "data": {
            "schema_version": "v2",
            "identifier": "12346789012A",
        },
    }

    with pytest.raises(ValidationError):
        validate_prepop_data_v1(
            prepop_data=payload, dataset_id="001", ru_ref="12346789012A"
        )


def test_validate_prepop_payload_missing_identifier_in_items():
    payload = {
        "dataset_id": "001",
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
        validate_prepop_data_v1(
            prepop_data=payload, dataset_id="001", ru_ref="12346789012A"
        )
