from __future__ import annotations

from abc import ABC, abstractmethod
from functools import cached_property
from typing import Any, TypedDict

from flask import current_app
from google.cloud import datastore

from app.data_models import app_models

ModelSchemaTypes = (
    app_models.QuestionnaireStateSchema
    | app_models.EQSessionSchema
    | app_models.UsedJtiClaimSchema
)

ModelTypes = (
    app_models.QuestionnaireState | app_models.EQSession | app_models.UsedJtiClaim
)


class TableConfig(TypedDict, total=False):
    key_field: str
    table_name_key: str
    schema: type[ModelSchemaTypes]
    expiry_field: str
    index_fields: list[str]


class StorageModel:
    TABLE_CONFIG_BY_TYPE: dict[type[ModelTypes], TableConfig] = {
        app_models.QuestionnaireState: {
            "key_field": "user_id",
            "table_name_key": "EQ_QUESTIONNAIRE_STATE_TABLE_NAME",
            "schema": app_models.QuestionnaireStateSchema,
            "index_fields": ["collection_exercise_sid", "submitted_at", "expires_at"],
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

    def __init__(self, model_type: type[ModelTypes]) -> None:
        self._model_type = model_type

        if self._model_type not in self.TABLE_CONFIG_BY_TYPE:
            raise KeyError("Invalid model_type provided")

        self._config = self.TABLE_CONFIG_BY_TYPE[self._model_type]
        self._schema = self._config["schema"]()

    @cached_property
    def key_field(self) -> str:
        return self._config["key_field"]

    @cached_property
    def expiry_field(self) -> str | None:
        return self._config.get("expiry_field")

    @cached_property
    def index_fields(self) -> list[str]:
        return self._config.get("index_fields", [])

    @cached_property
    def table_name(self) -> str:
        table: str = current_app.config[self._config["table_name_key"]]
        return table

    def serialize(self, model_to_serialize: ModelTypes) -> dict:
        serialized_data: dict = self._schema.dump(model_to_serialize)
        return serialized_data

    def deserialize(self, serialized_item: datastore.Entity) -> ModelTypes:
        deserialized_data: ModelTypes = self._schema.load(serialized_item)
        return deserialized_data


class StorageHandler(ABC):
    def __init__(self, client: Any):
        self.client = client

    @abstractmethod
    def put(self, model: ModelTypes, overwrite: bool = True) -> bool:
        pass  # pragma: no cover

    @abstractmethod
    def get(self, model_type: type[ModelTypes], key_value: str) -> ModelTypes | None:
        pass  # pragma: no cover

    @abstractmethod
    def delete(self, model: ModelTypes) -> None:
        pass  # pragma: no cover
