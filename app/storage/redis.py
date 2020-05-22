import json
from datetime import datetime

from dateutil.tz import tzutc

from app.storage.errors import ItemAlreadyExistsError
from .storage import StorageModel, StorageHandler


class Redis(StorageHandler):
    def put(self, model, overwrite=True):
        storage_model = StorageModel(model=model)
        item = storage_model.item
        item.pop(storage_model.key_field)

        if len(item) == 1 and storage_model.expiry_field in item:
            # Don't store a value if the only key that is not the key_field is the expiry_field
            value = ""
        else:
            value = json.dumps(item)

        expires_in = model.expires_at - datetime.now(tz=tzutc())
        record_created = self.client.set(
            name=storage_model.key_value, value=value, ex=expires_in, nx=not overwrite
        )

        if not record_created:
            raise ItemAlreadyExistsError()

    def get(self, model_type, key_value):
        storage_model = StorageModel(model_type=model_type)
        item = self.client.get(key_value)

        if item:
            item_dict = json.loads(item.decode("utf-8"))
            item_dict[storage_model.key_field] = key_value

            return storage_model.schema.load(item_dict)

    def delete(self, model):
        storage_model = StorageModel(model=model)
        return self.client.delete(storage_model.key_value)
