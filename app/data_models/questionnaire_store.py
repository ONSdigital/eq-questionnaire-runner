from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, MutableMapping, Optional

from app.data_models.answer_store import AnswerStore
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
        # self.metadata is a read-only view over self._metadata
        self.metadata: MetadataProxy | None = None
        self.response_metadata: MutableMapping = {}
        self.list_store = ListStore()
        self.answer_store = AnswerStore()
        self.progress_store = ProgressStore()
        self.supplementary_data_store = SupplementaryDataStore()
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
        self.metadata = MetadataProxy.from_dict(self._metadata)

        return self

    def set_supplementary_data(self, to_set: MutableMapping) -> None:
        """
        Used to set or update the supplementary data whenever the sds endpoint is called
        (Which should be once per session, but only if the sds_dataset_id has changed)

        this updates ListStore to add/update any lists for supplementary data and stores the
        identifier -> list_item_id mappings in the supplementary data store to use in the payload at the end
        """
        if self.supplementary_data_store.list_mappings:
            self._remove_old_supplementary_lists_and_answers(new_data=to_set)

        list_mappings = {
            list_name: self._create_supplementary_list(
                list_name=list_name, list_data=list_data
            )
            for list_name, list_data in to_set.get("items", {}).items()
        }

        self.supplementary_data_store = SupplementaryDataStore(
            supplementary_data=to_set, list_mappings=list_mappings
        )

    def _create_supplementary_list(
        self, *, list_name: str, list_data: list[dict]
    ) -> dict[str, str]:
        """
        Creates or updates a list in ListStore based off supplementary data
        returns the identifier -> list_item_id mappings used
        """
        list_mapping: dict[str, str] = {}
        for list_item in list_data:
            identifier = list_item["identifier"]
            # if any pre-existing supplementary data already has a mapping for this list item
            # then its already in the list store and doesn't require adding
            if not (
                list_item_id := self.supplementary_data_store.list_mappings.get(
                    list_name, {}
                ).get(identifier)
            ):
                list_item_id = self.list_store.add_list_item(list_name)
            list_mapping[identifier] = list_item_id
        return list_mapping

    def _remove_old_supplementary_lists_and_answers(
        self, new_data: MutableMapping
    ) -> None:
        """
        In the case that existing supplementary data is being replaced with new data: any list items in the old data
        but not the new data are removed from the list store and related answers are deleted
        :param new_data - the new supplementary data for comparison
        """
        deleted_list_item_ids: set[str] = set()
        for list_name, mappings in self.supplementary_data_store.list_mappings.items():
            if list_name in new_data.get("items", {}):
                new_identifiers = [
                    item["identifier"] for item in new_data["items"][list_name]
                ]
                for identifier, list_item_id in mappings.items():
                    if identifier not in new_identifiers:
                        self.list_store.delete_list_item(list_name, list_item_id)
                        deleted_list_item_ids.add(list_item_id)
            else:
                self.list_store.delete_list(list_name)
                deleted_list_item_ids.update(mappings.values())
        self.answer_store.remove_all_answers_for_list_item_ids(*deleted_list_item_ids)

    def _deserialize(self, data: str) -> None:
        json_data = json_loads(data)
        self.progress_store = ProgressStore(json_data.get("PROGRESS"))
        self.set_metadata(json_data.get("METADATA", {}))
        self.supplementary_data_store = SupplementaryDataStore.deserialize(
            json_data.get("SUPPLEMENTARY_DATA", {})
        )
        self.answer_store = AnswerStore(json_data.get("ANSWERS"))
        self.list_store = ListStore.deserialize(json_data.get("LISTS"))
        self.response_metadata = json_data.get("RESPONSE_METADATA", {})

    def serialize(self) -> str:
        data = {
            "METADATA": self._metadata,
            "ANSWERS": list(self.answer_store),
            "SUPPLEMENTARY_DATA": self.supplementary_data_store.serialize(),
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
        response_expires_at = self._metadata["response_expires_at"]
        self._storage.save(
            data=data,
            collection_exercise_sid=collection_exercise_sid,
            submitted_at=self.submitted_at,
            expires_at=parse_iso_8601_datetime(response_expires_at),
        )
