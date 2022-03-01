from datetime import datetime, timezone

import pytest
from google.api_core import exceptions
from google.cloud import datastore as google_datastore

from app.data_models.app_models import (
    EQSession,
    QuestionnaireState,
    QuestionnaireStateSchema,
)


@pytest.mark.usefixtures("app")
def test_get_by_key(datastore, client):
    model = QuestionnaireState("someuser", "data", "ce_sid", 1)
    model_data = QuestionnaireStateSchema().dump(model)

    m_entity = google_datastore.Entity()
    m_entity.update(model_data)
    client.get.return_value = m_entity

    returned_model = datastore.get(QuestionnaireState, "someuser")

    assert model.user_id == returned_model.user_id
    assert model.state_data == returned_model.state_data
    assert model.version == returned_model.version
    assert model.collection_exercise_sid == returned_model.collection_exercise_sid
    assert model.submitted_at == returned_model.submitted_at


@pytest.mark.usefixtures("app")
def test_get_not_found(datastore, client):
    client.get.return_value = None
    returned_model = datastore.get(QuestionnaireState, "someuser")
    assert not returned_model


@pytest.mark.usefixtures("app")
def test_put(datastore, client):
    model = QuestionnaireState("someuser", "data", "ce_sid", 1)

    datastore.put(model, True)

    put_data = client.put.call_args[0][0]

    assert model.user_id == put_data["user_id"]
    assert model.state_data == put_data["state_data"]
    assert model.version == put_data["version"]
    assert model.collection_exercise_sid == put_data["collection_exercise_sid"]
    assert model.submitted_at == put_data["submitted_at"]


@pytest.mark.usefixtures("app")
def test_put_without_overwrite(datastore):
    model = QuestionnaireState("someuser", "data", "ce_sid", 1)

    with pytest.raises(NotImplementedError) as exc:
        datastore.put(model, False)

    assert exc.value.args[0] == "Unique key checking not supported"


@pytest.mark.usefixtures("app")
def test_put_exclude_indexes(datastore, mocker):
    mock_entity = mocker.patch("app.storage.datastore.Entity")

    model = QuestionnaireState("someuser", "data", "ce_sid", 1)
    datastore.put(model)
    put_call_args = mock_entity.call_args.kwargs
    assert "exclude_from_indexes" in put_call_args
    assert len(put_call_args["exclude_from_indexes"]) == 5


@pytest.mark.usefixtures("app")
def test_put_with_index(datastore, mocker):
    mock_entity = mocker.patch("app.storage.datastore.Entity")
    model = EQSession(
        "session-id", "user-id", datetime.now(tz=timezone.utc), "session-data"
    )
    datastore.put(model)
    assert "expires_at" not in mock_entity.call_args.kwargs["exclude_from_indexes"]


@pytest.mark.usefixtures("app")
def test_delete(datastore, client):
    model = QuestionnaireState("someuser", "data", "ce_sid", 1)
    datastore.delete(model)

    assert client.key.call_args[0][1] == model.user_id

    m_key = client.key.return_value

    client.delete.assert_called_once_with(m_key)


@pytest.mark.usefixtures("app")
def test_retry(datastore, client, mocker):
    model = QuestionnaireState("someuser", "data", "ce_sid", 1)

    client.put = mocker.Mock(
        side_effect=[exceptions.InternalServerError("error"), mocker.DEFAULT]
    )
    datastore.put(model, True)
    assert client.put.call_count > 1
