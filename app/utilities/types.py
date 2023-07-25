from typing import NamedTuple, TypeAlias

from app.questionnaire.location import Location
from app.questionnaire.relationship_location import RelationshipLocation

LocationType: TypeAlias = Location | RelationshipLocation


class SectionKey(NamedTuple):
    section_id: str
    list_item_id: str | None
