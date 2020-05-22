import json
from datetime import datetime

import pytest
from dateutil.tz import tzutc

from app.data_model.app_models import EQSession, EQSessionSchema
from app.storage.storage import StorageModel

NOW = datetime.now(tz=tzutc()).replace(microsecond=0)


def test_model_or_model_type_not_provided():

    with pytest.raises(ValueError) as ex:
        StorageModel()

    assert "One of model/model_type is required" in str(ex)


def test_non_existent_model_type():
    with pytest.raises(KeyError) as ex:
        StorageModel(model_type=int)

    assert "Invalid model_type provided" in str(ex)


def test_storage_model_properties(app):  # pylint: disable=unused-argument
    eq_session = EQSession(
        eq_session_id="sessionid",
        user_id="someuser",
        session_data="somedata",
        expires_at=NOW,
    )

    storage_model = StorageModel(model=eq_session)

    assert isinstance(storage_model.schema, EQSessionSchema)
    assert storage_model.key_field == "eq_session_id"
    assert storage_model.key_value == "sessionid"
    assert storage_model.table_name == "dev-eq-session"

    expected_schema = EQSessionSchema().dump(eq_session)

    assert storage_model.item["eq_session_id"] == expected_schema["eq_session_id"]
    assert storage_model.item["user_id"] == expected_schema["user_id"]
    assert storage_model.item["session_data"] == expected_schema["session_data"]
    assert storage_model.item["created_at"] == expected_schema["created_at"]
    assert storage_model.item["expires_at"] == expected_schema["expires_at"]
    assert storage_model.item["updated_at"] >= expected_schema["updated_at"]
