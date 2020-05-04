from typing import Mapping, Sequence, Union, Dict, List

from jinja2 import escape, Markup

from app.data_model.answer_store import AnswerStore
from app.questionnaire.placeholder_transforms import PlaceholderTransforms


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

    def __call__(self, placeholder_list: Sequence[Mapping]) -> Mapping:
        for placeholder in placeholder_list:
            if placeholder["placeholder"] not in self._placeholder_map:
                self._placeholder_map[
                    placeholder["placeholder"]
                ] = self._parse_placeholder(placeholder)
        return self._placeholder_map

    def _lookup_answer(
        self, answer_id: str, list_item_id: str = None
    ) -> Union[Markup, Sequence[Markup], None]:
        answer = self._answer_store.get_answer(answer_id, list_item_id)
        if answer:
            if isinstance(answer.value, list):
                return [escape(value) for value in answer.value]
            return escape(answer.value)
        return None

    def _resolve_value_source(self, value_source, list_item_id):
        if value_source["source"] == "answers":
            return self._resolve_answer_value(value_source["identifier"], list_item_id)
        if value_source["source"] == "metadata":
            return self._resolve_metadata_value(value_source["identifier"])
        if value_source["source"] == "list":
            return len(self._list_store[value_source["identifier"]].items)

    def _resolve_answer_value(self, identifier, list_item_id):
        if isinstance(identifier, list):
            return [
                self._lookup_answer(each_identifier, list_item_id)
                for each_identifier in identifier
            ]
        return self._lookup_answer(identifier, list_item_id)

    def _resolve_metadata_value(self, identifier):
        if isinstance(identifier, list):
            return [
                self._metadata.get(each_identifier) for each_identifier in identifier
            ]
        return self._metadata.get(identifier)

    def _parse_placeholder(self, placeholder: Mapping) -> Mapping:
        try:
            return self._parse_transforms(placeholder["transforms"])
        except KeyError:
            return self._resolve_value_source(placeholder["value"], self._list_item_id)

    def _parse_transforms(self, transform_list: Sequence[Mapping]):
        transformed_value = None

        for transform in transform_list:
            list_item_id = self._get_list_item_id(
                transform.get("arguments", {})
                .get("list_to_concatenate", {})
                .get("list_item_selector", {})
                .get("id")
            )
            transform_args: Dict[str, Union[None, str, List[str]]] = {}
            for arg_key, arg_value in transform["arguments"].items():
                if not isinstance(arg_value, dict):
                    transform_args[arg_key] = arg_value
                elif "value" in arg_value:
                    transform_args[arg_key] = arg_value["value"]
                elif arg_value["source"] == "previous_transform":
                    transform_args[arg_key] = transformed_value
                else:
                    transform_args[arg_key] = self._resolve_value_source(
                        arg_value, list_item_id
                    )

            transformed_value = getattr(self._transformer, transform["transform"])(
                **transform_args
            )

        return transformed_value

    def _get_list_item_id(self, list_item_selector=None):
        if list_item_selector:
            return getattr(self._location, list_item_selector)
        return self._list_item_id
