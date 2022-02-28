import contextlib
from datetime import datetime, timedelta, timezone

import boto3
import fakeredis
from flask import current_app
from moto import mock_dynamodb2
import pytest

from app.storage.redis import Redis
from app.storage.dynamodb import Dynamodb
from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage
from app.storage.storage import StorageModel

from app.data_models.app_models import EQSession

NOW = datetime.now(tz=timezone.utc).replace(microsecond=0)


@pytest.fixture
def fake_eq_session():
    eq_session = EQSession(
        eq_session_id="sessionid",
        user_id="someuser",
        session_data="somedata",
        expires_at=NOW + timedelta(minutes=1),
    )

    return eq_session


@pytest.fixture
def ddb():
    with mock_dynamodb2() as mock_dynamo:
        mock_dynamo.start()
        boto3_client = boto3.resource("dynamodb", endpoint_url=None)
        for config in StorageModel.TABLE_CONFIG_BY_TYPE.values():
            table_name = current_app.config[config["table_name_key"]]
            if table_name:
                boto3_client.create_table(  # pylint: disable=no-member
                    TableName=table_name,
                    AttributeDefinitions=[
                        {"AttributeName": config["key_field"], "AttributeType": "S"}
                    ],
                    KeySchema=[
                        {"AttributeName": config["key_field"], "KeyType": "HASH"}
                    ],
                    ProvisionedThroughput={
                        "ReadCapacityUnits": 1,
                        "WriteCapacityUnits": 1,
                    },
                )
        yield Dynamodb(boto3_client)
        mock_dynamo.stop()


@pytest.fixture
def client(mocker):
    mock_client = mocker.Mock()
    mock_client.transaction.return_value = contextlib.suppress()
    return mock_client


@pytest.fixture
def encrypted_storage():
    return EncryptedQuestionnaireStorage("user_id", "user_ik", "pepper")


@pytest.fixture
def redis_client():
    return fakeredis.FakeStrictRedis()


@pytest.fixture
def redis(redis_client):
    return Redis(redis_client)
