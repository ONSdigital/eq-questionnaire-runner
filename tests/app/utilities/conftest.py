import pytest

from app.data_models.metadata_proxy import MetadataProxy


@pytest.fixture
def metadata_with_cir_instrument_id():
    return MetadataProxy.from_dict(
        {
            "cir_instrument_id": "f0519981-426c-8b93-75c0-bfc40c66fe25",
            "language_code": "cy",
        },
    )
