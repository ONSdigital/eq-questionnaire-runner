import pytest
from werkzeug.datastructures import ImmutableDict

from app.authentication.auth_payload_versions import AuthPayloadVersion
from app.data_models.metadata_proxy import MetadataProxy, SurveyMetadata

METADATA_V1 = {
    "schema_name": "1_0000",
    "ru_ref": "12345678901A",
    "response_id": "1",
    "account_service_url": "account_service_url",
    "tx_id": "tx_id",
    "collection_exercise_sid": "collection_exercise_sid",
    "case_id": "case_id",
    "response_expires_at": "2023-04-24T10:46:32+00:00",
}

METADATA_V2 = {
    "version": AuthPayloadVersion.V2.value,
    "schema_name": "1_0000",
    "response_id": "1",
    "account_service_url": "account_service_url",
    "tx_id": "tx_id",
    "collection_exercise_sid": "collection_exercise_sid",
    "case_id": "case_id",
    "response_expires_at": "2023-04-24T10:46:32+00:00",
    "survey_metadata": {
        "data": {
            "ru_ref": "12345678901A",
        },
    },
}


@pytest.mark.parametrize(
    "resolved_metadata_proxy_value, metadata_var",
    (
        (MetadataProxy.from_dict(METADATA_V1)["ru_ref"], METADATA_V1["ru_ref"]),
        (
            MetadataProxy.from_dict(METADATA_V2)["ru_ref"],
            METADATA_V2["survey_metadata"]["data"]["ru_ref"],
        ),
        (
            MetadataProxy.from_dict(METADATA_V1)["schema_name"],
            METADATA_V1["schema_name"],
        ),
        (
            MetadataProxy.from_dict(METADATA_V2)["schema_name"],
            METADATA_V2["schema_name"],
        ),
        (
            MetadataProxy.from_dict(METADATA_V2)["response_expires_at"],
            METADATA_V2["response_expires_at"],
        ),
        (MetadataProxy.from_dict(METADATA_V1)["non_existing"], None),
        (MetadataProxy.from_dict(METADATA_V2)["non_existing"], None),
    ),
)
def test_metadata_proxy_returns_value_for_valid_key(
    resolved_metadata_proxy_value, metadata_var
):
    assert resolved_metadata_proxy_value == metadata_var


def test_survey_metadata_returns_valid_key():
    expected_values = {"key": "value"}
    data = ImmutableDict(expected_values)

    survey_metadata = SurveyMetadata(data=data)

    assert survey_metadata["key"] == expected_values["key"]
