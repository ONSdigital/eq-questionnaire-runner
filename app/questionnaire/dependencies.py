from __future__ import annotations

from typing import TYPE_CHECKING, Mapping, Sequence

from ordered_set import OrderedSet
from werkzeug.datastructures import MultiDict

from app.data_models import ProgressStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.questionnaire_schema import get_sources_for_types_from_data
from app.utilities.mappings import get_flattened_mapping_values
from app.utilities.types import LocationType, SectionKey

if TYPE_CHECKING:
    from app.questionnaire.path_finder import PathFinder  # pragma: no cover


def get_routing_path_block_ids_by_section_for_dependent_sections(
    *,
    location: LocationType,
    progress_store: ProgressStore,
    path_finder: PathFinder,
    source_types: set[str],
    data: MultiDict | Mapping | Sequence,
    sections_to_ignore: list | None = None,
    ignore_keys: list[str] | None = None,
    dependent_sections: dict[str, set[str]] | dict[str, OrderedSet[str]],
) -> dict[SectionKey, tuple[str, ...]]:
    block_ids_by_section: dict[SectionKey, tuple[str, ...]] = {}
    sections_to_ignore = sections_to_ignore or []

    dependents = (
        OrderedSet(dependent_sections.get(location.block_id, []))
        if location.block_id
        else get_flattened_mapping_values(dependent_sections)
    )

    if dependents and not get_sources_for_types_from_data(
        source_types=source_types, data=data, ignore_keys=ignore_keys
    ):
        return block_ids_by_section

    for section in dependents:
        # Dependent sections other than the current section cannot be a repeating section
        list_item_id = location.list_item_id if section == location.section_id else None
        key = SectionKey(section, list_item_id)

        if key in sections_to_ignore:
            continue

        if key in progress_store.started_section_keys():
            routing_path = path_finder.routing_path(key)
            block_ids_by_section[key] = routing_path.block_ids

    return block_ids_by_section


def get_routing_path_block_ids_by_section_for_calculation_summary_dependencies(
    *,
    location: LocationType,
    progress_store: ProgressStore,
    path_finder: PathFinder,
    data: MultiDict | Mapping | Sequence,
    sections_to_ignore: list | None = None,
    ignore_keys: list[str] | None = None,
    schema: QuestionnaireSchema,
) -> dict[SectionKey, tuple[str, ...]]:
    """
    If the current location depends on any calculated or grand calculated summaries,
    for all the sections that those CS or GCS values depend on, get the blocks on the path for that section.
    These routing path block ids are then used to ensure the CS/GCS only includes answers on the path
    """
    dependent_sections = schema.calculation_summary_section_dependencies_by_block[
        location.section_id
    ]
    return get_routing_path_block_ids_by_section_for_dependent_sections(
        location=location,
        progress_store=progress_store,
        sections_to_ignore=sections_to_ignore,
        data=data,
        path_finder=path_finder,
        source_types={"calculated_summary", "grand_calculated_summary"},
        ignore_keys=ignore_keys,
        dependent_sections=dependent_sections,
    )
