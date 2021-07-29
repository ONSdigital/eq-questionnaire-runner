from typing import Any, Dict, Mapping, Optional, Sequence

from app.data_models.answer import AnswerValueTypes
from app.data_models.answer_store import AnswerStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.placeholder_transforms import PlaceholderTransforms
from app.questionnaire.value_source_resolver import (
    ValueSourceResolver,
    ValueSourceTypes,
)


class PlaceholderParser:
    """
    Parses placeholder statements from a schema dict and returns a map of their
    final values
    """

    def __init__(
        self,
        language,
        schema=None,
        answer_store=None,
        metadata=None,
        list_item_id=None,
        location=None,
        list_store=None,
    ):

        self._schema = schema
        self._answer_store = answer_store or AnswerStore()
        self._metadata = metadata
        self._list_item_id = list_item_id
        self._list_store = list_store
        self._location = location
        self._transformer = PlaceholderTransforms(language)
        self._placeholder_map = {}

        self._value_source_resolver = ValueSourceResolver(
            answer_store=self._answer_store,
            list_store=self._list_store,
            metadata=self._metadata,
            schema=self._schema,
            location=self._location,
            list_item_id=self._list_item_id,
            escape_answer_values=True,
        )

    def __call__(self, placeholder_list: Sequence[Mapping]) -> Mapping:
        placeholder_list = QuestionnaireSchema.get_mutable_deepcopy(placeholder_list)
        for placeholder in placeholder_list:
            if placeholder["placeholder"] not in self._placeholder_map:
                self._placeholder_map[
                    placeholder["placeholder"]
                ] = self._parse_placeholder(placeholder)
        return self._placeholder_map

    def _parse_placeholder(self, placeholder: Mapping) -> Any:
        try:
            return self._parse_transforms(placeholder["transforms"])
        except KeyError:
            return self._value_source_resolver.resolve(placeholder["value"])

    def _parse_transforms(self, transform_list: Sequence[Mapping]):
        transformed_value = None

        for transform in transform_list:
            transform_args: Dict[str, Optional[AnswerValueTypes]] = {}

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
    ) -> Optional[ValueSourceTypes]:
        values = []
        for value_source in value_source_list:
            value = self._value_source_resolver.resolve(value_source)
            if isinstance(value, list):
                values.extend(value)
            else:
                values.append(value)
        return values
