from __future__ import annotations

from decimal import Decimal
from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    Mapping,
    MutableMapping,
    Sequence,
    TypeAlias,
)

from app.data_models.data_stores import DataStores
from app.questionnaire import QuestionnaireSchema
from app.questionnaire import path_finder as pf
from app.questionnaire.dependencies import (
    get_routing_path_block_ids_by_section_for_calculation_summary_dependencies,
    get_routing_path_block_ids_by_section_for_dependent_sections,
)
from app.questionnaire.placeholder_transforms import PlaceholderTransforms
from app.questionnaire.questionnaire_schema import (
    TRANSFORMS_REQUIRING_ROUTING_PATH,
    TRANSFORMS_REQUIRING_UNRESOLVED_ARGUMENTS,
)
from app.questionnaire.value_source_resolver import (
    ValueSourceEscapedTypes,
    ValueSourceResolver,
    ValueSourceTypes,
)
from app.utilities.mappings import get_flattened_mapping_values, get_values_for_key
from app.utilities.types import LocationType, SectionKey

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
        data_stores: DataStores,
        schema: QuestionnaireSchema,
        renderer: PlaceholderRenderer,
        list_item_id: str | None = None,
        location: LocationType | None = None,
        placeholder_preview_mode: bool | None = False,
    ):
        self._transformer = PlaceholderTransforms(language, schema, renderer)
        self._placeholder_map: MutableMapping[
            str, ValueSourceEscapedTypes | ValueSourceTypes | None
        ] = {}
        self._data_stores = data_stores
        self._list_item_id = list_item_id
        self._schema = schema
        self._location = location
        self._placeholder_preview_mode = placeholder_preview_mode

        self._path_finder = pf.PathFinder(
            schema=self._schema, data_stores=self._data_stores
        )

        self._value_source_resolver = self._get_value_source_resolver()
        self._routing_path_block_ids_by_section_key: dict = {}

    def __call__(
        self, placeholder_list: Sequence[Mapping]
    ) -> MutableMapping[str, ValueSourceEscapedTypes | ValueSourceTypes]:
        sections_to_ignore = list(self._routing_path_block_ids_by_section_key)

        if routing_path_block_ids_map := self._get_routing_path_block_ids_by_section_for_calculated_summary_dependencies(
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
        routing_path_block_ids: Iterable[str] | None = None,
        assess_routing_path: bool | None = False,
    ) -> ValueSourceResolver:
        return ValueSourceResolver(
            data_stores=self._data_stores,
            schema=self._schema,
            location=self._location,
            list_item_id=self._list_item_id,
            escape_answer_values=True,
            use_default_answer=True,
            assess_routing_path=assess_routing_path,
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
            transform_args: MutableMapping = {}
            value_source_resolver = self._get_value_source_resolver_for_transform(
                transform
            )

            if transform["transform"] in TRANSFORMS_REQUIRING_UNRESOLVED_ARGUMENTS:
                transform_args["unresolved_arguments"] = transform["arguments"]

            for arg_key, arg_value in transform["arguments"].items():
                resolved_value: (
                    ValueSourceEscapedTypes | ValueSourceTypes | TransformedValueTypes
                )

                if isinstance(arg_value, list):
                    resolved_value = value_source_resolver.resolve_list(
                        value_source_list=arg_value,
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

    def _get_routing_path_block_ids_by_section_for_calculated_summary_dependencies(
        self,
        data: Sequence[Mapping],
        sections_to_ignore: list[str] | None = None,
    ) -> dict[SectionKey, tuple[str, ...]] | None:
        if not self._location:
            return {}

        return (
            get_routing_path_block_ids_by_section_for_calculation_summary_dependencies(
                location=self._location,
                progress_store=self._data_stores.progress_store,
                sections_to_ignore=sections_to_ignore,
                data=data,
                path_finder=self._path_finder,
                ignore_keys=["when"],
                schema=self._schema,
            )
        )

    @staticmethod
    def _all_value_sources_metadata(placeholder: Mapping) -> bool:
        sources = get_values_for_key("source", data=placeholder)
        return all(source == "metadata" for source in sources)

    def _get_value_source_resolver_for_transform(
        self, transform: Mapping
    ) -> ValueSourceResolver:
        if (
            self._location
            and transform["transform"] in TRANSFORMS_REQUIRING_ROUTING_PATH
        ):
            dependent_sections = (
                self._schema.placeholder_transform_section_dependencies_by_block[
                    self._location.section_id
                ]
            )
            block_ids = get_routing_path_block_ids_by_section_for_dependent_sections(
                location=self._location,
                progress_store=self._data_stores.progress_store,
                sections_to_ignore=["when"],
                path_finder=self._path_finder,
                data=transform,
                source_types={"answers"},
                dependent_sections=dependent_sections,
            )
            self._routing_path_block_ids_by_section_key.update(block_ids)
            transform_routing_path_block_ids = get_flattened_mapping_values(block_ids)

            value_source_routing_block_ids = (
                self._value_source_resolver.routing_path_block_ids or set()
            )

            routing_path_block_ids = (
                set(value_source_routing_block_ids) | transform_routing_path_block_ids
            )

            return self._get_value_source_resolver(
                routing_path_block_ids=routing_path_block_ids,
                assess_routing_path=True,
            )

        return self._value_source_resolver
