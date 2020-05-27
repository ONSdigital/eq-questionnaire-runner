from google.api_core.retry import Retry
from google.cloud.datastore import Entity
from structlog import get_logger

from .storage import StorageModel, StorageHandler

logger = get_logger()


class Datastore(StorageHandler):
    @Retry()
    def put(self, model, overwrite=True):
        if not overwrite:
            raise NotImplementedError("Unique key checking not supported")

        storage_model = StorageModel(model=model, model_type=type(model))
        serialized_item = storage_model.serialize()

        key = self.client.key(storage_model.table_name, storage_model.key_value)
        entity = Entity(key=key, exclude_from_indexes=tuple(serialized_item.keys()))
        entity.update(serialized_item)

        self.client.put(entity)

    @Retry()
    def get(self, model_type, key_value):
        storage_model = StorageModel(model_type=model_type)
        key = self.client.key(storage_model.table_name, key_value)

        serialized_item = self.client.get(key)
        if serialized_item:
            return storage_model.deserialize(serialized_item)

    @Retry()
    def delete(self, model):
        storage_model = StorageModel(model=model, model_type=type(model))
        key = self.client.key(storage_model.table_name, storage_model.key_value)

        return self.client.delete(key)
