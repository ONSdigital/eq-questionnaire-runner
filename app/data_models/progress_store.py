from dataclasses import astuple, dataclass
from typing import Iterable, List, Mapping, MutableMapping, Optional

from app.data_models.progress import Progress
from app.questionnaire.location import Location


@dataclass
class CompletionStatus:
    COMPLETED: str = "COMPLETED"
    IN_PROGRESS: str = "IN_PROGRESS"
    NOT_STARTED: str = "NOT_STARTED"
    INDIVIDUAL_RESPONSE_REQUESTED: str = "INDIVIDUAL_RESPONSE_REQUESTED"

    def __iter__(self):
        return iter(astuple(self))


class ProgressStore:
    """
    An object that stores and updates references to sections and blocks
    that have been started.
    """

    def __init__(self, in_progress_sections: List[Mapping] = None) -> None:
        """
        Instantiate a ProgressStore object that tracks the status of sections and its completed blocks
        Args:
            in_progress_sections: A list of hierarchical dict containing the section status and completed blocks
        """
        self._is_dirty = False  # type: bool
        self._is_routing_backwards = False  # type: bool
        self._progress = self._build_map(
            in_progress_sections or []
        )  # type: MutableMapping

    def __contains__(self, section_key) -> bool:
        return section_key in self._progress

    @staticmethod
    def _build_map(section_progress_list: List[Mapping]) -> MutableMapping:
        """
        Builds the progress_store's data structure from a list of progress dictionaries.

        The `section_key` is tuple consisting of `section_id` and the `list_item_id`.
        The `section_progress` is a mutableMapping created from the Progress object.

        Example structure:
        {
            ('some-section', 'a-list-item-id'): {
                'section_id': 'some-section',
                'status': 'COMPLETED',
                'list_item_id': 'a-list-item-id',
                'block_ids: ['some-block', 'another-block']
            }
        }
        """

        return {
            (
                section_progress["section_id"],
                section_progress.get("list_item_id"),
            ): Progress.from_dict(section_progress)
            for section_progress in section_progress_list
        }

    @property
    def is_dirty(self) -> bool:
        return self._is_dirty

    @property
    def is_routing_backwards(self) -> bool:
        return self._is_routing_backwards

    def is_section_complete(
        self, section_id: str, list_item_id: Optional[str] = None
    ) -> bool:
        return (section_id, list_item_id) in self.section_keys(
            statuses={
                CompletionStatus.COMPLETED,
                CompletionStatus.INDIVIDUAL_RESPONSE_REQUESTED,
            }
        )

    def section_keys(
        self, statuses: Iterable[str] = None, section_ids: Iterable[str] = None
    ):
        if not statuses:
            statuses = {*CompletionStatus()}

        section_keys = [
            section_key
            for section_key, section_progress in self._progress.items()
            if section_progress.status in statuses
        ]

        if section_ids is None:
            return section_keys

        return [
            section_key
            for section_key in section_keys
            if any(section_id in section_key for section_id in section_ids)
        ]

    def update_section_status(
        self, section_status: str, section_id: str, list_item_id: Optional[str] = None
    ) -> None:
        section_key = (section_id, list_item_id)
        if section_key in self._progress:
            self._progress[section_key].status = section_status
            self._is_dirty = True

        elif (
            section_status == CompletionStatus.INDIVIDUAL_RESPONSE_REQUESTED
            and section_key not in self._progress
        ):
            self._progress[section_key] = Progress(
                section_id=section_id,
                list_item_id=list_item_id,
                block_ids=[],
                status=section_status,
            )
            self._is_dirty = True

    def get_section_status(
        self, section_id: str, list_item_id: Optional[str] = None
    ) -> str:
        section_key = (section_id, list_item_id)
        if section_key in self._progress:
            return self._progress[section_key].status

        return CompletionStatus.NOT_STARTED

    def get_completed_block_ids(
        self, section_id: str, list_item_id: Optional[str] = None
    ) -> List[Optional[str]]:
        section_key = (section_id, list_item_id)
        if section_key in self._progress:
            return self._progress[section_key].block_ids

        return []

    def add_completed_location(self, location: Location) -> None:
        section_id = location.section_id
        list_item_id = location.list_item_id

        completed_block_ids = self.get_completed_block_ids(section_id, list_item_id)

        if location.block_id not in completed_block_ids:
            completed_block_ids.append(location.block_id)

            section_key = (section_id, list_item_id)

            if section_key in self._progress:
                self._progress[section_key].block_ids = completed_block_ids
            else:
                self._progress[section_key] = Progress(
                    section_id=section_id,
                    list_item_id=list_item_id,
                    block_ids=completed_block_ids,
                )

            self._is_dirty = True

    def remove_completed_location(self, location: Location) -> None:
        section_key = (location.section_id, location.list_item_id)
        if (
            section_key in self._progress
            and location.block_id in self._progress[section_key].block_ids
        ):
            self._progress[section_key].block_ids.remove(location.block_id)

            if not self._progress[section_key].block_ids:
                del self._progress[section_key]

            self._is_dirty = True

    def remove_progress_for_list_item_id(self, list_item_id: str) -> None:
        """Remove progress associated with a particular list_item_id
        This method iterates through all progress.

        *Not efficient.*
        """

        section_keys_to_delete = [
            (section_id, progress_list_item_id)
            for section_id, progress_list_item_id in self._progress
            if progress_list_item_id == list_item_id
        ]

        for section_key in section_keys_to_delete:
            del self._progress[section_key]

            self._is_dirty = True

    def serialize(self) -> List:
        return list(self._progress.values())

    def remove_location_for_backwards_routing(self, location: Location) -> None:
        self.remove_completed_location(location=location)
        self._is_routing_backwards = True

    def clear(self) -> None:
        self._progress.clear()
        self._is_dirty = True
