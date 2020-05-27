import pytest

from app.data_model.app_models import EQSessionSchema
from app.storage.storage import StorageModel


def test_non_existent_model_type():
    with pytest.raises(KeyError) as ex:
        StorageModel(model_type=int)

    assert "Invalid model_type provided" in str(ex)


def test_storage_model_properties(
    app, fake_eq_session
):  # pylint: disable=unused-argument
    storage_model = StorageModel(
        model=fake_eq_session, model_type=type(fake_eq_session)
    )

    assert storage_model.key_field == "eq_session_id"
    assert storage_model.key_value == "sessionid"
    assert storage_model.expiry_field == "expires_at"
    assert storage_model.table_name == "dev-eq-session"
    assert storage_model.expires_in.total_seconds() > 0


def test_serialise(fake_eq_session):
    expected_schema = EQSessionSchema().dump(fake_eq_session)

    storage_model = StorageModel(
        model=fake_eq_session, model_type=type(fake_eq_session)
    )
    serialised_item = storage_model.serialise()

    assert serialised_item["eq_session_id"] == expected_schema["eq_session_id"]
    assert serialised_item["user_id"] == expected_schema["user_id"]
    assert serialised_item["session_data"] == expected_schema["session_data"]
    assert serialised_item["created_at"] == expected_schema["created_at"]
    assert serialised_item["expires_at"] == expected_schema["expires_at"]
    assert serialised_item["updated_at"] >= expected_schema["updated_at"]


def test_deserialise(fake_eq_session):
    storage_model = StorageModel(
        model=fake_eq_session, model_type=type(fake_eq_session)
    )
    serialised_item = storage_model.serialise()

    assert (
        storage_model.deserialise(serialised_item).__dict__
        == EQSessionSchema().load(serialised_item).__dict__
    )
