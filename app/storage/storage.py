from abc import ABC, abstractmethod
from functools import cached_property

from flask import current_app

from app.data_models import app_models


class StorageModel:
    TABLE_CONFIG = {
        app_models.QuestionnaireState: {
            "key_field": "user_id",
            "table_name_key": "EQ_QUESTIONNAIRE_STATE_TABLE_NAME",
            "schema": app_models.QuestionnaireStateSchema,
        },
        app_models.EQSession: {
            "key_field": "eq_session_id",
            "expiry_field": "expires_at",
            "index_fields": ["expires_at"],
            "table_name_key": "EQ_SESSION_TABLE_NAME",
            "schema": app_models.EQSessionSchema,
        },
        app_models.UsedJtiClaim: {
            "key_field": "jti_claim",
            "expiry_field": "expires_at",
            "table_name_key": "EQ_USED_JTI_CLAIM_TABLE_NAME",
            "schema": app_models.UsedJtiClaimSchema,
        },
    }

    def __init__(self, model_type):
        self._model_type = model_type

        if self._model_type not in self.TABLE_CONFIG:
            raise KeyError("Invalid model_type provided")

        self._config = self.TABLE_CONFIG[self._model_type]
        self._schema = self._config["schema"]()

    @cached_property
    def key_field(self):
        return self._config["key_field"]

    @cached_property
    def expiry_field(self):
        return self._config.get("expiry_field")

    @cached_property
    def index_fields(self):
        return self._config.get("index_fields", [])

    @cached_property
    def table_name(self):
        return current_app.config[self._config["table_name_key"]]

    def serialize(self, model_to_serialize):
        return self._schema.dump(model_to_serialize)

    def deserialize(self, serialized_item):
        return self._schema.load(serialized_item)


class StorageHandler(ABC):
    def __init__(self, client):
        self.client = client

    @abstractmethod
    def put(self, model, overwrite=True):
        pass  # pragma: no cover

    @abstractmethod
    def get(self, model_type, key_value):
        pass  # pragma: no cover

    @abstractmethod
    def delete(self, model):
        pass  # pragma: no cover
