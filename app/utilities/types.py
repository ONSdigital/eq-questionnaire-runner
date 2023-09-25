from typing import TYPE_CHECKING, NamedTuple, TypeAlias, TypedDict, Union

if TYPE_CHECKING:
    from app.questionnaire.location import Location  # pragma: no cover
    from app.questionnaire.relationship_location import (
        RelationshipLocation,  # pragma: no cover
    )

LocationType: TypeAlias = Union["Location", "RelationshipLocation"]
SupplementaryDataKeyType: TypeAlias = tuple[str, str | None]
SupplementaryDataValueType: TypeAlias = dict | str | list | None


class SectionKeyDict(TypedDict):
    section_id: str
    list_item_id: str | None


class SectionKey(NamedTuple):
    section_id: str
    list_item_id: str | None = None

    def to_dict(self) -> SectionKeyDict:
        return SectionKeyDict(
            section_id=self.section_id, list_item_id=self.list_item_id
        )


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


class SupplementaryDataListMapping(TypedDict):
    identifier: str | int
    list_item_id: str


class Choice(NamedTuple):
    value: str
    label: str


class ChoiceWithDetailAnswer(NamedTuple):
    value: str
    label: str
    detail_answer_id: str | None
