import json
from abc import abstractmethod, ABC
from functools import cached_property

from flask import current_app

from app.data_model import app_models
from app.data_model.app_models import UsedJtiClaim, EQSession


class StorageModel:
    TABLE_CONFIG = {
        app_models.SubmittedResponse: {
            "key_field": "tx_id",
            "table_name_key": "EQ_SUBMITTED_RESPONSES_TABLE_NAME",
            "schema": app_models.SubmittedResponseSchema,
        },
        app_models.QuestionnaireState: {
            "key_field": "user_id",
            "table_name_key": "EQ_QUESTIONNAIRE_STATE_TABLE_NAME",
            "schema": app_models.QuestionnaireStateSchema,
        },
        app_models.EQSession: {
            "key_field": "eq_session_id",
            "table_name_key": "EQ_SESSION_TABLE_NAME",
            "schema": app_models.EQSessionSchema,
        },
        app_models.UsedJtiClaim: {
            "key_field": "jti_claim",
            "table_name_key": "EQ_USED_JTI_CLAIM_TABLE_NAME",
            "schema": app_models.UsedJtiClaimSchema,
        },
    }

    def __init__(self, model=None, model_type=None):
        self._model = model
        self._model_type = type(model) if model else model_type

        if not self._model_type:
            raise ValueError("One of model/model_type is required")

        if self._model_type not in self.TABLE_CONFIG:
            raise KeyError("Invalid model_type provided")

        self._config = self.TABLE_CONFIG[self._model_type]

    @cached_property
    def schema(self):
        return self._config["schema"]()

    @cached_property
    def key_field(self):
        return self._config["key_field"]

    @cached_property
    def item(self):
        if self._model:
            if isinstance(self._model, UsedJtiClaim):
                return int(self._model.used_at.timestamp())

            if isinstance(self._model, EQSession):
                return json.dumps(self.schema.dump(self._model))

            return self.schema.dump(self._model)

    @cached_property
    def key_value(self):
        if self._model:
            return getattr(self._model, self.key_field)

    @cached_property
    def table_name(self):
        return current_app.config[self._config["table_name_key"]]


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
