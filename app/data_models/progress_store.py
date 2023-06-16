from dataclasses import astuple, dataclass
from typing import Iterable, Iterator, MutableMapping, Optional

from app.data_models.progress import Progress, ProgressDictType
from app.questionnaire.location import Location

ProgressKeyType = tuple[str, Optional[str]]


@dataclass
class CompletionStatus:
    COMPLETED: str = "COMPLETED"
    IN_PROGRESS: str = "IN_PROGRESS"
    NOT_STARTED: str = "NOT_STARTED"
    INDIVIDUAL_RESPONSE_REQUESTED: str = "INDIVIDUAL_RESPONSE_REQUESTED"

    def __iter__(self) -> Iterator[tuple[str]]:
        return iter(astuple(self))


class ProgressStore:
    """
    An object that stores and updates references to sections and list items
    that have been started.
    """

    def __init__(
        self,
        in_progress_sections_and_list_items: Iterable[ProgressDictType] | None = None,
    ) -> None:
        """
        Instantiate a ProgressStore object that tracks the status of sections and list items, and their completed blocks.
        Args:
            in_progress_sections_and_list_items: A list of hierarchical dict containing the completion status and completed blocks
        """
        self._is_dirty: bool = False
        self._is_routing_backwards: bool = False
        self._progress: MutableMapping[ProgressKeyType, Progress] = self._build_map(
            in_progress_sections_and_list_items or []
        )

    def __contains__(self, progress_key: ProgressKeyType) -> bool:
        return progress_key in self._progress

    @staticmethod
    def _build_map(progress_list: Iterable[ProgressDictType]) -> MutableMapping:
        """
        Builds the progress_store's data structure from a list of progress dictionaries.

        The `progress_key` is tuple consisting of `section_id` and the `list_item_id`.
        The `progress` is a mutableMapping created from the Progress object.

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
                progress["section_id"],
                progress.get("list_item_id"),
            ): Progress.from_dict(progress)
            for progress in progress_list
        }

    @property
    def is_dirty(self) -> bool:
        return self._is_dirty

    @property
    def is_routing_backwards(self) -> bool:
        return self._is_routing_backwards

    def is_section_or_list_item_complete(
        self, section_id: str, list_item_id: Optional[str] = None
    ) -> bool:
        return (section_id, list_item_id) in self.progress_keys(
            statuses={
                CompletionStatus.COMPLETED,
                CompletionStatus.INDIVIDUAL_RESPONSE_REQUESTED,
            }
        )

    def progress_keys(
        self,
        statuses: Optional[Iterable[str]] = None,
        section_ids: Optional[Iterable[str]] = None,
    ) -> list[ProgressKeyType]:
        if not statuses:
            statuses = {*CompletionStatus()}

        progress_keys = [
            section_key
            for section_key, section_progress in self._progress.items()
            if section_progress.status in statuses
        ]

        if section_ids is None:
            return progress_keys

        return [
            progress_key
            for progress_key in progress_keys
            if any(section_id in progress_key for section_id in section_ids)
        ]

    def update_section_or_list_item_completion_status(
        self,
        completion_status: str,
        section_id: str,
        list_item_id: Optional[str] = None,
    ) -> bool:
        """
        Updates the completion status of the section or list item specified by the key based on the given section id and list item id.
        """
        updated = False
        section_key = (section_id, list_item_id)
        if section_key in self._progress:
            if self._progress[section_key].status != completion_status:
                updated = True
                self._progress[section_key].status = completion_status
                self._is_dirty = True

        elif completion_status == CompletionStatus.INDIVIDUAL_RESPONSE_REQUESTED:
            self._progress[section_key] = Progress(
                section_id=section_id,
                list_item_id=list_item_id,
                block_ids=[],
                status=completion_status,
            )
            self._is_dirty = True

        return updated

    def get_section_or_list_item_status(
        self, section_id: str, list_item_id: Optional[str] = None
    ) -> str:
        progress_key = (section_id, list_item_id)
        if progress_key in self._progress:
            return self._progress[progress_key].status

        return CompletionStatus.NOT_STARTED

    def get_block_status(
        self, *, block_id: str, section_id: str, list_item_id: str | None = None
    ) -> str:
        section_or_list_item_blocks = self.get_completed_block_ids(
            section_id=section_id, list_item_id=list_item_id
        )
        if block_id in section_or_list_item_blocks:
            return CompletionStatus.COMPLETED

        return CompletionStatus.NOT_STARTED

    def get_completed_block_ids(
        self, *, section_id: str, list_item_id: str | None = None
    ) -> list[str]:
        progress_key = (section_id, list_item_id)
        if progress_key in self._progress:
            return self._progress[progress_key].block_ids

        return []

    def add_completed_location(self, location: Location) -> None:
        section_id = location.section_id
        list_item_id = location.list_item_id

        completed_block_ids = self.get_completed_block_ids(
            section_id=section_id, list_item_id=list_item_id
        )

        if location.block_id not in completed_block_ids:
            completed_block_ids.append(location.block_id)  # type: ignore

            progress_key = (section_id, list_item_id)

            if progress_key in self._progress:
                self._progress[progress_key].block_ids = completed_block_ids
            else:
                self._progress[progress_key] = Progress(
                    section_id=section_id,
                    list_item_id=list_item_id,
                    block_ids=completed_block_ids,
                    status=CompletionStatus.IN_PROGRESS,
                )

            self._is_dirty = True

    def remove_completed_location(self, location: Location) -> bool:
        progress_key = (location.section_id, location.list_item_id)
        if (
            progress_key in self._progress
            and location.block_id in self._progress[progress_key].block_ids
        ):
            self._progress[progress_key].block_ids.remove(location.block_id)

            if not self._progress[progress_key].block_ids:
                self._progress[progress_key].status = CompletionStatus.IN_PROGRESS

            self._is_dirty = True
            return True

        return False

    def remove_progress_for_list_item_id(self, list_item_id: str) -> None:
        """Remove progress associated with a particular list_item_id
        This method iterates through all progress.

        *Not efficient.*
        """

        progress_keys_to_delete = [
            (section_id, progress_list_item_id)
            for section_id, progress_list_item_id in self._progress
            if progress_list_item_id == list_item_id
        ]

        for progress_key in progress_keys_to_delete:
            del self._progress[progress_key]

            self._is_dirty = True

    def serialize(self) -> list[Progress]:
        return list(self._progress.values())

    def remove_location_for_backwards_routing(self, location: Location) -> None:
        self.remove_completed_location(location=location)
        self._is_routing_backwards = True

    def clear(self) -> None:
        self._progress.clear()
        self._is_dirty = True

    def started_section_keys(
        self, section_ids: Optional[Iterable[str]] = None
    ) -> list[ProgressKeyType]:
        return self.progress_keys(
            statuses={CompletionStatus.COMPLETED, CompletionStatus.IN_PROGRESS},
            section_ids=section_ids,
        )
