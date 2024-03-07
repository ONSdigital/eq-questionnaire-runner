from functools import cached_property
from typing import Callable, Iterable, Mapping, Tuple

from werkzeug.datastructures import ImmutableDict

from app.data_models.data_stores import DataStores
from app.jinja_filters import format_number, format_percentage, format_unit
from app.questionnaire.questionnaire_schema import (
    QuestionnaireSchema,
    get_calculated_summary_answer_ids,
)
from app.questionnaire.return_location import ReturnLocation
from app.questionnaire.routing_path import RoutingPath
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.schema_utils import get_answer_ids_in_block
from app.questionnaire.value_source_resolver import ValueSourceResolver
from app.questionnaire.variants import choose_question_to_display, transform_variants
from app.utilities.decimal_places import get_formatted_currency
from app.utilities.strings import pascal_case_to_hyphenated_lowercase
from app.utilities.types import LocationType
from app.views.contexts.context import Context
from app.views.contexts.summary.calculated_summary_block import NumericType
from app.views.contexts.summary.group import Group


class CalculatedSummaryContext(Context):
    def __init__(
        self,
        language: str,
        schema: QuestionnaireSchema,
        data_stores: DataStores,
        routing_path: RoutingPath,
        current_location: LocationType,
        return_location: ReturnLocation,
    ) -> None:
        super().__init__(
            language,
            schema,
            data_stores,
        )
        self._data_stores = data_stores
        self.routing_path_block_ids = routing_path.block_ids
        self.current_location = current_location
        self.return_location = return_location

    @cached_property
    def rendered_block(self) -> dict:
        # Type ignore block is guaranteed to exist at this point
        block_id: str = self.current_location.block_id  # type: ignore
        block: ImmutableDict = self._schema.get_block(block_id)  # type: ignore

        return self._placeholder_renderer.render(
            data_to_render=block, list_item_id=self.current_location.list_item_id
        )

    def build_groups_for_section(
        self,
        *,
        section: Mapping,
        routing_path_block_ids: Iterable[str],
    ) -> list[Mapping]:
        """
        If the calculated summary is being edited from a grand calculated summary
        the details of the grand calculated summary to return to needs to be passed down to the calculated summary answer links
        """
        return_to = "calculated-summary"
        # Type ignore: safe to assume block_id is not None
        return_to_block_id: str = self.current_location.block_id  # type: ignore
        if self.return_location.return_to == "grand-calculated-summary":
            return_to_block_id += f",{self.return_location.return_to_block_id}"
            return_to += ",grand-calculated-summary"
        return [
            Group(
                group_schema=group,
                routing_path_block_ids=routing_path_block_ids,
                schema=self._schema,
                data_stores=self._data_stores,
                location=self.current_location,
                language=self._language,
                summary_type="CalculatedSummary",
                return_location=ReturnLocation(
                    return_to=return_to,
                    return_to_block_id=return_to_block_id,
                    return_to_list_item_id=self.return_location.return_to_list_item_id,
                    return_to_answer_id=(
                        self.return_location.return_to_answer_id
                        if self.return_location.return_to == "grand-calculated-summary"
                        else None
                    ),
                ),
            ).serialize()
            for group in section["groups"]
        ]

    def build_view_context(self) -> dict[str, dict]:
        calculated_section: dict = self._build_calculated_summary_section(
            self.rendered_block
        )
        calculation = self.rendered_block["calculation"]

        groups = self.build_groups_for_section(
            section=calculated_section,
            routing_path_block_ids=self.routing_path_block_ids,
        )

        formatted_total = self._get_formatted_total(
            groups=groups or [],
            calculation=(
                ValueSourceResolver.get_calculation_operator(
                    calculation["calculation_type"]
                )
                if calculation.get("answers_to_calculate")
                else calculation["operation"]
            ),
        )

        return self._build_formatted_summary(
            groups=groups, calculation=calculation, formatted_total=formatted_total
        )

    def _build_formatted_summary(
        self,
        *,
        groups: Iterable[Mapping],
        calculation: Mapping,
        formatted_total: str,
    ) -> dict[str, dict]:
        collapsible = self.rendered_block.get("collapsible") or False
        block_title = self.rendered_block["title"]

        sections = [{"id": self.current_location.section_id, "groups": groups}]

        return {
            "summary": {
                "sections": sections,
                "answers_are_editable": True,
                "calculated_question": self._get_calculated_question(
                    calculation_question=calculation,
                    formatted_total=formatted_total,
                ),
                "title": block_title % {"total": formatted_total},
                "collapsible": collapsible,
                "summary_type": self.rendered_block["type"],
            }
        }

    def _build_calculated_summary_section(self, rendered_block: Mapping) -> dict:
        """Build up the list of blocks only including blocks / questions / answers which are relevant to the summary"""
        # type ignores added as block will exist at this point
        block_id: str = self.current_location.block_id  # type: ignore
        group: ImmutableDict = self._schema.get_group_for_block_id(block_id)  # type: ignore
        # type ignores it is not valid to not have a section at this point
        section_id: str = self._schema.get_section_id_for_block_id(block_id)  # type: ignore

        blocks = []
        if rendered_block["calculation"].get("answers_to_calculate"):
            answers_to_calculate = rendered_block["calculation"]["answers_to_calculate"]
        else:
            answers_to_calculate = get_calculated_summary_answer_ids(rendered_block)

        blocks_to_calculate: list[ImmutableDict] = [
            # Type ignore: the answer blocks will always exist at this point
            self._schema.get_block_for_answer_id(answer_id)  # type: ignore
            for answer_id in answers_to_calculate
        ]

        unique_blocks = list(
            {block["id"]: block for block in blocks_to_calculate}.values()
        )

        for block in unique_blocks:
            if QuestionnaireSchema.is_question_block_type(block["type"]):
                transformed_block = self._remove_unwanted_questions_answers(
                    block, answers_to_calculate
                )
                if set(get_answer_ids_in_block(transformed_block)) & set(
                    answers_to_calculate
                ):
                    blocks.append(transformed_block)

        return {"id": section_id, "groups": [{"id": group["id"], "blocks": blocks}]}

    def _remove_unwanted_questions_answers(
        self, block: ImmutableDict, answer_ids_to_keep: Iterable[str]
    ) -> dict:
        """
        Evaluates questions in a block and removes any questions not containing a relevant answer
        """
        block_to_transform: ImmutableDict = transform_variants(
            block,
            self._schema,
            self._data_stores,
            self.current_location,
        )
        transformed_block: dict = QuestionnaireSchema.get_mutable_deepcopy(
            block_to_transform
        )
        block_question = transformed_block["question"]

        matching_answers = []
        for answer_id in answer_ids_to_keep:
            matching_answers.extend(self._schema.get_answers_by_answer_id(answer_id))

        questions_to_keep = [
            self._schema.parent_id_map[answer["id"]] for answer in matching_answers
        ]

        if block_question["id"] in questions_to_keep:
            if answers := block_question.get("answers"):
                answers_to_keep = [
                    answer for answer in answers if answer["id"] in answer_ids_to_keep
                ]
                block_question["answers"] = answers_to_keep
            if dynamic_answers := block_question.get("dynamic_answers"):
                dynamic_answers_to_keep = [
                    answer
                    for answer in dynamic_answers["answers"]
                    if answer["id"] in answer_ids_to_keep
                ]
                block_question["dynamic_answers"]["answers"] = dynamic_answers_to_keep

        return transformed_block

    def _get_evaluated_total(
        self,
        *,
        calculation: Mapping,
        routing_path_block_ids: Iterable[str],
    ) -> NumericType:
        """
        For a calculation in the new style and the list of involved block ids (possibly across sections) evaluate the total
        """
        evaluate_calculated_summary = RuleEvaluator(
            data_stores=self._data_stores,
            schema=self._schema,
            routing_path_block_ids=routing_path_block_ids,
            location=self.current_location,
        )
        # Type ignore: in the case of a calculated summation it will always be a numeric type
        calculated_total: NumericType = evaluate_calculated_summary.evaluate(calculation)  # type: ignore
        return calculated_total

    def _get_formatted_total(
        self, groups: list, calculation: Callable | ImmutableDict
    ) -> str:
        answer_format, values_to_calculate = self._get_answer_format(groups)

        if isinstance(calculation, Mapping):
            calculated_total = self._get_evaluated_total(
                calculation=calculation,
                routing_path_block_ids=self.routing_path_block_ids,
            )
        else:
            calculated_total = calculation(values_to_calculate)

        return self._format_total(answer_format=answer_format, total=calculated_total)

    def _get_answer_format(self, groups: Iterable[Mapping]) -> Tuple[dict, list]:
        values_to_calculate: list = []
        answer_format: dict = {"type": None}
        decimal_limits: list[int] = []
        for group in groups:
            for block in group["blocks"]:
                question = choose_question_to_display(
                    block,
                    self._schema,
                    self._data_stores,
                    current_location=self.current_location,
                )
                for answer in question["answers"]:
                    if not answer_format["type"]:
                        answer_format = {
                            "type": answer["type"],
                            "unit": answer.get("unit"),
                            "unit_length": answer.get("unit_length"),
                            "currency": answer.get("currency"),
                        }

                    if (decimal_places := answer.get("decimal_places")) is not None:
                        decimal_limits.append(decimal_places)

                    answer_value = answer.get("value") or 0
                    values_to_calculate.append(answer_value)
        answer_format["decimal_places"] = max(decimal_limits, default=None)
        return answer_format, values_to_calculate

    @staticmethod
    def _format_total(
        *,
        answer_format: Mapping,
        total: NumericType,
    ) -> str:
        if answer_format["type"] == "currency":
            return get_formatted_currency(
                value=total,
                currency=answer_format["currency"],
                decimal_limit=answer_format.get("decimal_places"),
            )

        if answer_format["type"] == "unit":
            return format_unit(
                answer_format["unit"],
                total,
                answer_format["unit_length"],
            )

        if answer_format["type"] == "percentage":
            return format_percentage(total)

        return format_number(total)

    def _get_calculated_question(
        self, *, calculation_question: Mapping, formatted_total: str
    ) -> dict:
        calculation_title = calculation_question["title"]
        block_type = pascal_case_to_hyphenated_lowercase(self.rendered_block["type"])

        return {
            "title": calculation_title,
            "id": f"{block_type}-question",
            "answers": [{"id": f"{block_type}-answer", "value": formatted_total}],
        }
