from __future__ import annotations

from dataclasses import dataclass
from typing import List, Mapping, Optional


@dataclass
class Progress:
    section_id: str
    block_ids: List[Optional[str]]
    status: Optional[str] = None
    list_item_id: Optional[str] = None

    @classmethod
    def from_dict(cls, progress_dict: Mapping) -> Progress:
        return cls(
            section_id=progress_dict["section_id"],
            block_ids=progress_dict["block_ids"],
            status=progress_dict["status"],
            list_item_id=progress_dict.get("list_item_id"),
        )

    def for_json(self) -> Mapping:
        attributes = vars(self)
        return {k: v for k, v in attributes.items() if v is not None}
