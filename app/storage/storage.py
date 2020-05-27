from abc import abstractmethod, ABC
from datetime import datetime
from functools import cached_property

from dateutil.tz import tzutc
from flask import current_app

from app.data_model import app_models


class StorageModel:
    TABLE_CONFIG = {
        app_models.SubmittedResponse: {
            "key_field": "tx_id",
            "expiry_field": "expires_at",
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
            "expiry_field": "expires_at",
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

    def __init__(self, model_type, model=None):
        self._model_type = model_type
        self._model = model

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
    def expires_in(self):
        if self._model and self.expiry_field:
            expiry_at = getattr(self._model, self.expiry_field)
            return expiry_at - datetime.now(tz=tzutc())

    @cached_property
    def key_value(self):
        if self._model:
            return getattr(self._model, self.key_field)

    @cached_property
    def table_name(self):
        return current_app.config[self._config["table_name_key"]]

    def serialise(self):
        if self._model:
            return self._schema.dump(self._model)

    def deserialise(self, serialised_item):
        return self._schema.load(serialised_item)


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
