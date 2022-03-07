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
def test_get_by_key(datastore, client, questionnaire_state):
    model_data = QuestionnaireStateSchema().dump(questionnaire_state)

    m_entity = google_datastore.Entity()
    m_entity.update(model_data)
    client.get.return_value = m_entity

    returned_model = datastore.get(QuestionnaireState, "someuser")

    assert questionnaire_state.user_id == returned_model.user_id
    assert questionnaire_state.state_data == returned_model.state_data
    assert questionnaire_state.version == returned_model.version
    assert (
        questionnaire_state.collection_exercise_sid
        == returned_model.collection_exercise_sid
    )
    assert questionnaire_state.submitted_at == returned_model.submitted_at


@pytest.mark.usefixtures("app")
def test_get_not_found(datastore, client):
    client.get.return_value = None
    returned_model = datastore.get(QuestionnaireState, "someuser")
    assert not returned_model


@pytest.mark.usefixtures("app")
def test_put(datastore, client, questionnaire_state):

    datastore.put(questionnaire_state, True)

    put_data = client.put.call_args[0][0]

    assert questionnaire_state.user_id == put_data["user_id"]
    assert questionnaire_state.state_data == put_data["state_data"]
    assert questionnaire_state.version == put_data["version"]
    assert (
        questionnaire_state.collection_exercise_sid
        == put_data["collection_exercise_sid"]
    )
    assert questionnaire_state.submitted_at == put_data["submitted_at"]


@pytest.mark.usefixtures("app")
def test_put_without_overwrite(datastore, questionnaire_state):

    with pytest.raises(NotImplementedError) as exc:
        datastore.put(questionnaire_state, False)

    assert exc.value.args[0] == "Unique key checking not supported"


@pytest.mark.usefixtures("app")
def test_put_exclude_indexes(datastore, mocker, questionnaire_state):
    mock_entity = mocker.patch("app.storage.datastore.Entity")

    datastore.put(questionnaire_state)
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
def test_delete(datastore, client, questionnaire_state):
    datastore.delete(questionnaire_state)

    assert client.key.call_args[0][1] == questionnaire_state.user_id

    m_key = client.key.return_value

    client.delete.assert_called_once_with(m_key)


@pytest.mark.usefixtures("app")
def test_retry(datastore, client, mocker, questionnaire_state):

    client.put = mocker.Mock(
        side_effect=[exceptions.InternalServerError("error"), mocker.DEFAULT]
    )
    datastore.put(questionnaire_state, True)
    assert client.put.call_count > 1
