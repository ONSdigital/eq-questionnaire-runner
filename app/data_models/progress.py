from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional, TypedDict


class ProgressDictType(TypedDict, total=False):
    section_id: str
    block_ids: list[str]
    status: str
    list_item_id: str


@dataclass
class Progress:
    section_id: str
    block_ids: list[str]
    status: str
    list_item_id: Optional[str] = None

    @classmethod
    def from_dict(cls, progress_dict: ProgressDictType) -> Progress:
        return cls(
            section_id=progress_dict["section_id"],
            block_ids=progress_dict["block_ids"],
            status=progress_dict["status"],
            list_item_id=progress_dict.get("list_item_id"),
        )

    def for_json(self) -> Mapping:
        attributes = vars(self)
        return {k: v for k, v in attributes.items() if v is not None}


class ListItemProgressDictType(TypedDict, total=False):
    list_item_id: str
    status: str
    blocks: list[BlockProgressDictType]


class BlockProgressDictType(TypedDict, total=False):
    block_id: str
    status: str


@dataclass
class ListItemProgress:
    list_item_id: str
    status: str
    blocks: list[BlockProgress]

    @classmethod
    def from_dict(cls, list_item_progress_dict: ListItemProgressDictType) -> ListItemProgress:
        return cls(
            list_item_id=list_item_progress_dict["list_item_id"],
            status=list_item_progress_dict["status"],
            blocks=[
                BlockProgress.from_dict(block_progress)
                for block_progress in list_item_progress_dict["blocks"]
            ]
        )

    def to_dict(self) -> ListItemProgressDictType:
        return ListItemProgressDictType(
            list_item_id=self.list_item_id,
            status=self.status,
            blocks=[BlockProgressDictType(block_id=block.block_id, status=block.status) for block in self.blocks]
        )


@dataclass
class BlockProgress:
    block_id: str
    status: str

    @classmethod
    def from_dict(cls, block_progress_dict: BlockProgressDictType) -> BlockProgress:
        return cls(
            block_id=block_progress_dict["block_id"],
            status=block_progress_dict["status"]
        )
