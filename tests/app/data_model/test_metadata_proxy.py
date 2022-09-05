import pytest

from app.data_models.metadata_proxy import MetadataProxy

METADATA_V1 = {
    "schema_name": "1_0000",
    "ru_ref": "432423423423",
    "response_id": "1",
    "account_service_url": "account_service_url",
    "tx_id": "tx_id",
    "collection_exercise_sid": "collection_exercise_sid",
    "case_id": "case_id",
}

METADATA_V2 = {
    "version": "v2",
    "schema_name": "1_0000",
    "response_id": "1",
    "account_service_url": "account_service_url",
    "tx_id": "tx_id",
    "collection_exercise_sid": "collection_exercise_sid",
    "case_id": "case_id",
    "survey_metadata": {
        "data": {
            "ru_ref": "432423423423",
        },
    },
}


@pytest.mark.parametrize(
    "resolved_metadata_proxy_value, metadata_var",
    (
        (MetadataProxy.from_dict(dict(METADATA_V1))["ru_ref"], METADATA_V1["ru_ref"]),
        (
            MetadataProxy.from_dict(dict(METADATA_V2))["ru_ref"],
            METADATA_V2["survey_metadata"]["data"]["ru_ref"],
        ),
        (
            MetadataProxy.from_dict(dict(METADATA_V1))["schema_name"],
            METADATA_V1["schema_name"],
        ),
        (
            MetadataProxy.from_dict(dict(METADATA_V2))["schema_name"],
            METADATA_V2["schema_name"],
        ),
        (MetadataProxy.from_dict(dict(METADATA_V1))["non_existing"], None),
        (MetadataProxy.from_dict(dict(METADATA_V2))["non_existing"], None),
    ),
)
def test_metadata_proxy_returns_value_for_valid_key(
    resolved_metadata_proxy_value, metadata_var
):
    assert resolved_metadata_proxy_value == metadata_var
