from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, MutableMapping, Optional

from app.data_models.answer_store import AnswerStore
from app.data_models.data_stores import DataStores
from app.data_models.list_store import ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.data_models.progress_store import ProgressStore
from app.data_models.supplementary_data_store import SupplementaryDataStore
from app.questionnaire.rules.utils import parse_iso_8601_datetime
from app.utilities.json import json_dumps, json_loads

if TYPE_CHECKING:
    from app.storage.encrypted_questionnaire_storage import (  # pragma: no cover
        EncryptedQuestionnaireStorage,
    )


class QuestionnaireStore:
    LATEST_VERSION = 1

    def __init__(
        self, storage: EncryptedQuestionnaireStorage, version: Optional[int] = None
    ):
        self._storage = storage
        if version is None:
            version = self.get_latest_version_number()
        self.version = version
        self._metadata: MutableMapping = {}
        self._stores = DataStores()
        self.data_stores = self._stores
        self.submitted_at: Optional[datetime]
        self.collection_exercise_sid: Optional[str]

        (
            raw_data,
            self.collection_exercise_sid,
            version,
            self.submitted_at,
        ) = self._storage.get_user_data()

        if raw_data:
            self._deserialize(raw_data)
        if version is not None:
            self.version = version

    def get_latest_version_number(self) -> int:
        return self.LATEST_VERSION

    def set_metadata(self, to_set: MutableMapping) -> QuestionnaireStore:
        """
        Set metadata. This should only be used where absolutely necessary.
        Metadata should normally be read only.
        """
        self._metadata = to_set
        self._stores.metadata = MetadataProxy.from_dict(self._metadata)

        return self

    def _deserialize(self, data: str) -> None:
        json_data = json_loads(data)
        self._stores.progress_store = ProgressStore(json_data.get("PROGRESS"))
        self.set_metadata(json_data.get("METADATA", {}))
        self._stores.supplementary_data_store = SupplementaryDataStore.deserialize(
            json_data.get("SUPPLEMENTARY_DATA", {})
        )
        self._stores.answer_store = AnswerStore(json_data.get("ANSWERS"))
        self._stores.list_store = ListStore.deserialize(json_data.get("LISTS"))
        self._stores.response_metadata = json_data.get("RESPONSE_METADATA", {})

    def serialize(self) -> str:
        data = {
            "METADATA": self._metadata,
            "ANSWERS": list(self._stores.answer_store),
            "SUPPLEMENTARY_DATA": self._stores.supplementary_data_store.serialize(),
            "LISTS": self._stores.list_store.serialize(),
            "PROGRESS": self._stores.progress_store.serialize(),
            "RESPONSE_METADATA": self._stores.response_metadata,
        }
        return json_dumps(data)

    def delete(self) -> None:
        self._storage.delete()
        self._metadata.clear()
        self._stores.response_metadata = {}
        self._stores.answer_store.clear()
        self._stores.progress_store.clear()

    def save(self) -> None:
        data = self.serialize()
        collection_exercise_sid = (
            self.collection_exercise_sid or self._metadata["collection_exercise_sid"]
        )
        response_expires_at = self._metadata["response_expires_at"]
        self._storage.save(
            data=data,
            collection_exercise_sid=collection_exercise_sid,
            submitted_at=self.submitted_at,
            expires_at=parse_iso_8601_datetime(response_expires_at),
        )
