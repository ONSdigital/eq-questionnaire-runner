import json

from app.storage.errors import ItemAlreadyExistsError
from .storage import StorageModel, StorageHandler


class Redis(StorageHandler):
    def put(self, model, overwrite=True):
        storage_model = StorageModel(model=model)
        item = storage_model.item
        if isinstance(item, dict):
            item = json.dumps(item)

        record_created = self.client.set(
            name=storage_model.key_value,
            value=item,
            ex=model.expires_in_seconds,
            nx=not overwrite,
        )

        if not record_created:
            raise ItemAlreadyExistsError()

    def get(self, model_type, key_value):
        storage_model = StorageModel(model_type=model_type)
        item = self.client.get(key_value)

        if item:
            return storage_model.schema.load(json.loads(item.decode("utf-8")))

    def delete(self, model):
        storage_model = StorageModel(model=model)
        return self.client.delete(storage_model.key_value)
