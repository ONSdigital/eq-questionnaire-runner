from copy import deepcopy
from decimal import Decimal
from typing import Callable, List, Mapping, Tuple, Union

from werkzeug.datastructures import ImmutableDict

from app.jinja_filters import (
    format_number,
    format_percentage,
    format_unit,
    get_formatted_currency,
)
from app.questionnaire import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.schema_utils import get_answer_ids_in_block
from app.questionnaire.value_source_resolver import ValueSourceResolver
from app.questionnaire.variants import choose_question_to_display, transform_variants
from app.views.contexts.context import Context
from app.views.contexts.summary.group import Group


class CalculatedSummaryContext(Context):
    def build_groups_for_section(
        self, section: Mapping, return_to_block_id: str, current_location: Location
    ) -> List[Group]:
        routing_path = self._router.routing_path(section["id"])

        return [
            Group(
                group,
                routing_path,
                self._answer_store,
                self._list_store,
                self._metadata,
                self._response_metadata,
                self._schema,
                current_location,
                self._language,
                return_to="calculated-summary",
                return_to_block_id=return_to_block_id,
            ).serialize()
            for group in section["groups"]
        ]

    def build_view_context_for_calculated_summary(
        self, current_location: Location
    ) -> Mapping:
        # type ignores added as block will exist at this point
        block_id: str = current_location.block_id  # type: ignore
        block: ImmutableDict = self._schema.get_block(block_id)  # type: ignore

        calculated_section = self._build_calculated_summary_section(
            block, current_location
        )
        calculation = block["calculation"]

        groups = self.build_groups_for_section(
            calculated_section, block_id, current_location
        )

        formatted_total = self._get_formatted_total(
            groups or [],
            current_location=current_location,
            calculation=ValueSourceResolver.get_calculation_operator(
                calculation["calculation_type"]
            )
            if calculation.get("answers_to_calculate")
            else calculation["operation"],
        )

        collapsible = block.get("collapsible") or False
        block_title = block.get("title")

        return {
            "summary": {
                "groups": groups,
                "answers_are_editable": True,
                "calculated_question": self._get_calculated_question(
                    calculation, formatted_total
                ),
                "title": block_title % dict(total=formatted_total)
                if block_title
                else None,
                "collapsible": collapsible,
                "summary_type": "CalculatedSummary",
            }
        }

    def _build_calculated_summary_section(
        self, rendered_block: ImmutableDict, current_location: Location
    ) -> Mapping:
        """Build up the list of blocks only including blocks / questions / answers which are relevant to the summary"""
        if (block_id := current_location.block_id) and (
            group := self._schema.get_group_for_block_id(block_id)
        ):
            section_id = self._schema.get_section_id_for_block_id(block_id)

            blocks = []
            if rendered_block["calculation"].get("answers_to_calculate"):
                answers_to_calculate = rendered_block["calculation"][
                    "answers_to_calculate"
                ]
            else:
                answers_to_calculate = self._schema.get_calculated_summary_answer_ids(
                    rendered_block
                )

            blocks_to_calculate = [
                self._schema.get_block_for_answer_id(answer_id)
                for answer_id in answers_to_calculate
            ]

            unique_blocks = list(
                {block["id"]: block for block in blocks_to_calculate if block}.values()
            )

            for block in unique_blocks:
                if block and QuestionnaireSchema.is_question_block_type(block["type"]):
                    transformed_block = self._remove_unwanted_questions_answers(
                        block, answers_to_calculate, current_location=current_location
                    )
                    if set(get_answer_ids_in_block(transformed_block)) & set(
                        answers_to_calculate
                    ):
                        blocks.append(transformed_block)

            return {"id": section_id, "groups": [{"id": group["id"], "blocks": blocks}]}

    def _remove_unwanted_questions_answers(
        self, block, answer_ids_to_keep, current_location
    ) -> str:
        """
        Evaluates questions in a block and removes any questions not containing a relevant answer
        """
        transformed_block = transform_variants(
            block,
            self._schema,
            self._metadata,
            self._response_metadata,
            self._answer_store,
            self._list_store,
            current_location=current_location,
        )
        transformed_block = deepcopy(transformed_block)
        transformed_block = QuestionnaireSchema.get_mutable_deepcopy(transformed_block)
        block_question = transformed_block["question"]

        matching_answers = []
        for answer_id in answer_ids_to_keep:
            matching_answers.extend(self._schema.get_answers_by_answer_id(answer_id))

        questions_to_keep = [
            self._schema.parent_id_map[answer["id"]] for answer in matching_answers
        ]

        if block_question["id"] in questions_to_keep:
            answers_to_keep = [
                answer
                for answer in block_question["answers"]
                if answer["id"] in answer_ids_to_keep
            ]
            block_question["answers"] = answers_to_keep

        return transformed_block

    def _get_formatted_total(
        self,
        groups: list,
        current_location: Location,
        calculation: Union[Callable, ImmutableDict],
    ) -> str:
        answer_format, values_to_calculate = self._get_answer_format(
            groups, current_location
        )

        if isinstance(calculation, ImmutableDict):
            evaluate_calculated_summary = RuleEvaluator(
                self._schema,
                self._answer_store,
                self._list_store,
                self._metadata,
                self._response_metadata,
                location=current_location,
            )

            calculated_total: Union[int, float, Decimal] = evaluate_calculated_summary.evaluate(calculation)  # type: ignore
        else:
            calculated_total = calculation(values_to_calculate)

        return self._format_total(answer_format, calculated_total)

    def _get_answer_format(
        self, groups: list, current_location: Location
    ) -> Tuple[Mapping, list]:
        values_to_calculate: list = []
        answer_format: Mapping = {"type": None}
        for group in groups:
            for block in group["blocks"]:
                question = choose_question_to_display(
                    block,
                    self._schema,
                    self._metadata,
                    self._response_metadata,
                    self._answer_store,
                    self._list_store,
                    current_location=current_location,
                )
                for answer in question["answers"]:
                    if not answer_format["type"]:
                        answer_format = {
                            "type": answer["type"],
                            "unit": answer.get("unit"),
                            "unit_length": answer.get("unit_length"),
                            "currency": answer.get("currency"),
                        }
                    answer_value = answer.get("value") or 0
                    values_to_calculate.append(answer_value)

        return answer_format, values_to_calculate

    @staticmethod
    def _format_total(
        answer_format: Mapping[str, str], total: Union[int, float, Decimal]
    ) -> str:
        if answer_format["type"] == "currency":
            return get_formatted_currency(total, answer_format["currency"])

        if answer_format["type"] == "unit":
            return format_unit(
                answer_format["unit"],
                total,
                answer_format["unit_length"],
            )

        if answer_format["type"] == "percentage":
            return format_percentage(total)

        return format_number(total)

    @staticmethod
    def _get_calculated_question(
        calculation_question: ImmutableDict, formatted_total: str
    ) -> Mapping:
        calculation_title = calculation_question["title"]

        return {
            "title": calculation_title,
            "id": "calculated-summary-question",
            "answers": [{"id": "calculated-summary-answer", "value": formatted_total}],
        }
