from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Union

from app.data_models.answer import AnswerValueTypes
from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListModel, ListStore
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.relationship_location import RelationshipLocation

ValueSourceTypes = Union[None, str, int, Decimal, list]


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
            and self.schema.answer_should_have_list_item_id(value_source["identifier"])
            else None
        )

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

    def _resolve_answer_value(self, value_source: dict) -> ValueSourceTypes:
        list_item_id = self._resolve_list_item_id_for_value_source(value_source)
        answer_id = value_source["identifier"]

        answer_value = self._get_answer_value(
            answer_id=answer_id, list_item_id=list_item_id
        )

        if isinstance(answer_value, dict):
            return (
                answer_value.get(value_source["selector"])
                if "selector" in value_source
                else None
            )

        return answer_value

    def _resolve_value_source_list(
        self, value_source_list: list[dict]
    ) -> Optional[ValueSourceTypes]:
        values = []
        for value_source in value_source_list:
            value = self._resolve_value_source_dict(value_source)
            if isinstance(value, list):
                values.extend(value)
            else:
                values.append(value)
        return values

    def _resolve_value_source_dict(self, value_source: dict) -> ValueSourceTypes:
        source = value_source["source"]
        identifier = value_source.get("identifier")

        if source == "answers":
            return self._resolve_answer_value(value_source)
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

    def resolve(self, value_source: Union[list, dict]) -> ValueSourceTypes:
        if isinstance(value_source, list):
            return self._resolve_value_source_list(value_source)

        return self._resolve_value_source_dict(value_source)
