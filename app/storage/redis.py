from datetime import datetime

import simplejson as json
from dateutil.tz import tzutc

from app.storage.errors import ItemAlreadyExistsError

from .storage import StorageHandler, StorageModel


class Redis(StorageHandler):
    def put(self, model, overwrite=True):
        storage_model = StorageModel(model_type=type(model))
        serialized_item = storage_model.serialize(model)
        serialized_item.pop(storage_model.key_field)

        if len(serialized_item) == 1 and storage_model.expiry_field in serialized_item:
            # Don't store a value if the only key that is not the key_field is the expiry_field
            value = ""
        else:
            value = json.dumps(serialized_item)

        key_value = getattr(model, storage_model.key_field)

        expires_in = None
        if storage_model.expiry_field:
            expiry_at = getattr(model, storage_model.expiry_field)
            expires_in = expiry_at - datetime.now(tz=tzutc())

        record_created = self.client.set(
            name=key_value, value=value, ex=expires_in, nx=not overwrite
        )

        if not record_created:
            raise ItemAlreadyExistsError()

    def get(self, model_type, key_value):
        storage_model = StorageModel(model_type=model_type)
        item = self.client.get(key_value)

        if item:
            item_dict = json.loads(item.decode("utf-8"))
            item_dict[storage_model.key_field] = key_value

            return storage_model.deserialize(item_dict)

    def delete(self, model):
        storage_model = StorageModel(model_type=type(model))
        key_value = getattr(model, storage_model.key_field)
        return self.client.delete(key_value)
