from dataclasses import asdict, dataclass
from typing import Iterable, Iterator, TypedDict, cast


class RelationshipDict(TypedDict, total=False):
    list_item_id: str
    to_list_item_id: str
    relationship: str


@dataclass
class Relationship:
    """
    Represents a relationship between two items.
    """

    list_item_id: str
    to_list_item_id: str
    relationship: str

    def for_json(self) -> RelationshipDict:
        return cast(RelationshipDict, asdict(self))


class RelationshipStore:
    """
    Stores and updates relationships.
    """

    def __init__(self, relationships: Iterable[RelationshipDict] | None = None) -> None:
        self._is_dirty = False
        self._relationships = self._build_map(relationships or [])

    def __iter__(self) -> Iterator[Relationship]:
        return iter(self._relationships.values())

    def __contains__(self, relationship: Relationship) -> bool:
        return (
            relationship.list_item_id,
            relationship.to_list_item_id,
        ) in self._relationships

    def __len__(self) -> int:
        return len(self._relationships)

    @property
    def is_dirty(self) -> bool:
        return self._is_dirty

    def clear(self) -> None:
        self._relationships.clear()
        self._is_dirty = True

    def serialize(self) -> list[RelationshipDict]:
        return [
            relationship.for_json() for relationship in self._relationships.values()
        ]

    def get_relationship(
        self, list_item_id: str, to_list_item_id: str
    ) -> Relationship | None:
        key = (list_item_id, to_list_item_id)
        return self._relationships.get(key)

    def remove_relationship(self, list_item_id: str, to_list_item_id: str) -> None:
        key = (list_item_id, to_list_item_id)
        if self._relationships.pop(key, None):
            self._is_dirty = True

    def add_or_update(self, relationship: Relationship) -> None:
        key = (relationship.list_item_id, relationship.to_list_item_id)

        existing_relationship = self._relationships.get(key)

        if existing_relationship != relationship:
            self._is_dirty = True
            self._relationships[key] = relationship

    def remove_all_relationships_for_list_item_id(self, list_item_id: str) -> None:
        """Remove all relationships associated with a particular list_item_id
        This method iterates through the entire list of relationships.
        """

        keys_to_delete = [
            (relationship.list_item_id, relationship.to_list_item_id)
            for relationship in self
            if list_item_id
            in (
                relationship.to_list_item_id,
                relationship.list_item_id,
            )
        ]

        for key in keys_to_delete:
            del self._relationships[key]
            self._is_dirty = True

    @staticmethod
    def _build_map(
        relationships: Iterable[RelationshipDict],
    ) -> dict[tuple[str, str], Relationship]:
        return {
            (
                relationship["list_item_id"],
                relationship["to_list_item_id"],
            ): Relationship(**relationship)
            for relationship in relationships
        }
