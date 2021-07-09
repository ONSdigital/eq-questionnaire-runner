from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Optional, Union


@dataclass
class Answer:
    answer_id: str
    value: Union[str, int, float, list, dict]
    list_item_id: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, answer_dict: dict) -> Answer:
        return cls(
            answer_id=answer_dict["answer_id"],
            value=answer_dict["value"],
            list_item_id=answer_dict.get("list_item_id"),
        )

    def for_json(self) -> dict:
        output = self.to_dict()
        if not self.list_item_id:
            del output["list_item_id"]
        return output

    def to_dict(self) -> dict:
        return asdict(self)
