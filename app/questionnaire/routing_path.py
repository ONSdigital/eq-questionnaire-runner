from typing import Iterator, SupportsIndex

from app.utilities.types import SectionKey


class RoutingPath:
    """Holds a list of block_ids and has section_id, list_item_id and list_name attributes"""

    def __init__(
        self,
        *,
        block_ids: list[str],
        section_id: str,
        list_item_id: str | None = None,
        list_name: str | None = None,
    ):
        self.block_ids = tuple(block_ids)
        self.section_id = section_id
        self.list_item_id = list_item_id
        self.list_name = list_name

    def __len__(self) -> int:
        return len(self.block_ids)

    def __getitem__(self, index: int) -> str:
        return self.block_ids[index]

    def __iter__(self) -> Iterator[str]:
        return iter(self.block_ids)

    def __reversed__(self) -> Iterator[str]:
        return reversed(self.block_ids)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RoutingPath):
            return (
                self.block_ids == other.block_ids
                and self.section_id == other.section_id
                and self.list_item_id == other.list_item_id
                and self.list_name == other.list_name
            )

        if isinstance(other, list):
            return self.block_ids == tuple(other)

        return self.block_ids == other

    def index(self, value: str, *args: SupportsIndex) -> int:
        return self.block_ids.index(value, *args)

    @property
    def section_key(self) -> SectionKey:
        return SectionKey(self.section_id, self.list_item_id)
