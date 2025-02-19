from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping, TypedDict


class CompletionStatus(StrEnum):
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    NOT_STARTED = "NOT_STARTED"


class ProgressDict(TypedDict, total=False):
    section_id: str
    block_ids: list[str]
    status: CompletionStatus
    list_item_id: str | None


@dataclass
class Progress:
    section_id: str
    block_ids: list[str]
    status: CompletionStatus
    list_item_id: str | None = None

    @classmethod
    def from_dict(cls, progress_dict: ProgressDict) -> Progress:
        return cls(
            section_id=progress_dict["section_id"],
            block_ids=progress_dict["block_ids"],
            status=CompletionStatus(progress_dict["status"]),
            list_item_id=progress_dict.get("list_item_id"),
        )

    def for_json(self) -> Mapping:
        attributes = vars(self)
        return {k: v for k, v in attributes.items() if v is not None}
