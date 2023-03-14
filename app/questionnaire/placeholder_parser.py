from decimal import Decimal
from typing import TYPE_CHECKING, Any, Mapping, MutableMapping, Sequence, Union

from app.data_models import ProgressStore
from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import Location, QuestionnaireSchema, path_finder
from app.questionnaire.placeholder_transforms import PlaceholderTransforms
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.value_source_resolver import (
    ValueSourceEscapedTypes,
    ValueSourceResolver,
    ValueSourceTypes,
)

if TYPE_CHECKING:
    from app.questionnaire.path_finder import PathFinder  # pragma: no cover
    from app.questionnaire.placeholder_renderer import (
        PlaceholderRenderer,  # pragma: no cover
    )

TransformedValueTypes = Union[None, str, int, Decimal, bool]


class PlaceholderParser:
    """
    Parses placeholder statements from a schema dict and returns a map of their
    final values
    """

    def __init__(
        self,
        language: str,
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: MetadataProxy | None,
        response_metadata: Mapping,
        schema: QuestionnaireSchema,
        renderer: "PlaceholderRenderer",
        progress_store: ProgressStore,
        list_item_id: str | None = None,
        location: Location | RelationshipLocation | None = None,
        placeholder_preview_mode: bool | None = False,
    ):
        self._transformer = PlaceholderTransforms(language, schema, renderer)
        self._placeholder_map: MutableMapping[
            str, Union[ValueSourceEscapedTypes, ValueSourceTypes, None]
        ] = {}
        self._answer_store = answer_store
        self._list_store = list_store
        self._metadata = metadata
        self._response_metadata = response_metadata
        self._list_item_id = list_item_id
        self._schema = schema
        self._location = location
        self._progress_store = progress_store
        self._placeholder_preview_mode = placeholder_preview_mode

        self._path_finder = path_finder.PathFinder(
            schema=self._schema,
            answer_store=self._answer_store,
            list_store=self._list_store,
            progress_store=self._progress_store,
            metadata=self._metadata,
            response_metadata=self._response_metadata,
        )

        self._value_source_resolver = self._get_value_source_resolver()
        self._routing_paths: dict = {}

    def __call__(
        self, placeholder_list: Sequence[Mapping]
    ) -> MutableMapping[str, Union[ValueSourceEscapedTypes, ValueSourceTypes]]:
        placeholder_list = QuestionnaireSchema.get_mutable_deepcopy(placeholder_list)

        sections_to_ignore = list(self._routing_paths)

        if routing_path_block_ids_map := self._get_routing_path_block_ids(
            sections_to_ignore
        ):
            self._routing_paths.update(routing_path_block_ids_map)

            routing_path_block_ids = get_flattened_mapping_value(
                routing_path_block_ids_map
            )
            self._value_source_resolver = self._get_value_source_resolver(
                routing_path_block_ids
            )

        for placeholder in placeholder_list:
            if placeholder["placeholder"] not in self._placeholder_map:
                self._placeholder_map[
                    placeholder["placeholder"]
                ] = self._parse_placeholder(placeholder)
        return self._placeholder_map

    def _get_value_source_resolver(
        self, routing_path_block_ids: set[str] | None = None
    ) -> ValueSourceResolver:
        return ValueSourceResolver(
            answer_store=self._answer_store,
            list_store=self._list_store,
            metadata=self._metadata,
            schema=self._schema,
            location=self._location,
            list_item_id=self._list_item_id,
            escape_answer_values=True,
            response_metadata=self._response_metadata,
            use_default_answer=True,
            assess_routing_path=False,
            routing_path_block_ids=routing_path_block_ids,
        )

    def _parse_placeholder(self, placeholder: Mapping) -> Any:
        if self._placeholder_preview_mode and not self._all_value_sources_metadata(
            placeholder
        ):
            return f'{{{placeholder["placeholder"]}}}'

        try:
            return self._parse_transforms(placeholder["transforms"])
        except KeyError:
            return self._value_source_resolver.resolve(placeholder["value"])

    def _parse_transforms(
        self, transform_list: Sequence[Mapping]
    ) -> TransformedValueTypes:
        transformed_value: TransformedValueTypes = None

        for transform in transform_list:
            transform_args: MutableMapping[str, Any] = {}

            for arg_key, arg_value in transform["arguments"].items():
                resolved_value: Union[
                    ValueSourceEscapedTypes, ValueSourceTypes, TransformedValueTypes
                ]

                if isinstance(arg_value, list):
                    resolved_value = self._resolve_value_source_list(arg_value)
                elif isinstance(arg_value, dict):
                    if "value" in arg_value:
                        resolved_value = arg_value["value"]
                    elif arg_value["source"] == "previous_transform":
                        resolved_value = transformed_value
                    else:
                        resolved_value = self._value_source_resolver.resolve(arg_value)
                else:
                    resolved_value = arg_value

                transform_args[arg_key] = resolved_value

            transformed_value = getattr(self._transformer, transform["transform"])(
                **transform_args
            )

        return transformed_value

    def _resolve_value_source_list(
        self, value_source_list: list[dict]
    ) -> list[ValueSourceTypes]:
        values: list[ValueSourceTypes] = []
        for value_source in value_source_list:
            value = self._value_source_resolver.resolve(value_source)
            if isinstance(value, list):
                values.extend(value)
            else:
                values.append(value)
        return values

    def _get_routing_path_block_ids(
        self, sections_to_ignore: list | None = None
    ) -> dict[str, list[str]]:
        if self._location:
            return get_block_ids_for_calculated_summary_dependencies(
                schema=self._schema,
                location=self._location,
                progress_store=self._progress_store,
                path=self._path_finder,
                sections_to_ignore=sections_to_ignore,
            )
        return {}

    def _all_value_sources_metadata(self, placeholder: Mapping) -> bool:
        sources = self._schema.get_values_for_key(placeholder, key="source")
        return all(source == "metadata" for source in sources)


def get_block_ids_for_calculated_summary_dependencies(
    schema: QuestionnaireSchema,
    location: Location | RelationshipLocation,
    progress_store: ProgressStore,
    path: "PathFinder",
    sections_to_ignore: list | None = None,
) -> dict[str, list[str]]:
    # Type ignore: Added to this method as the block will exist at this point
    blocks_id_by_section = {}

    sections_to_ignore = sections_to_ignore or []
    dependent_sections = schema.calculated_summary_section_dependencies_by_block.get(
        location.section_id
    )

    if block_id := location.block_id:
        try:
            dependents = dependent_sections[block_id]  # type: ignore
        except KeyError:
            dependents = set()
    else:
        dependents = {
            section
            for dependents in dependent_sections.values()  # type: ignore
            if dependents
            for section in dependents
        }

    for section in dependents:
        if section in sections_to_ignore:
            continue

        if schema.get_repeat_for_section(section):
            key = (section, location.list_item_id)
        else:
            key = (section, None)

        if key in progress_store.started_section_keys():
            routing_path = path.routing_path(*key)
            blocks_id_by_section[section] = routing_path.block_ids

    return blocks_id_by_section


def get_flattened_mapping_value(
    routing_path_block_ids_map: dict[str, list[str]]
) -> set[str]:
    return {x for v in routing_path_block_ids_map.values() for x in v}
