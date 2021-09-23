from decimal import Decimal
from typing import Any, Mapping, Optional, Sequence, Union

from werkzeug.datastructures import ImmutableDict

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.placeholder_transforms import PlaceholderTransforms
from app.questionnaire.value_source_resolver import (
    ValueSourceEscapedTypes,
    ValueSourceResolver,
    ValueSourceTypes,
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
        metadata: ImmutableDict,
        schema: QuestionnaireSchema,
        list_item_id: Optional[str] = None,
        location: Location = None,
    ):

        self._answer_store = answer_store
        self._list_store = list_store
        self._metadata = metadata
        self._schema = schema
        self._list_item_id = list_item_id
        self._location = location
        self._transformer = PlaceholderTransforms(language)
        self._placeholder_map: dict[
            str, Union[ValueSourceEscapedTypes, ValueSourceTypes, None]
        ] = {}

        self._value_source_resolver = ValueSourceResolver(
            answer_store=self._answer_store,
            list_store=self._list_store,
            metadata=self._metadata,
            schema=self._schema,
            location=self._location,
            list_item_id=self._list_item_id,
            escape_answer_values=True,
        )

    def __call__(
        self, placeholder_list: Sequence[Mapping]
    ) -> dict[str, Union[ValueSourceEscapedTypes, ValueSourceTypes]]:
        placeholder_list = QuestionnaireSchema.get_mutable_deepcopy(placeholder_list)
        for placeholder in placeholder_list:
            if placeholder["placeholder"] not in self._placeholder_map:
                self._placeholder_map[
                    placeholder["placeholder"]
                ] = self._parse_placeholder(placeholder)
        return self._placeholder_map

    def _parse_placeholder(
        self, placeholder: Mapping
    ) -> Union[ValueSourceEscapedTypes, ValueSourceTypes]:
        try:
            return self._parse_transforms(placeholder["transforms"])
        except KeyError:
            return self._value_source_resolver.resolve(placeholder["value"])

    def _parse_transforms(
        self, transform_list: Sequence[Mapping]
    ) -> Optional[ValueSourceTypes]:
        transformed_value: Union[
            list[ValueSourceTypes],
            ValueSourceEscapedTypes,
            ValueSourceTypes,
            TransformedValueTypes,
        ] = None

        for transform in transform_list:
            transform_args: dict[str, Any] = {}

            for arg_key, arg_value in transform["arguments"].items():
                if isinstance(arg_value, list):
                    transformed_value = self._resolve_value_source_list(arg_value)
                elif isinstance(arg_value, dict):
                    if "value" in arg_value:
                        transformed_value = arg_value["value"]
                    elif arg_value["source"] == "previous_transform":
                        transformed_value = transformed_value
                    else:
                        transformed_value = self._value_source_resolver.resolve(
                            arg_value
                        )
                else:
                    transformed_value = arg_value

                transform_args[arg_key] = transformed_value

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
