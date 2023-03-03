from decimal import Decimal
from typing import (
    TYPE_CHECKING,
    Any,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Union,
)

from app.data_models import ProgressStore
from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import Location, QuestionnaireSchema
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
        metadata: Optional[MetadataProxy],
        response_metadata: Mapping,
        schema: QuestionnaireSchema,
        renderer: "PlaceholderRenderer",
        list_item_id: Optional[str] = None,
        location: Union[Location, RelationshipLocation, None] = None,
        progress_store: Optional[ProgressStore] = None,
        path_finder: Optional["PathFinder"] = None,
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
        self._path_finder = path_finder

        self._value_source_resolver = self._get_value_source_resolver()
        self._routing_paths = {}

    def _get_block_id_for_calculated_summary_dependencies(
        self, placeholder_list: Sequence[Mapping]
    ):
        return self._schema.get_values_for_key(placeholder_list, "source")

    def __call__(
        self, placeholder_list: Sequence[Mapping]
    ) -> MutableMapping[str, Union[ValueSourceEscapedTypes, ValueSourceTypes]]:
        placeholder_list = QuestionnaireSchema.get_mutable_deepcopy(placeholder_list)

        if routing_path_block_ids := self._get_routing_path_block_ids():
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
        self, routing_path_block_ids: list[str] | None = None
    ):
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
            progress_store=self._progress_store,
            path_finder=self._path_finder,
        )

    def _parse_placeholder(
        self, placeholder: Mapping
    ) -> Union[ValueSourceEscapedTypes, ValueSourceTypes, TransformedValueTypes]:
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

    def _get_routing_path_block_ids(self) -> list[str]:
        return self._get_block_ids_for_calculated_summary_dependencies()

    def _get_block_ids_for_calculated_summary_dependencies(self):
        if not self._path_finder:
            raise ValueError("PathFinder not set")

        if not self._location:
            return []

        if block_id := self._location.block_id:
            dependent_sections = (
                self._schema.calculated_summary_section_dependencies_by_block.get(
                    self._location.section_id
                )[block_id]
            )
        else:
            dependencies_by_blocks = (
                self._schema.calculated_summary_section_dependencies_by_block.get(
                    self._location.section_id
                ).values()
            )
            dependent_sections = {
                section
                for dependents in dependencies_by_blocks
                if dependents
                for section in dependents
            }

        block_dependencies: list = []

        for dependent_section in dependent_sections:
            if (
                dependent_section,
                None,
            ) in self._path_finder.progress_store.started_section_keys():
                key = dependent_section, None

                if not (path := self._routing_paths.get(key)):
                    path = self._path_finder.routing_path(
                        section_id=key[0], list_item_id=key[1]
                    )
                    self._routing_paths[key] = path.block_ids

                block_dependencies.extend(path.block_ids)

        return block_dependencies
