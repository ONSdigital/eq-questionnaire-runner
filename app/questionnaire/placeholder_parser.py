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
        list_item_id: str | None = None,
        location: Location | RelationshipLocation | None = None,
        progress_store: ProgressStore | None = None,
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
        self._routing_paths: dict = {}
        self._sections_to_ignore: list = []

    def __call__(
        self, placeholder_list: Sequence[Mapping]
    ) -> MutableMapping[str, Union[ValueSourceEscapedTypes, ValueSourceTypes]]:
        placeholder_list = QuestionnaireSchema.get_mutable_deepcopy(placeholder_list)

        if routing_path_block_ids_map := self._get_routing_path_block_ids(
            self._sections_to_ignore
        ):
            self._sections_to_ignore.extend(iter(routing_path_block_ids_map.keys()))

            routing_path_block_ids = flatten_block_ids_map(routing_path_block_ids_map)
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

    def _get_routing_path_block_ids(
        self, sections_to_ignore: list | None = None
    ) -> dict[str, list[str]]:
        if self._location and self._path_finder:
            return get_block_ids_for_calculated_summary_dependencies(
                schema=self._schema,
                location=self._location,
                path_finder=self._path_finder,
                sections_to_ignore=sections_to_ignore,
            )
        return {}


def get_block_ids_for_calculated_summary_dependencies(
    schema: QuestionnaireSchema,
    location: Location | RelationshipLocation,
    path_finder: "PathFinder",
    sections_to_ignore: list | None = None,
) -> dict[str, list[str]]:
    # Type ignore: Added to this method as the block will exist at this point
    blocks_id_by_section = {}

    sections_to_ignore = sections_to_ignore or []
    dependent_sections = schema.calculated_summary_section_dependencies_by_block.get(  # type: ignore
        location.section_id
    )
    dependents: set = set()
    if block_id := location.block_id:
        if schema.get_block(block_id).get("type") not in [  # type: ignore
            "ListEditQuestion",
            "ListAddQuestion",
            "ListRemoveQuestion",
            "UnrelatedQuestion",
            "PrimaryPersonListAddOrEditQuestion",
        ]:
            dependents = dependent_sections[block_id]  # type: ignore

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

        keys = [(section, location.list_item_id), (section, None)]
        for key in keys:
            if key in path_finder.progress_store.started_section_keys():
                path = path_finder.routing_path(*key)
                blocks_id_by_section[section] = path.block_ids

    return blocks_id_by_section


def flatten_block_ids_map(routing_path_block_ids_map: dict[str, list[str]]) -> set[str]:
    return {x for v in routing_path_block_ids_map.values() for x in v}
