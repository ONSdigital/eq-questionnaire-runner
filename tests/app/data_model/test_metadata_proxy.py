import pytest

from app.data_models.metadata_proxy import MetadataProxy

METADATA_V1 = {
    "schema_name": "1_0000",
    "ru_ref": "432423423423",
}

METADATA_V2 = {
    "version": "v2",
    "schema_name": "1_0000",
    "survey_metadata": {
        "data": {
            "ru_ref": "432423423423",
        },
    },
}


@pytest.mark.parametrize(
    "resolved_metadata_proxy_value, metadata_var",
    (
        (MetadataProxy(METADATA_V1).ru_ref, METADATA_V1["ru_ref"]),
        (
            MetadataProxy(METADATA_V2).ru_ref,
            METADATA_V2["survey_metadata"]["data"]["ru_ref"],
        ),
        (MetadataProxy(METADATA_V1).schema_name, METADATA_V1["schema_name"]),
        (MetadataProxy(METADATA_V2).schema_name, METADATA_V2["schema_name"]),
        (MetadataProxy(METADATA_V1).tx_id, None),
        (MetadataProxy(METADATA_V2).tx_id, None),
    ),
)
def test_metadata_proxy_returns_value_for_valid_key(
    resolved_metadata_proxy_value, metadata_var
):
    assert resolved_metadata_proxy_value == metadata_var
