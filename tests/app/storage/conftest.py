import contextlib
from datetime import datetime, timedelta, timezone

import boto3
import fakeredis
import pytest
from flask import current_app
from moto import mock_aws

from app.data_models.app_models import EQSession, QuestionnaireState
from app.storage.dynamodb import Dynamodb
from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage
from app.storage.redis import Redis
from app.storage.storage import StorageModel


@pytest.fixture
def dynamodb():
    with mock_aws() as mocked_aws_environment:
        mocked_aws_environment.start()
        boto3_client = boto3.resource("dynamodb", endpoint_url=None)
        for config in StorageModel.TABLE_CONFIG_BY_TYPE.values():
            table_name = current_app.config[config["table_name_key"]]
            if table_name:
                boto3_client.create_table(
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
        mocked_aws_environment.stop()


@pytest.fixture
def mock_client(mocker):
    client = mocker.Mock()
    client.transaction.return_value = contextlib.suppress()
    return client


@pytest.fixture
def encrypted_storage():
    return EncryptedQuestionnaireStorage("user_id", "user_ik", "pepper")


@pytest.fixture(name="redis_client")
def mock_redis_client():
    return fakeredis.FakeStrictRedis()


@pytest.fixture
def redis(redis_client):
    return Redis(redis_client)


@pytest.fixture
def questionnaire_state():
    return QuestionnaireState("someuser", "data", "ce_sid", 1)


@pytest.fixture
def eq_session():
    return EQSession(
        eq_session_id="sessionid",
        user_id="someuser",
        session_data="somedata",
        expires_at=datetime.now(tz=timezone.utc).replace(microsecond=0)
        + timedelta(minutes=1),
    )
