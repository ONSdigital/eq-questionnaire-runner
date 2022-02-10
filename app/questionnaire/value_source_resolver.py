from dataclasses import dataclass
from decimal import Decimal
from typing import Mapping, Optional, Union

from markupsafe import Markup

from app.data_models.answer import AnswerValueTypes, escape_answer_value
from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListModel, ListStore
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.location import InvalidLocationException
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
    metadata: Mapping
    response_metadata: Mapping
    schema: QuestionnaireSchema
    location: Union[None, Location, RelationshipLocation]
    list_item_id: Optional[str]
    use_default_answer: bool = False
    escape_answer_values: bool = False

    def _get_answer_value(
        self, answer_id: str, list_item_id: Optional[str]
    ) -> Optional[AnswerValueTypes]:

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
                if not self.location:
                    raise InvalidLocationException(
                        "list_item_selector source location used without location"
                    )

                list_item_id = getattr(self.location, list_item_selector["identifier"])

            elif list_item_selector["source"] == "list":
                list_item_id = getattr(
                    self.list_store[list_item_selector["identifier"]],
                    list_item_selector["selector"],
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

    def _resolve_list_value_source(self, value_source: dict) -> Union[int, str, list]:
        identifier = value_source["identifier"]
        list_model: ListModel = self.list_store[identifier]

        if selector := value_source.get("selector"):
            value: Union[str, list, int] = getattr(list_model, selector)
            return value

        return list(list_model)

    def resolve(
        self, value_source: dict
    ) -> Union[ValueSourceEscapedTypes, ValueSourceTypes]:
        source = value_source["source"]

        if source == "answers":
            return self._resolve_answer_value_source(value_source)

        if source == "list":
            return self._resolve_list_value_source(value_source)

        if source == "metadata":
            return self.metadata.get(value_source.get("identifier"))

        if source == "location" and value_source.get("identifier") == "list_item_id":
            # This does not use the location object because
            # routes such as individual response does not have the concept of location.
            return self.list_item_id

        if source == "response_metadata":
            return self.response_metadata.get(value_source.get("identifier"))
