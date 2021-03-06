from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional

from flask import url_for


class InvalidLocationException(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value


@dataclass
class Location:
    """
    Store a location in the questionnaire.

    section_id: The id of the current section.
    block_id: The id of the current block. This could be a block inside a list collector
    list_item_id: The list_item_id if this location is associated with a list
    list_name: The list name
    """

    section_id: str
    block_id: Optional[str] = None
    list_name: Optional[str] = None
    list_item_id: Optional[str] = None

    def __hash__(self):
        return hash(frozenset(self.__dict__.values()))

    @classmethod
    def from_dict(cls, location_dict: Mapping):
        section_id = location_dict["section_id"]
        block_id = location_dict["block_id"]
        list_item_id = location_dict.get("list_item_id")
        list_name = location_dict.get("list_name")
        return cls(
            section_id=section_id,
            block_id=block_id,
            list_name=list_name,
            list_item_id=list_item_id,
        )

    def url(self, **kwargs) -> str:
        """
        Return the survey runner url that this location represents
        Any additional keyword arguments are parsed as query strings.
        :return:
        """
        return url_for(
            "questionnaire.block",
            block_id=self.block_id,
            list_name=self.list_name,
            list_item_id=self.list_item_id,
            **kwargs,
        )
