from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Union

from markupsafe import Markup

from app.data_models.answer import (
    AnswerValueEscapedTypes,
    AnswerValueTypes,
    escape_answer_value,
)
from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListModel, ListStore
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.relationship_location import RelationshipLocation

ValueSourceTypes = Union[None, str, int, Decimal, list]
ValueSourceEscapedTypes = Union[
    Markup,
    list[Markup],
]


@dataclass
class ValueSourceResolver:
    answer_store: AnswerStore
    list_store: ListStore
    metadata: dict
    schema: QuestionnaireSchema
    location: Union[Location, RelationshipLocation]
    list_item_id: Optional[str]
    routing_path_block_ids: Optional[list] = None
    use_default_answer: bool = False
    escape_answer_values: bool = False

    def _is_answer_on_path(self, answer_id: str) -> bool:
        if self.routing_path_block_ids:
            block = self.schema.get_block_for_answer_id(answer_id)
            return block is not None and block["id"] in self.routing_path_block_ids

        return True

    def _get_answer_value(
        self, answer_id: str, list_item_id: Optional[str]
    ) -> Optional[AnswerValueTypes]:
        if not self._is_answer_on_path(answer_id):
            return None

        if answer := self.answer_store.get_answer(answer_id, list_item_id):
            return answer.value

        if self.use_default_answer and (
            answer := self.schema.get_default_answer(answer_id)
        ):
            return answer.value

    def _resolve_list_item_id_for_value_source(
        self, value_source: dict
    ) -> Optional[str]:
        list_item_id: Optional[str] = None

        if list_item_selector := value_source.get("list_item_selector"):
            if list_item_selector["source"] == "location":
                list_item_id = getattr(self.location, list_item_selector["id"])

            elif list_item_selector["source"] == "list":
                list_item_id = getattr(
                    self.list_store[list_item_selector["id"]],
                    list_item_selector["id_selector"],
                )

        if list_item_id:
            return list_item_id

        return (
            self.list_item_id
            if self.list_item_id
            and self.schema.is_repeating_answer(value_source["identifier"])
            else None
        )

    def _resolve_answer_value_source(
        self, value_source: dict
    ) -> Union[ValueSourceEscapedTypes, ValueSourceTypes]:
        list_item_id = self._resolve_list_item_id_for_value_source(value_source)
        answer_id = value_source["identifier"]

        answer_value = self._get_answer_value(
            answer_id=answer_id, list_item_id=list_item_id
        )

        if isinstance(answer_value, dict):
            answer_value = (
                answer_value.get(value_source["selector"])
                if "selector" in value_source
                else None
            )

        if answer_value is not None and self.escape_answer_values:
            return escape_answer_value(answer_value)

        return answer_value

    def resolve(
        self, value_source: dict
    ) -> Union[ValueSourceEscapedTypes, ValueSourceTypes]:
        source = value_source["source"]
        identifier = value_source.get("identifier")

        if source == "answers":
            return self._resolve_answer_value_source(value_source)
        if source == "metadata":
            return self.metadata.get(identifier)
        if source == "list":
            list_model: ListModel = self.list_store[identifier]

            if id_selector := value_source.get("id_selector"):
                value: Union[str, list] = getattr(list_model, id_selector)
                return value

            return len(list_model)

        if source == "location" and identifier == "list_item_id":
            # This does not use the location object because
            # routes such as individual response does not have the concept of location.
            return self.list_item_id
