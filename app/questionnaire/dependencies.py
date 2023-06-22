from __future__ import annotations

from typing import TYPE_CHECKING, Mapping, Sequence

from ordered_set import OrderedSet
from werkzeug.datastructures import MultiDict

from app.data_models import ProgressStore
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.questionnaire_schema import get_sources_for_type_from_data
from app.questionnaire.relationship_location import RelationshipLocation
from app.utilities.mappings import get_flattened_mapping_values

if TYPE_CHECKING:
    from app.questionnaire.path_finder import PathFinder  # pragma: no cover


def get_block_ids_for_dependencies(
    *,
    schema: QuestionnaireSchema,
    location: Location | RelationshipLocation,
    progress_store: ProgressStore,
    path_finder: PathFinder,
    source_type: str,
    data: MultiDict | Mapping | Sequence,
    sections_to_ignore: list | None = None,
    ignore_keys: list[str] | None = None,
) -> dict[tuple, tuple[str, ...]]:
    block_ids_by_section: dict[tuple, tuple[str, ...]] = {}
    sections_to_ignore = sections_to_ignore or []
    dependent_sections: dict[str, set[str]] | dict[str, OrderedSet[str]]
    if source_type == "calculated_summary":
        dependent_sections = schema.calculated_summary_section_dependencies_by_block[
            location.section_id
        ]

    else:
        dependent_sections = schema.placeholder_section_dependencies_by_block[
            location.section_id
        ]
        ignore_keys = None

    dependents = (
        OrderedSet(dependent_sections.get(location.block_id, []))
        if location.block_id
        else get_flattened_mapping_values(dependent_sections)
    )

    if dependents and not get_sources_for_type_from_data(
        source_type=source_type, data=data, ignore_keys=ignore_keys
    ):
        return block_ids_by_section

    for section in dependents:
        list_item_id = location.list_item_id if section == location.section_id else None
        key = (section, list_item_id)

        if key in sections_to_ignore:
            continue

        if key in progress_store.started_section_keys():
            routing_path = path_finder.routing_path(*key)
            block_ids_by_section[key] = routing_path.block_ids

    return block_ids_by_section
