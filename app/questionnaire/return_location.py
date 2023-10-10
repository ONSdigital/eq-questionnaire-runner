from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(kw_only=True)
class ReturnLocation:
    """
    Used to store return locations in the questionnaire.

    return_to: TODO: Not sure what this is, in relation to the below IDs/names?
    return_to_block_id: The block_id of the block to return to
    return_to_answer_id: The answer_id of the answer to return to
    return_to_list_name: The list_name to return to if the location is associated with a list
    return_to_list_item_id: The list_item_id to return to if the location is associated with a list
    """

    return_to: str | None = None  # Can this be None??
    return_to_block_id: str | None = None
    return_to_answer_id: str | None = None
    return_to_list_name: str | None = None
    return_to_list_item_id: str | None = None


    # @classmethod
    # def from_dict(cls, return_location_dict: Mapping[str, str]) -> ReturnLocation:
    #     return_to = return_location_dict["return_to"]
    #     return_to_block_id = return_location_dict["return_to_block_id"]
    #     return_to_answer_id = return_location_dict["return_to_answer_id"]
    #     return_to_list_name = return_location_dict.get("return_to_list_name")
    #     return_to_list_item_id = return_location_dict.get("return_to_list_item_id")
    #     return cls(
    #         return_to=return_to,
    #         return_to_block_id=return_to_block_id,
    #         return_to_answer_id=return_to_answer_id,
    #         return_to_list_name=return_to_list_name,
    #         return_to_list_item_id=return_to_list_item_id,
    #     )

    # TODO: Similar to other dataclass functions. Do we want to allow potentially ALL populated values being passed into things like url_for()?
    def to_dict(self) -> Mapping:
        attributes = vars(self)
        return {k: v for k, v in attributes.items() if v is not None}



    # def url(self, **kwargs: Any) -> str:
    #     """
    #     Return the survey runner url that this location represents
    #     Any additional keyword arguments are parsed as query strings.
    #     :return:
    #     """
    #     return url_for(
    #         "questionnaire.block",
    #         block_id=self.block_id,
    #         list_name=self.list_name,
    #         list_item_id=self.list_item_id,
    #         **kwargs,
    #     )

    # @property
    # def section_key(self) -> SectionKey:
    #     return SectionKey(self.section_id, self.list_item_id)
