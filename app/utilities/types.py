from typing import TYPE_CHECKING, NamedTuple, TypeAlias, Union

if TYPE_CHECKING:
    from app.questionnaire.location import Location
    from app.questionnaire.relationship_location import RelationshipLocation

LocationType: TypeAlias = Union["Location", "RelationshipLocation"]


class SectionKey(NamedTuple):
    section_id: str
    list_item_id: str | None = None
