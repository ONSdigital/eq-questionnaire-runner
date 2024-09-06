from dataclasses import dataclass
from decimal import Decimal
from typing import Callable, Iterable, Mapping, TypeAlias

from markupsafe import Markup
from werkzeug.datastructures import ImmutableDict

from app.data_models.answer import (
    AnswerValueEscapedTypes,
    AnswerValueTypes,
    escape_answer_value,
)
from app.data_models.data_stores import DataStores
from app.data_models.list_store import ListModel
from app.data_models.metadata_proxy import NoMetadataException
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.location import InvalidLocationException, SectionKey
from app.questionnaire.rules import rule_evaluator
from app.utilities.types import LocationType

ValueSourceTypes: TypeAlias = None | str | int | Decimal | list | dict
ValueSourceEscapedTypes: TypeAlias = Markup | list[Markup]
IntOrDecimal: TypeAlias = int | Decimal
ResolvedAnswerList: TypeAlias = list[AnswerValueTypes | AnswerValueEscapedTypes | None]


@dataclass
class ValueSourceResolver:
    data_stores: DataStores
    schema: QuestionnaireSchema
    location: LocationType | None
    list_item_id: str | None
    routing_path_block_ids: Iterable[str] | None = None
    use_default_answer: bool = False
    escape_answer_values: bool = False
    assess_routing_path: bool | None = True

    def _is_answer_on_path(self, answer_id: str) -> bool:
        if self.routing_path_block_ids:
            block = self.schema.get_block_for_answer_id(answer_id)
            return block is not None and self._is_block_on_path(block["id"])
        return True

    def _is_block_on_path(self, block_id: str) -> bool:
        # other usages of this function than _is_answer_on_path don't have this check so require it here
        if not self.routing_path_block_ids:
            return True

        # repeating blocks aren't on the path, so check the parent list collector
        if block_id in self.schema.list_collector_repeating_block_ids:
            return self.schema.parent_id_map[block_id] in self.routing_path_block_ids

        return block_id in self.routing_path_block_ids

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

        if answer := self.data_stores.answer_store.get_answer(answer_id, list_item_id):
            return answer.value

        if self.use_default_answer and (
            answer := self.schema.get_default_answer(answer_id)
        ):
            return answer.value

    def _resolve_list_item_id_for_answer_id(self, answer_id: str) -> str | None:
        """
        If there's a list item id and the answer is repeating, return the list item id to resolve the instance of the answer
        However if the answer is repeating for a different list, return None so that the repeating answer id resolves to a list
        """
        if self.list_item_id and (
            list_name_for_answer := self.schema.get_list_name_for_answer_id(answer_id)
        ):
            # if there is a current list, and it differs to the repeating answer one, return None
            if (
                self.location
                and self.location.list_name
                and self.location.list_name != list_name_for_answer
            ):
                return None
            return self.list_item_id

    def _resolve_list_item_id_for_value_source(
        self, value_source: Mapping
    ) -> str | None:
        if list_item_selector := value_source.get("list_item_selector"):
            if list_item_selector["source"] == "location":
                if not self.location:
                    raise InvalidLocationException(
                        "list_item_selector source location used without location"
                    )
                # Type ignore: the identifier is a string, same below
                return getattr(self.location, list_item_selector["identifier"])  # type: ignore

            if list_item_selector["source"] == "list":
                return getattr(  # type: ignore
                    self.data_stores.list_store[list_item_selector["identifier"]],
                    list_item_selector["selector"],
                )

        if value_source["source"] == "supplementary_data":
            return (
                self.list_item_id
                if self.data_stores.supplementary_data_store.is_data_repeating(
                    value_source["identifier"]
                )
                else None
            )

        if value_source["source"] == "answers":
            return self._resolve_list_item_id_for_answer_id(value_source["identifier"])

    def _resolve_repeating_answers_for_list(
        self, *, answer_id: str, list_name: str
    ) -> ResolvedAnswerList:
        """Return the list of answers in answer store that correspond to the given list name and dynamic/repeating answer_id"""
        answer_values: ResolvedAnswerList = []
        for list_item_id in self.data_stores.list_store[list_name]:
            answer_value = self._get_answer_value(
                answer_id=answer_id, list_item_id=list_item_id
            )
            if answer_value is not None:
                answer_values.append(
                    escape_answer_value(answer_value)
                    if self.escape_answer_values
                    else answer_value
                )
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

    def _resolve_list_repeating_block_answers(
        self, answer_id: str
    ) -> ResolvedAnswerList:
        # Type ignore: block must exist for this function to be called
        repeating_block: ImmutableDict = self.schema.get_block_for_answer_id(answer_id)  # type: ignore
        list_name = self.schema.list_names_by_list_repeating_block_id[
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
            if self.schema.is_answer_in_list_collector_repeating_block(answer_id):
                return self._resolve_list_repeating_block_answers(answer_id)

        answer_value = self._get_answer_value(
            answer_id=answer_id,
            list_item_id=list_item_id,
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
            return self.data_stores.progress_store.get_section_status(
                SectionKey(identifier)
            )

        if selector == "block":
            if not self.location:
                raise ValueError("location is required to resolve block progress")

            if not self._is_block_on_path(identifier):
                return None

            # Type ignore: Section id will exist at this point
            section_id_for_block: str = self.schema.get_section_id_for_block_id(identifier)  # type: ignore

            return self.data_stores.progress_store.get_block_status(
                block_id=identifier,
                section_key=SectionKey(
                    section_id=section_id_for_block,
                    list_item_id=(
                        self.location.list_item_id
                        if self.location.section_id == section_id_for_block
                        else None
                    ),
                ),
            )

    def _resolve_list_value_source(self, value_source: Mapping) -> int | str | list:
        identifier = value_source["identifier"]
        list_model: ListModel = self.data_stores.list_store[identifier]

        if selector := value_source.get("selector"):
            value: str | list | int = getattr(list_model, selector)
            return value

        return list(list_model)

    def _resolve_summary_with_calculation(
        self, value_source: Mapping, *, assess_routing_path: bool
    ) -> IntOrDecimal | None:
        """Calculates the value for the 'calculation' used by the provided Calculated or Grand Calculated Summary.

        The caller is responsible for ensuring the provided summary and its components are on the path
        or providing routing_path_block_ids when initialising the value source resolver.
        """
        summary_block: ImmutableDict = self.schema.get_block(value_source["identifier"])  # type: ignore
        if not self._is_block_on_path(summary_block["id"]):
            return None

        calculation = summary_block["calculation"]
        # the calculation object for the old type of calculated summary block may contain answers_to_calculate instead of operation
        if calculation.get("answers_to_calculate"):
            operator = self.get_calculation_operator(calculation["calculation_type"])
            values = [
                self._get_answer_value(
                    answer_id=answer_id,
                    list_item_id=self._resolve_list_item_id_for_answer_id(answer_id),
                    assess_routing_path=assess_routing_path,
                )
                for answer_id in calculation["answers_to_calculate"]
            ]
            return operator([value for value in values if value])  # type: ignore

        evaluator = rule_evaluator.RuleEvaluator(
            self.schema,
            data_stores=self.data_stores,
            location=self.location,
            routing_path_block_ids=self.routing_path_block_ids,
        )

        return evaluator.evaluate(calculation["operation"])  # type: ignore

    def _resolve_metadata_source(self, value_source: Mapping) -> str | None:
        if not self.data_stores.metadata:
            raise NoMetadataException
        identifier = value_source["identifier"]
        return self.data_stores.metadata[identifier]

    def _resolve_location_source(self, value_source: Mapping) -> str | None:
        if value_source.get("identifier") == "list_item_id":
            return self.list_item_id

    def _resolve_response_metadata_source(self, value_source: Mapping) -> str | None:
        return self.data_stores.response_metadata.get(value_source.get("identifier"))

    def resolve_list(self, value_source_list: list[Mapping]) -> list[ValueSourceTypes]:
        values: list[ValueSourceTypes] = []
        for value_source in value_source_list:
            value = self.resolve(value_source)
            if isinstance(value, list):
                values.extend(value)
            else:
                values.append(value)
        return values

    def _resolve_supplementary_data_source(
        self, value_source: Mapping
    ) -> ValueSourceTypes:
        list_item_id = self._resolve_list_item_id_for_value_source(value_source)

        return self.data_stores.supplementary_data_store.get_data(
            identifier=value_source["identifier"],
            selectors=value_source.get("selectors"),
            list_item_id=list_item_id,
        )

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

        if source in {"calculated_summary", "grand_calculated_summary"}:
            return self._resolve_summary_with_calculation(
                value_source=value_source, assess_routing_path=True
            )
        resolve_method_mapping = {
            "answers": self._resolve_answer_value_source,
            "list": self._resolve_list_value_source,
            "metadata": self._resolve_metadata_source,
            "location": self._resolve_location_source,
            "response_metadata": self._resolve_response_metadata_source,
            "progress": self._resolve_progress_value_source,
            "supplementary_data": self._resolve_supplementary_data_source,
        }

        return resolve_method_mapping[source](value_source)
