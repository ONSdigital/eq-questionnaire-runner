from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any, Mapping, MutableMapping, Sequence, TypeAlias

from ordered_set import OrderedSet

from app.data_models import ProgressStore
from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire import path_finder as pf
from app.questionnaire.dependencies import (
    get_block_ids_for_dependencies,
    get_calculated_summary_block_ids_of_dependent_section,
)
from app.questionnaire.placeholder_transforms import PlaceholderTransforms
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.value_source_resolver import (
    ValueSourceEscapedTypes,
    ValueSourceResolver,
    ValueSourceTypes,
)
from app.utilities.mappings import get_flattened_mapping_values

if TYPE_CHECKING:
    from app.questionnaire.placeholder_renderer import (
        PlaceholderRenderer,  # pragma: no cover
    )

TransformedValueTypes: TypeAlias = None | str | int | Decimal | bool


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
        response_metadata: MutableMapping,
        schema: QuestionnaireSchema,
        renderer: PlaceholderRenderer,
        progress_store: ProgressStore,
        list_item_id: str | None = None,
        location: Location | RelationshipLocation | None = None,
        placeholder_preview_mode: bool | None = False,
    ):
        self._transformer = PlaceholderTransforms(language, schema, renderer)
        self._placeholder_map: MutableMapping[
            str, ValueSourceEscapedTypes | ValueSourceTypes | None
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

        self._path_finder = pf.PathFinder(
            schema=self._schema,
            answer_store=self._answer_store,
            list_store=self._list_store,
            progress_store=self._progress_store,
            metadata=self._metadata,
            response_metadata=self._response_metadata,
        )

        self._value_source_resolver = self._get_value_source_resolver()
        self._routing_path_block_ids_by_section_key: dict = {}

    def __call__(
        self, placeholder_list: Sequence[Mapping]
    ) -> MutableMapping[str, ValueSourceEscapedTypes | ValueSourceTypes]:
        sections_to_ignore = list(self._routing_path_block_ids_by_section_key)

        if routing_path_block_ids_map := self._get_routing_path_block_ids(
            data=placeholder_list,
            sections_to_ignore=sections_to_ignore,
        ):
            self._routing_path_block_ids_by_section_key.update(
                routing_path_block_ids_map
            )

            routing_path_block_ids = get_flattened_mapping_values(
                routing_path_block_ids_map
            )
            self._value_source_resolver = self._get_value_source_resolver(
                routing_path_block_ids=routing_path_block_ids,
            )

        for placeholder in placeholder_list:
            # :TODO: Caching of placeholder values will need to be revisited once validation is added to ensure that placeholders are globally unique
            # if placeholder["placeholder"] not in self._placeholder_map:
            self._placeholder_map[placeholder["placeholder"]] = self._parse_placeholder(
                placeholder
            )
        return self._placeholder_map

    def _get_value_source_resolver(
        self,
        *,
        routing_path_block_ids: OrderedSet[str] | None = None,
        assess_routing_path: bool = False,
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
            assess_routing_path=assess_routing_path,
            routing_path_block_ids=routing_path_block_ids,
            progress_store=self._progress_store,
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
            transform_args: MutableMapping = {}
            value_source_resolver = self._get_value_source_resolver_for_transform(
                transform
            )
            for arg_key, arg_value in transform["arguments"].items():
                resolved_value: ValueSourceEscapedTypes | ValueSourceTypes | TransformedValueTypes

                if isinstance(arg_value, list):
                    resolved_value = self._resolve_value_source_list(
                        value_source_list=arg_value,
                        value_source_resolver=value_source_resolver,
                    )
                elif isinstance(arg_value, dict):
                    if "value" in arg_value:
                        resolved_value = arg_value["value"]
                    elif arg_value["source"] == "previous_transform":
                        resolved_value = transformed_value
                    else:
                        resolved_value = value_source_resolver.resolve(arg_value)
                else:
                    resolved_value = arg_value

                transform_args[arg_key] = resolved_value

            transformed_value = getattr(self._transformer, transform["transform"])(
                **transform_args
            )

        return transformed_value

    @staticmethod
    def _resolve_value_source_list(
        value_source_list: list[dict], value_source_resolver: ValueSourceResolver
    ) -> list[ValueSourceTypes]:
        values: list[ValueSourceTypes] = []
        for value_source in value_source_list:
            value = value_source_resolver.resolve(value_source)
            if isinstance(value, list):
                values.extend(value)
            else:
                values.append(value)
        return values

    def _get_routing_path_block_ids(
        self,
        data: Sequence[Mapping],
        sections_to_ignore: list | None = None,
    ) -> dict[tuple, tuple[str, ...]] | None:
        if not self._location:
            return {}

        return get_calculated_summary_block_ids_of_dependent_section(
            location=self._location,
            progress_store=self._progress_store,
            sections_to_ignore=sections_to_ignore,
            data=data,
            path_finder=self._path_finder,
            ignore_keys=["when"],
            schema=self._schema,
        )

    def _all_value_sources_metadata(self, placeholder: Mapping) -> bool:
        sources = self._schema.get_values_for_key(placeholder, key="source")
        return all(source == "metadata" for source in sources)

    def _get_value_source_resolver_for_transform(
        self, transform: Mapping
    ) -> ValueSourceResolver:
        if self._location and (
            dependent_sections := self._schema.placeholder_section_dependencies_by_block[
                self._location.section_id
            ]
        ):
            block_ids = get_block_ids_for_dependencies(
                location=self._location,
                progress_store=self._progress_store,
                sections_to_ignore=["when"],
                path_finder=self._path_finder,
                data=transform,
                source_type="answers",
                dependent_sections=dependent_sections,
            )
            self._routing_path_block_ids_by_section_key.update(block_ids)
            routing_path_block_ids = get_flattened_mapping_values(block_ids)

            if (
                value_source_routing_block_ids := self._value_source_resolver.routing_path_block_ids
            ):
                for block_id in value_source_routing_block_ids:
                    routing_path_block_ids.append(block_id)

            return self._get_value_source_resolver(
                routing_path_block_ids=routing_path_block_ids,
                assess_routing_path=True,
            )

        return self._value_source_resolver
