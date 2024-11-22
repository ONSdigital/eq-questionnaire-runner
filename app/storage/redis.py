from datetime import datetime, timezone
from typing import Optional

import redis
from redis.exceptions import ConnectionError as RedisConnectionError
from structlog import get_logger

from app.storage.errors import ItemAlreadyExistsError
from app.storage.storage import ModelTypes, StorageHandler, StorageModel
from app.utilities.json import json_dumps, json_loads

logger = get_logger()


class Redis(StorageHandler):
    def __init__(
        self,
        client: redis.Redis,
    ) -> None:
        super().__init__(client)

    @staticmethod
    def log_retry(command: str) -> None:
        logger.info("retrying redis command", command=command)

    def put(self, model: ModelTypes, overwrite: bool = True) -> bool:
        storage_model = StorageModel(model_type=type(model))
        serialized_item = storage_model.serialize(model)
        serialized_item.pop(storage_model.key_field)

        if len(serialized_item) == 1 and storage_model.expiry_field in serialized_item:
            # Don't store a value if the only key that is not the key_field is the expiry_field
            value = ""
        else:
            value = json_dumps(serialized_item)

        key_value = getattr(model, storage_model.key_field)

        expires_in = None
        if storage_model.expiry_field:
            expiry_at = getattr(model, storage_model.expiry_field)
            expires_in = expiry_at - datetime.now(tz=timezone.utc)

        try:
            record_created = self.client.set(
                name=key_value, value=value, ex=expires_in, nx=not overwrite
            )
        except RedisConnectionError:
            self.log_retry("set")
            record_created = self.client.set(
                name=key_value, value=value, ex=expires_in, nx=not overwrite
            )

        if not record_created:
            raise ItemAlreadyExistsError()

        return True

    def get(self, model_type: type[ModelTypes], key_value: str) -> Optional[ModelTypes]:
        storage_model = StorageModel(model_type=model_type)
        try:
            item = self.client.get(key_value)
        except RedisConnectionError:
            self.log_retry("get")
            item = self.client.get(key_value)

        if item:
            item_dict = json_loads(item.decode("utf-8"))
            item_dict[storage_model.key_field] = key_value

            return storage_model.deserialize(item_dict)

    def delete(self, model: ModelTypes) -> None:
        storage_model = StorageModel(model_type=type(model))
        key_value = getattr(model, storage_model.key_field)

        try:
            self.client.delete(key_value)
        except RedisConnectionError:
            self.log_retry("delete")
            self.client.delete(key_value)
