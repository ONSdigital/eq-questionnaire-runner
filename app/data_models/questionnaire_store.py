from __future__ import annotations

from datetime import datetime
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Mapping, Optional, Union

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress_store import ProgressStore
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
        self._metadata: Any = {}
        # self.metadata is a read-only view over self._metadata
        self.metadata: Any = MappingProxyType(self._metadata)
        self.response_metadata: dict = {}
        self.list_store = ListStore()
        self.answer_store = AnswerStore()
        self.progress_store = ProgressStore()
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

    def set_metadata(
        self, to_set: Mapping[str, Union[str, int, list]]
    ) -> QuestionnaireStore:
        """
        Set metadata. This should only be used where absolutely necessary.
        Metadata should normally be read only.
        """
        self._metadata = to_set
        self.metadata = MappingProxyType(self._metadata)

        return self

    def _deserialize(self, data: str) -> None:
        json_data = json_loads(data)
        self.progress_store = ProgressStore(json_data.get("PROGRESS"))
        self.set_metadata(json_data.get("METADATA", {}))
        self.answer_store = AnswerStore(json_data.get("ANSWERS"))
        self.list_store = ListStore.deserialize(json_data.get("LISTS"))
        self.response_metadata = json_data.get("RESPONSE_METADATA", {})

    def serialize(self) -> Any:
        data = {
            "METADATA": self._metadata,
            "ANSWERS": list(self.answer_store),
            "LISTS": self.list_store.serialize(),
            "PROGRESS": self.progress_store.serialize(),
            "RESPONSE_METADATA": self.response_metadata,
        }
        return json_dumps(data)

    def delete(self) -> None:
        self._storage.delete()
        self._metadata.clear()
        self.response_metadata = {}
        self.answer_store.clear()
        self.progress_store.clear()

    def save(self) -> None:
        data = self.serialize()
        collection_exercise_sid = (
            self.collection_exercise_sid or self._metadata["collection_exercise_sid"]
        )
        response_expires_at = self._metadata.get("response_expires_at")
        self._storage.save(
            data=data,
            collection_exercise_sid=collection_exercise_sid,
            submitted_at=self.submitted_at,
            expires_at=parse_iso_8601_datetime(response_expires_at)
            if response_expires_at
            else None,
        )
