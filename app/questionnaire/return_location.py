from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Mapping


@dataclass(kw_only=True, frozen=True)
class ReturnLocation:
    """
    Used to store return locations in the questionnaire.

    return_to: The name of the section to return to
    return_to_block_id: The block_id of the block to return to
    return_to_answer_id: The answer_id of the answer to return to
    return_to_list_name: The list_name to return to if the location is associated with a list
    return_to_list_item_id: The list_item_id to return to if the location is associated with a list
    """

    return_to: str | None = None
    return_to_block_id: str | None = None
    return_to_answer_id: str | None = None
    return_to_list_name: str | None = None
    return_to_list_item_id: str | None = None

    def to_dict(self, anchor_return_to_answer_id: bool = False) -> Mapping:
        attributes = asdict(self)
        if anchor_return_to_answer_id:
            attributes["_anchor"] = attributes["return_to_answer_id"]
            del attributes["return_to_answer_id"]
        return {k: v for k, v in attributes.items() if v is not None}
