from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional, TypedDict


class ProgressDictType(TypedDict, total=False):
    section_id: str
    block_ids: list[Optional[str]]
    status: str
    list_item_id: str


@dataclass
class Progress:
    section_id: str
    block_ids: list[Optional[str]]
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
