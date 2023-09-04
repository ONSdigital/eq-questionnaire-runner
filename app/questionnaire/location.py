from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, NamedTuple

from flask import url_for


class SectionKey(NamedTuple):
    section_id: str
    list_item_id: str | None


class InvalidLocationException(Exception):
    def __init__(self, value: str):
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
    block_id: str | None = None
    list_name: str | None = None
    list_item_id: str | None = None

    def __hash__(self) -> int:
        return hash(frozenset(self.__dict__.values()))

    @classmethod
    def from_dict(cls, location_dict: Mapping[str, str]) -> Location:
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

    def url(self, **kwargs: Any) -> str:
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

    @property
    def section_key(self) -> SectionKey:
        return SectionKey(self.section_id, self.list_item_id)
