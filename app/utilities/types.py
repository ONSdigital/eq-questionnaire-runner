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
    """
    The 'is_complete' property is used when updating the progress of the section. If the value is 'None'
    then the routing path for this section will be re-evaluated to determine if it is complete.
    """

    section_id: str
    list_item_id: str | None = None
    is_complete: bool | None = None

    @property
    def section_key(self) -> SectionKey:
        return SectionKey(self.section_id, self.list_item_id)
