from dataclasses import dataclass
from decimal import Decimal
from typing import Callable, Iterable, Mapping, MutableMapping, TypeAlias

from markupsafe import Markup
from werkzeug.datastructures import ImmutableDict

from app.data_models import ProgressStore
from app.data_models.answer import (
    AnswerValueEscapedTypes,
    AnswerValueTypes,
    escape_answer_value,
)
from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListModel, ListStore
from app.data_models.metadata_proxy import MetadataProxy, NoMetadataException
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.location import InvalidLocationException
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.rules import rule_evaluator

ValueSourceTypes: TypeAlias = None | str | int | Decimal | list
ValueSourceEscapedTypes: TypeAlias = Markup | list[Markup]
IntOrDecimal: TypeAlias = int | Decimal
ResolvedAnswerList: TypeAlias = list[AnswerValueTypes | AnswerValueEscapedTypes | None]


@dataclass
class ValueSourceResolver:
    answer_store: AnswerStore
    list_store: ListStore
    metadata: MetadataProxy | None
    response_metadata: MutableMapping
    schema: QuestionnaireSchema
    location: Location | RelationshipLocation | None
    list_item_id: str | None
    progress_store: ProgressStore
    routing_path_block_ids: Iterable[str] | None = None
    use_default_answer: bool = False
    escape_answer_values: bool = False
    assess_routing_path: bool = True

    def _is_answer_on_path(self, answer_id: str) -> bool:
        if self.routing_path_block_ids:
            block = self.schema.get_block_for_answer_id(answer_id)
            return block is not None and self._is_block_on_path(block["id"])
        return True

    def _is_block_on_path(self, block_id: str) -> bool:
        if block_id in self.schema.repeating_block_ids:
            # repeating blocks aren't on the path, so check the parent list collector
            list_name = self.schema.list_names_by_list_repeating_block[block_id]
            # Type ignore: section and list collector will both exist if the block is repeating
            section: ImmutableDict = self.schema.get_section_for_block_id(block_id)  # type: ignore
            list_collector_block: ImmutableDict = self.schema.get_list_collector_for_list(section, list_name)  # type: ignore
            return list_collector_block["id"] in (self.routing_path_block_ids or [])
        return block_id in (self.routing_path_block_ids or [])

    def _get_answer_value(
        self,
        answer_id: str,
        list_item_id: str | None,
        assess_routing_path: bool | None = None,
    ) -> AnswerValueTypes | None:
        assess_routing_path = (
            assess_routing_path
            if assess_routing_path is not None
            else self.assess_routing_path
        )

        if assess_routing_path and not self._is_answer_on_path(answer_id):
            return None

        if answer := self.answer_store.get_answer(answer_id, list_item_id):
            return answer.value

        if self.use_default_answer and (
            answer := self.schema.get_default_answer(answer_id)
        ):
            return answer.value

    def _resolve_list_item_id_for_value_source(
        self, value_source: Mapping
    ) -> str | None:
        list_item_id: str | None = None

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

    def _resolve_repeating_answers_for_list(
        self, *, answer_id: str, list_name: str
    ) -> ResolvedAnswerList:
        """Return the list of answers in answer store that correspond to the given list name and dynamic/repeating answer_id"""
        answer_values: ResolvedAnswerList = []
        for list_item_id in self.list_store[list_name]:
            answer_value = self._get_answer_value(
                answer_id=answer_id, list_item_id=list_item_id
            )
            if answer_value is not None and self.escape_answer_values:
                answer_values.append(escape_answer_value(answer_value))
            else:
                answer_values.append(answer_value)
        return answer_values

    def _resolve_dynamic_answers(
        self,
        answer_id: str,
    ) -> ResolvedAnswerList | None:
        # Type ignore: block must exist for this function to be called
        question = self.schema.get_block_for_answer_id(answer_id).get("question", {})  # type: ignore
        dynamic_answers = question["dynamic_answers"]
        values = dynamic_answers["values"]
        if values["source"] == "list":
            return self._resolve_repeating_answers_for_list(
                answer_id=answer_id, list_name=values["identifier"]
            )

    def _resolve_repeating_block_answers(self, answer_id: str) -> ResolvedAnswerList:
        # Type ignore: block must exist for this function to be called
        repeating_block: ImmutableDict = self.schema.get_block_for_answer_id(answer_id)  # type: ignore
        list_name = self.schema.list_names_by_list_repeating_block[
            repeating_block["id"]
        ]
        return self._resolve_repeating_answers_for_list(
            answer_id=answer_id, list_name=list_name
        )

    def _resolve_answer_value_source(
        self, value_source: Mapping
    ) -> ValueSourceEscapedTypes | ValueSourceTypes:
        """resolves answer value by first checking if the answer is dynamic whilst not in a repeating section,
        which indicates that it is a repeating answer resolving to a list. Otherwise, retrieve answer value as normal.
        """
        list_item_id = self._resolve_list_item_id_for_value_source(value_source)
        answer_id = value_source["identifier"]

        # if not in a repeating section and the id is for a list of dynamic/repeating block answers, then return the list of values
        if not list_item_id:
            if self.schema.is_answer_dynamic(answer_id):
                return self._resolve_dynamic_answers(answer_id)
            if self.schema.is_answer_for_repeating_block(answer_id):
                return self._resolve_repeating_block_answers(answer_id)

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

    def _resolve_progress_value_source(
        self, value_source: Mapping
    ) -> ValueSourceEscapedTypes | ValueSourceTypes | None:
        identifier = value_source["identifier"]
        selector = value_source["selector"]
        if selector == "section":
            # List item id is set to None here as we do not support checking progress value sources for
            # repeating sections
            return self.progress_store.get_section_or_repeating_blocks_progress_status(
                section_id=identifier, list_item_id=None
            )

        if selector == "block":
            if not self.location:
                raise ValueError("location is required to resolve block progress")

            if self.routing_path_block_ids and not self._is_block_on_path(identifier):
                return None

            # Type ignore: Section id will exist at this point
            section_id_for_block: str = self.schema.get_section_id_for_block_id(identifier)  # type: ignore

            return self.progress_store.get_block_status(
                block_id=identifier,
                section_id=section_id_for_block,
                list_item_id=self.location.list_item_id
                if self.location.section_id == section_id_for_block
                else None,
            )

    def _resolve_list_value_source(self, value_source: Mapping) -> int | str | list:
        identifier = value_source["identifier"]
        list_model: ListModel = self.list_store[identifier]

        if selector := value_source.get("selector"):
            value: str | list | int = getattr(list_model, selector)
            return value

        return list(list_model)

    def _resolve_calculated_summary_value_source(
        self, value_source: Mapping, *, assess_routing_path: bool
    ) -> IntOrDecimal | None:
        """Calculates the value for the 'calculation' used by the provided Calculated Summary.

        The caller is responsible for ensuring the provided Calculated Summary and its answers are on the path,
        or providing routing_path_block_ids when initialising the value source resolver.
        """
        calculated_summary_block: ImmutableDict = self.schema.get_block(value_source["identifier"])  # type: ignore

        if self.routing_path_block_ids and not self._is_block_on_path(
            calculated_summary_block["id"]
        ):
            return None

        calculation = calculated_summary_block["calculation"]
        if calculation.get("answers_to_calculate"):
            operator = self.get_calculation_operator(calculation["calculation_type"])
            list_item_id = self._resolve_list_item_id_for_value_source(value_source)
            values = [
                self._get_answer_value(
                    answer_id=answer_id,
                    list_item_id=list_item_id,
                    assess_routing_path=assess_routing_path,
                )
                for answer_id in calculation["answers_to_calculate"]
            ]
            return operator([value for value in values if value])  # type: ignore

        evaluator = rule_evaluator.RuleEvaluator(
            self.schema,
            self.answer_store,
            self.list_store,
            self.metadata,
            self.response_metadata,
            progress_store=self.progress_store,
            location=self.location,
            routing_path_block_ids=self.routing_path_block_ids,
        )

        return evaluator.evaluate(calculation["operation"])  # type: ignore

    def _resolve_metadata_source(self, value_source: Mapping) -> str | None:
        if not self.metadata:
            raise NoMetadataException
        identifier = value_source["identifier"]
        return self.metadata[identifier]

    def _resolve_location_source(self, value_source: Mapping) -> str | None:
        if value_source.get("identifier") == "list_item_id":
            return self.list_item_id

    def _resolve_response_metadata_source(self, value_source: Mapping) -> str | None:
        return self.response_metadata.get(value_source.get("identifier"))

    @staticmethod
    def get_calculation_operator(
        calculation_type: str,
    ) -> Callable[[Iterable[IntOrDecimal]], IntOrDecimal]:
        if calculation_type == "sum":
            return sum

        raise NotImplementedError(f"Invalid calculation_type: {calculation_type}")

    def resolve(
        self, value_source: Mapping
    ) -> ValueSourceEscapedTypes | ValueSourceTypes:
        source = value_source["source"]

        if source == "calculated_summary":
            return self._resolve_calculated_summary_value_source(
                value_source=value_source, assess_routing_path=True
            )

        resolve_method_mapping = {
            "answers": self._resolve_answer_value_source,
            "list": self._resolve_list_value_source,
            "metadata": self._resolve_metadata_source,
            "location": self._resolve_location_source,
            "response_metadata": self._resolve_response_metadata_source,
            "progress": self._resolve_progress_value_source,
        }

        return resolve_method_mapping[source](value_source)
