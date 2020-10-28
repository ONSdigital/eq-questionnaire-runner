from typing import Dict, List, Mapping, Sequence, Union

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListModel
from app.questionnaire import QuestionnaireSchema
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
        placeholder_list = QuestionnaireSchema.get_mutable_deepcopy(placeholder_list)
        for placeholder in placeholder_list:
            if placeholder["placeholder"] not in self._placeholder_map:
                self._placeholder_map[
                    placeholder["placeholder"]
                ] = self._parse_placeholder(placeholder)
        return self._placeholder_map

    def _resolve_value_source(self, value_source):
        if value_source["source"] == "answers":
            return self._resolve_answer_value(value_source)
        if value_source["source"] == "metadata":
            return self._resolve_metadata_value(value_source["identifier"])
        if value_source["source"] == "list":
            id_selector = value_source.get("id_selector")
            list_model: ListModel = self._list_store[value_source["identifier"]]

            if id_selector:
                return getattr(list_model, id_selector)

            return len(list_model)
        if (
            value_source["source"] == "location"
            and value_source["identifier"] == "list_item_id"
        ):
            return self._list_item_id

    def _resolve_answer_value(self, value_source):
        list_item_id = self._get_list_item_id_from_value_source(value_source)

        if isinstance(value_source["identifier"], (list, tuple)):
            return [
                self._answer_store.get_escaped_answer_value(
                    each_identifier, list_item_id
                )
                for each_identifier in value_source["identifier"]
            ]
        answer = self._answer_store.get_escaped_answer_value(
            value_source["identifier"], list_item_id
        )
        return (
            answer.get(value_source["selector"])
            if "selector" in value_source
            else answer
        )

    def _resolve_metadata_value(self, identifier):
        if isinstance(identifier, (list, tuple)):
            return [
                self._metadata.get(each_identifier) for each_identifier in identifier
            ]
        return self._metadata.get(identifier)

    def _parse_placeholder(self, placeholder: Mapping) -> Mapping:
        try:
            return self._parse_transforms(placeholder["transforms"])
        except KeyError:
            return self._resolve_value_source(placeholder["value"])

    def _parse_transforms(self, transform_list: Sequence[Mapping]):
        transformed_value = None

        for transform in transform_list:
            transform_args: Dict[str, Union[None, str, List[str]]] = {}
            for arg_key, arg_value in transform["arguments"].items():
                if not isinstance(arg_value, dict):
                    transform_args[arg_key] = arg_value
                elif "value" in arg_value:
                    transform_args[arg_key] = arg_value["value"]
                elif arg_value["source"] == "previous_transform":
                    transform_args[arg_key] = transformed_value
                else:
                    transform_args[arg_key] = self._resolve_value_source(arg_value)

            transformed_value = getattr(self._transformer, transform["transform"])(
                **transform_args
            )

        return transformed_value

    def _get_list_item_id_from_value_source(self, value_source):
        list_item_selector = value_source.get("list_item_selector")
        if list_item_selector:
            if list_item_selector["source"] == "location":
                return getattr(self._location, list_item_selector["id"])
            if list_item_selector["source"] == "list":
                return getattr(
                    self._list_store[list_item_selector["id"]],
                    list_item_selector["id_selector"],
                )
        return self._list_item_id
