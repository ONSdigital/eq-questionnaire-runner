from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Callable, Iterable, Mapping, Optional, Union

from markupsafe import Markup

from app.data_models.answer import AnswerValueTypes, escape_answer_value
from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListModel, ListStore
from app.data_models.metadata_proxy import MetadataProxy, NoMetadataException
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.location import InvalidLocationException
from app.questionnaire.relationship_location import RelationshipLocation

ValueSourceTypes = Union[None, str, int, Decimal, list]
ValueSourceEscapedTypes = Union[
    Markup,
    list[Markup],
]
IntOrDecimal = Union[int, Decimal]


@dataclass
class ValueSourceResolver:
    answer_store: AnswerStore
    list_store: ListStore
    metadata: Optional[MetadataProxy]
    response_metadata: Mapping
    schema: QuestionnaireSchema
    location: Union[None, Location, RelationshipLocation]
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
        self, value_source: Mapping
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
        self, value_source: Mapping
    ) -> Union[ValueSourceEscapedTypes, ValueSourceTypes]:
        list_item_id = self._resolve_list_item_id_for_value_source(value_source)
        answer_id = value_source["identifier"]

        answer_value = self._get_answer_value(
            answer_id=answer_id, list_item_id=list_item_id
        )

        if isinstance(answer_value, Mapping):
            answer_value = (
                answer_value.get(value_source["selector"])
                if "selector" in value_source
                else None
            )

        if answer_value is not None and self.escape_answer_values:
            return escape_answer_value(answer_value)

        return answer_value

    def _resolve_list_value_source(
        self, value_source: Mapping
    ) -> Union[int, str, list]:
        identifier = value_source["identifier"]
        list_model: ListModel = self.list_store[identifier]

        if selector := value_source.get("selector"):
            value: Union[str, list, int] = getattr(list_model, selector)
            return value

        return list(list_model)

    def _resolve_calculated_summary_value_source(
        self, value_source: Mapping
    ) -> IntOrDecimal:
        """Calculates the value for the 'calculation' used by the provided Calculated Summary.

        The caller is responsible for ensuring the provided Calculated Summary and its answers are on the path.
        """
        calculated_summary_block: Mapping[str, Any] = self.schema.get_block(value_source["identifier"])  # type: ignore
        calculation = calculated_summary_block["calculation"]
        operator = self.get_calculation_operator(calculation["calculation_type"])
        list_item_id = self._resolve_list_item_id_for_value_source(value_source)
        values = [
            self._get_answer_value(answer_id=answer_id, list_item_id=list_item_id)
            for answer_id in calculation["answers_to_calculate"]
        ]
        return operator([value for value in values if value])  # type: ignore

    @staticmethod
    def get_calculation_operator(
        calculation_type: str,
    ) -> Callable[[Iterable[IntOrDecimal]], IntOrDecimal]:
        if calculation_type == "sum":
            return sum

        raise NotImplementedError(f"Invalid calculation_type: {calculation_type}")

    def resolve(
        self, value_source: Mapping
    ) -> Union[ValueSourceEscapedTypes, ValueSourceTypes]:
        source = value_source["source"]

        if source == "answers":
            return self._resolve_answer_value_source(value_source)

        if source == "list":
            return self._resolve_list_value_source(value_source)

        if source == "metadata":
            if not self.metadata:
                raise NoMetadataException
            identifier = value_source["identifier"]
            return self.metadata[identifier]

        if source == "location" and value_source.get("identifier") == "list_item_id":
            # This does not use the location object because
            # routes such as individual response does not have the concept of location.
            return self.list_item_id

        if source == "response_metadata":
            return self.response_metadata.get(value_source.get("identifier"))

        if source == "calculated_summary":
            return self._resolve_calculated_summary_value_source(value_source)
