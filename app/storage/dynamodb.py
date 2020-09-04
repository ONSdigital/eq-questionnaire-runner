from botocore.exceptions import ClientError

from app.storage.errors import ItemAlreadyExistsError

from .storage import StorageHandler, StorageModel


class Dynamodb(StorageHandler):
    def put(self, model, overwrite=True):
        storage_model = StorageModel(model_type=type(model))
        table = self.client.Table(storage_model.table_name)

        put_kwargs = {"Item": storage_model.serialize(model)}
        if not overwrite:
            put_kwargs[
                "ConditionExpression"
            ] = f"attribute_not_exists({storage_model.key_field})"

        try:
            response = table.put_item(**put_kwargs)["ResponseMetadata"][
                "HTTPStatusCode"
            ]
            return response == 200
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise ItemAlreadyExistsError() from e

            raise  # pragma: no cover

    def get(self, model_type, key_value):
        storage_model = StorageModel(model_type=model_type)
        table = self.client.Table(storage_model.table_name)
        key = {storage_model.key_field: key_value}

        response = table.get_item(Key=key, ConsistentRead=True)
        serialized_item = response.get("Item")

        if serialized_item:
            return storage_model.deserialize(serialized_item)

    def delete(self, model):
        storage_model = StorageModel(model_type=type(model))
        table = self.client.Table(storage_model.table_name)
        key_value = getattr(model, storage_model.key_field)
        key = {storage_model.key_field: key_value}

        response = table.delete_item(Key=key)
        item = response.get("Item")
        return item
