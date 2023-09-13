from typing import NamedTuple, TypeAlias, TypedDict

from app.questionnaire.location import Location
from app.questionnaire.relationship_location import RelationshipLocation

LocationType: TypeAlias = Location | RelationshipLocation
SupplementaryDataKeyType: TypeAlias = tuple[str, str | None]
SupplementaryDataValueType: TypeAlias = dict | str | list | None


class SectionKey(NamedTuple):
    section_id: str
    list_item_id: str | None


class SupplementaryDataListMapping(TypedDict):
    identifier: str | int
    list_item_id: str
