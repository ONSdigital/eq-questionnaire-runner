import contextlib

from google.cloud.datastore import Key


class MockDatastore:

    # pylint: disable=unused-argument
    def __init__(self, **kwargs):
        self.storage = {}
        self.delete_call_count = 0

    # pylint: disable=no-self-use
    def transaction(self):
        return contextlib.suppress()

    def put(self, entity):
        self.storage[entity.key] = entity

    def get(self, key):
        return self.storage.get(key)

    def delete(self, key):
        self.delete_call_count += 1
        del self.storage[key]

    # pylint: disable=no-self-use
    def key(self, *path_args, **kwargs):
        return Key(*path_args, project="local", **kwargs)
