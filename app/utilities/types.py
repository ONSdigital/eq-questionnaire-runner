from typing import TYPE_CHECKING, NamedTuple, TypeAlias, Union

if TYPE_CHECKING:
    from app.questionnaire.location import Location  # pragma: no cover
    from app.questionnaire.relationship_location import (
        RelationshipLocation,  # pragma: no cover
    )

LocationType: TypeAlias = Union["Location", "RelationshipLocation"]


class SectionKey(NamedTuple):
    section_id: str
    list_item_id: str | None = None


class DependentSection(NamedTuple):
    section_id: str
    list_item_id: str | None
    is_complete: bool | None

    @property
    def section_key(self) -> SectionKey:
        return SectionKey(self.section_id, self.list_item_id)
