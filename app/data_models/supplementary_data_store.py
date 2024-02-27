from __future__ import annotations

from functools import cached_property
from typing import Iterable, Mapping, MutableMapping

from werkzeug.datastructures import ImmutableDict

from app.utilities.make_immutable import make_immutable
from app.utilities.types import (
    SupplementaryDataKeyType,
    SupplementaryDataListMapping,
    SupplementaryDataValueType,
)


class InvalidSupplementaryDataSelector(Exception):
    pass


class SupplementaryDataStore:
    """
    An object that stores supplementary data
    """

    def __init__(
        self,
        supplementary_data: MutableMapping | None = None,
        list_mappings: Mapping[str, list[SupplementaryDataListMapping]] | None = None,
    ):
        """
        Initialised with the "data" value from the sds api response
        and list mappings of the form
        {
            list_name: [
                {"identifier": identifier-1, "list_item_id": list_item_id-1 },
                {"identifier": identifier-2, "list_item_id": list_item_id-2 }
            ]
        }
        """
        self._raw_data = supplementary_data or {}
        self._list_mappings = list_mappings or {}
        # use shallow copy of the data, as items will be popped off
        self._data_map = self._build_map({**self._raw_data})

    @cached_property
    def raw_data(self) -> ImmutableDict:
        data: ImmutableDict = make_immutable(self._raw_data)
        return data

    @cached_property
    def list_mappings(self) -> ImmutableDict[str, list[ImmutableDict]]:
        mappings: ImmutableDict[str, list[ImmutableDict]] = make_immutable(
            self._list_mappings
        )
        return mappings

    @cached_property
    def list_lookup(self) -> dict[str, dict[str | int, str]]:
        """Create a lookup for easily finding the list_item_id for a given identifier"""
        return {
            list_name: {
                mapping["identifier"]: mapping["list_item_id"] for mapping in list_data
            }
            for list_name, list_data in self._list_mappings.items()
        }

    def _build_map(
        self, data: MutableMapping
    ) -> dict[SupplementaryDataKeyType, SupplementaryDataValueType]:
        """
        The raw data will be of the form
        {
          "some_key": "some_value"
          "items": {
            "some_list": [
                {"identifier": ... },
                {"identifier": ... }
            ]
          }
        }
        each list item has an identifier which will link to a list-item-id in self.list_lookup
        for example: {"some_list": {identifier-1: list_item_id-1, identifier-2: list_item_id-2 }}

        resulting map based off list mappings has the form
        {
            ("some_key", None): "some_value"
            ("some_list", list_item_id-1): {"identifier": identifier-1, ...}
            ("some_list", list_item_id-2): {"identifier": identifier-2, ...}
        }
        """
        list_items = data.pop("items", {})
        resulting_map: dict[SupplementaryDataKeyType, SupplementaryDataValueType] = {
            (key, None): value for key, value in data.items()
        }
        for list_name, list_data in list_items.items():
            for item in list_data:
                identifier = item["identifier"]
                list_item_id = self.list_lookup[list_name][identifier]
                resulting_map[(list_name, list_item_id)] = item
        return resulting_map

    def get_data(
        self,
        *,
        identifier: str,
        selectors: Iterable[str] | None = None,
        list_item_id: str | None = None,
    ) -> SupplementaryDataValueType:
        """
        Used to retrieve supplementary data in a similar style to AnswerStore
        the identifier is the top level key for static data, and the name of the list for list items
        selectors are used to reference nested data

        For example if you wanted the identifier for the first item in "some_list"
        it would be get_data(identifier="some_list", selectors=["identifier"], list_item_id=list_item_id-1)
        """
        if self.is_data_repeating(identifier) and not list_item_id:
            values = []
            for _list_item_id in self.list_lookup.get(identifier, {}).values():
                value = self._resolve_value(
                    identifier=identifier,
                    selectors=selectors,
                    list_item_id=_list_item_id,
                )
                if value is not None:
                    values.append(value)
            return values

        return self._resolve_value(
            identifier=identifier, selectors=selectors, list_item_id=list_item_id
        )

    def _resolve_value(
        self,
        *,
        identifier: str,
        selectors: Iterable[str] | None,
        list_item_id: str | None,
    ) -> dict | str | list | None:
        value = self._data_map.get((identifier, list_item_id))
        # for nested data, index with each selector, or return None if there is no data to index
        for selector in selectors or []:
            if value is None:
                return None
            if not isinstance(value, Mapping):
                # if value is not None, and also not index able, raise an error
                raise InvalidSupplementaryDataSelector(
                    f"Cannot use the selector `{selector}` on non-nested data"
                )
            value = value.get(selector)

        return value

    def is_data_repeating(self, identifier: str) -> bool:
        """
        Returns true if the identifier is for one of the lists
        """
        return identifier in self._list_mappings

    def serialize(self) -> dict:
        return {
            "data": self._raw_data,
            "list_mappings": self._list_mappings,
        }

    @classmethod
    def deserialize(cls, serialized_data: Mapping) -> SupplementaryDataStore:
        if not serialized_data:
            return cls()

        return cls(
            supplementary_data=serialized_data["data"],
            list_mappings=serialized_data["list_mappings"],
        )
