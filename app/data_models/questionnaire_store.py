from types import MappingProxyType

import simplejson as json

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress_store import ProgressStore


class QuestionnaireStore:
    LATEST_VERSION = 1

    def __init__(self, storage, version=None):
        self._storage = storage
        if version is None:
            version = self.get_latest_version_number()
        self.version = version
        self._metadata = {}
        # self.metadata is a read-only view over self._metadata
        self.metadata = MappingProxyType(self._metadata)
        self.response_metadata = {}
        self.list_store = ListStore()
        self.answer_store = AnswerStore()
        self.progress_store = ProgressStore()

        raw_data, version = self._storage.get_user_data()
        if raw_data:
            self._deserialize(raw_data)
        if version is not None:
            self.version = version

    def get_latest_version_number(self):
        return self.LATEST_VERSION

    def set_metadata(self, to_set):
        """
        Set metadata. This should only be used where absolutely necessary.
        Metadata should normally be read only.
        """
        self._metadata = to_set
        self.metadata = MappingProxyType(self._metadata)

        return self

    def _deserialize(self, data):
        json_data = json.loads(data, use_decimal=True)
        self.progress_store = ProgressStore(json_data.get("PROGRESS"))
        self.set_metadata(json_data.get("METADATA", {}))
        self.answer_store = AnswerStore(json_data.get("ANSWERS"))
        self.list_store = ListStore.deserialize(json_data.get("LISTS"))
        self.response_metadata = json_data.get("RESPONSE_METADATA", {})

    def serialize(self):
        data = {
            "METADATA": self._metadata,
            "ANSWERS": list(self.answer_store),
            "LISTS": self.list_store.serialize(),
            "PROGRESS": self.progress_store.serialize(),
            "RESPONSE_METADATA": self.response_metadata,
        }
        return json.dumps(data, for_json=True)

    def delete(self):
        self._storage.delete()
        self._metadata.clear()
        self.response_metadata = {}
        self.answer_store.clear()
        self.progress_store.clear()

    def save(self):
        data = self.serialize()
        self._storage.save(data=data)
