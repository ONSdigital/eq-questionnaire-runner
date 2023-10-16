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
    return_to_answer_id: str | None = None  # TODO: This can be an anchor, so make sure to check for it when unpacking in the to_dict function
    return_to_list_name: str | None = None
    return_to_list_item_id: str | None = None
    # anchor: # TODO: Check if this can live in the class, or whether it's

    def to_dict(self) -> Mapping:
        attributes = asdict(self)
        return {
            k: v for k, v in attributes.items() if v is not None
        }  # TODO: Add a boolean check to see if anchor == return_to_answer_id?
