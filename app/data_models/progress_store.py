from typing import Iterable, MutableMapping

from app.data_models.progress import CompletionStatus, Progress, ProgressDict
from app.questionnaire.location import Location, SectionKey
from app.utilities.types import LocationType


class ProgressStore:
    """
    An object that stores and updates references to sections and list items
    that have been started.
    """

    def __init__(
        self,
        progress: Iterable[ProgressDict] | None = None,
    ) -> None:
        """
        Instantiate a ProgressStore object that tracks the progress status of Sections & Repeating Sections,
        and their completed blocks, as well as Repeating Blocks for List Items.
            - Standard Sections are keyed by Section ID, and a None List Item ID
            - Repeating Sections (dynamic Sections created for List Items that have been added using a List Collector)
                are keyed by their Section ID, and the List Item ID of the item it is the section for.
            - Repeating Blocks for List Items are keyed by the Section ID for the Section in which their List Collector
                appears, and the List Item ID. Repeating Blocks progress is only tracked if the List Collector
                that created the List Item has Repeating Blocks, and progress of the Repeating Blocks for a List Item
                indicates if all required Repeating Blocks from the List Collector have been completed for the List Item.
        Args:
            progress: A list of hierarchical dict containing the completion status
                and completed blocks of Sections, Repeating Sections and List Items
        """
        self._is_dirty: bool = False
        self._is_routing_backwards: bool = False
        self._progress: MutableMapping[SectionKey, Progress] = self._build_map(
            progress or []
        )

    def __contains__(self, section_key: SectionKey) -> bool:
        return section_key in self._progress

    @staticmethod
    def _build_map(
        section_list: Iterable[ProgressDict],
    ) -> MutableMapping:
        """
        Builds the ProgressStore's data structure from a list of section dictionaries.

        The `section_key` is tuple consisting of `section_id` and the `list_item_id`.
        The `section` is a mutableMapping created from the Progress object.

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
            SectionKey(
                section["section_id"], section.get("list_item_id")
            ): Progress.from_dict(section)
            for section in section_list
        }

    @property
    def is_dirty(self) -> bool:
        return self._is_dirty

    @property
    def is_routing_backwards(self) -> bool:
        return self._is_routing_backwards

    def is_section_complete(self, section_key: SectionKey) -> bool:
        """
        Return True if the CompletionStatus of the Section or List Item specified by the given section_id and
         list_item_id is COMPLETED or INDIVIDUAL_RESPONSE_REQUESTED, else False.
        """
        return section_key in self.section_keys(
            statuses={
                CompletionStatus.COMPLETED,
                CompletionStatus.INDIVIDUAL_RESPONSE_REQUESTED,
            }
        )

    def section_keys(
        self,
        statuses: Iterable[CompletionStatus] | None = None,
        section_ids: Iterable[str] | None = None,
    ) -> list[SectionKey]:
        """
        Return the Keys of the Section and Repeating Blocks progresses stored in this ProgressStore.
        """
        if not statuses:
            statuses = CompletionStatus

        section_keys = [
            section_key
            for section_key, section_progress in self._progress.items()
            if section_progress.status in statuses
        ]

        if section_ids is None:
            return section_keys

        return [
            progress_key
            for progress_key in section_keys
            if any(section_id in progress_key for section_id in section_ids)
        ]

    def update_section_status(
        self, status: CompletionStatus, section_key: SectionKey
    ) -> bool:
        """
        Updates the status of the Section or Repeating Blocks for a list item specified by the key based on the given section id and list item id.
        """
        updated = False
        if section_key in self._progress:
            if self._progress[section_key].status != status:
                updated = True
                self._progress[section_key].status = status
                self._is_dirty = True

        elif status == CompletionStatus.INDIVIDUAL_RESPONSE_REQUESTED:
            self._progress[section_key] = Progress(
                block_ids=[], status=status, **section_key.to_dict()
            )
            self._is_dirty = True

        return updated

    def get_section_status(self, section_key: SectionKey) -> CompletionStatus:
        """
        Return the CompletionStatus of the Section or Repeating Blocks for a list item,
        specified by the given section_id and list_item_id in SectionKey.
        Returns NOT_STARTED if the progress does not exist
        """
        if section_key in self._progress:
            return self._progress[section_key].status

        return CompletionStatus.NOT_STARTED

    def get_block_status(
        self, *, block_id: str, section_key: SectionKey
    ) -> CompletionStatus:
        """
        Return the completion status of the block specified by the given block_id,
        if it is part of the progress of the given Section or Repeating Blocks for list item
        specified by the given section_id or list_item_id
        """
        blocks = self.get_completed_block_ids(section_key)
        if block_id in blocks:
            return CompletionStatus.COMPLETED

        return CompletionStatus.NOT_STARTED

    def get_completed_block_ids(self, section_key: SectionKey) -> list[str]:
        """
        Return the block ids recorded as part of the progress for the Section or Repeating Blocks
        for list item specified by the given section_id and list_item_id in SectionKey
        """
        if section_key in self._progress:
            return self._progress[section_key].block_ids

        return []

    def add_completed_location(self, location: LocationType) -> None:
        """
        Adds the block from the given Location, to the progress specified by the
        section id and list item id within the Location.
        """
        completed_block_ids = self.get_completed_block_ids(location.section_key)

        if location.block_id not in completed_block_ids:
            completed_block_ids.append(location.block_id)  # type: ignore
            progress_key = location.section_key
            if progress_key in self._progress:
                self._progress[progress_key].block_ids = completed_block_ids
            else:
                self._progress[progress_key] = Progress(
                    section_id=location.section_id,
                    list_item_id=location.list_item_id,
                    block_ids=completed_block_ids,
                    status=CompletionStatus.IN_PROGRESS,
                )

            self._is_dirty = True

    def remove_completed_location(self, location: LocationType) -> bool:
        """
        Removes the block in the given Location, from the progress specified by the
        section id and list item id within the Location if it exists in the store.
        """
        progress_key = location.section_key
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
            SectionKey(section_id, progress_list_item_id)
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
        self, section_ids: Iterable[str] | None = None
    ) -> list[SectionKey]:
        return self.section_keys(
            statuses={CompletionStatus.COMPLETED, CompletionStatus.IN_PROGRESS},
            section_ids=section_ids,
        )

    def is_block_complete(self, *, block_id: str, section_key: SectionKey) -> bool:
        return block_id in self.get_completed_block_ids(section_key)
