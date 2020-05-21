import json
from datetime import datetime

from app.data_model.app_models import EQSession, UsedJtiClaim
from app.storage.errors import ItemAlreadyExistsError
from .storage import StorageModel, StorageHandler


class Redis(StorageHandler):
    def put(self, model, overwrite=False):
        if isinstance(model, UsedJtiClaim):
            record_created = self._put_jti(model)
        elif isinstance(model, EQSession):
            record_created = self._put_session(model)
        else:
            raise NotImplementedError(
                "Only UsedJtiClaimSchema and EQSessionSchema supported"
            )

        if not record_created:
            raise ItemAlreadyExistsError()

    def _put_jti(self, jti):
        expires_in_seconds = int((jti.expires_at - jti.used_at).total_seconds())
        record_created = self.client.set(
            name=jti.jti_claim,
            value=int(jti.used_at.timestamp()),
            ex=expires_in_seconds,
            nx=True,
        )

        return record_created

    def _put_session(self, model):
        storage_model = StorageModel(model=model)
        expires_at_datetime = datetime.utcfromtimestamp(
            storage_model.item["expires_at"]
        )
        expires_in_seconds = int(
            (expires_at_datetime - datetime.utcnow()).total_seconds()
        )

        record_created = self.client.set(
            name=model.eq_session_id,
            value=json.dumps(storage_model.item),
            ex=expires_in_seconds,
            nx=False,
        )

        return record_created

    def get(self, model_type, key_value):
        storage_model = StorageModel(model_type=model_type)
        item = self.client.get(key_value)

        if item:
            return storage_model.schema.load(json.loads(item.decode("utf-8")))

    def delete(self, model):
        storage_model = StorageModel(model=model)
        return self.client.delete(storage_model.key_value)
