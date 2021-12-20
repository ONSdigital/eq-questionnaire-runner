from copy import deepcopy

from app.jinja_filters import (
    format_number,
    format_percentage,
    format_unit,
    get_formatted_currency,
)
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.schema_utils import (
    choose_question_to_display,
    get_answer_ids_in_block,
    transform_variants,
)
from app.views.contexts.context import Context
from app.views.contexts.summary.group import Group


class CalculatedSummaryContext(Context):
    def build_groups_for_section(self, section):
        routing_path = self._router.routing_path(section["id"])

        location = Location(section["id"])

        return [
            Group(
                group,
                routing_path,
                self._answer_store,
                self._list_store,
                self._metadata,
                self._response_metadata,
                self._schema,
                location,
                self._language,
                return_to="final-summary",
            ).serialize()
            for group in section["groups"]
        ]

    def build_view_context_for_calculated_summary(self, current_location):
        block = self._schema.get_block(current_location.block_id)

        calculated_section = self._build_calculated_summary_section(
            block, current_location
        )

        groups = self.build_groups_for_section(calculated_section)

        formatted_total = self._get_formatted_total(
            groups or [], current_location=current_location
        )

        context = {
            "summary": {
                "groups": groups,
                "answers_are_editable": True,
                "calculated_question": self._get_calculated_question(
                    block["calculation"], formatted_total
                ),
                "title": block.get("title") % dict(total=formatted_total),
                "collapsible": block.get("collapsible", False),
                "summary_type": "CalculatedSummary",
            }
        }

        return context

    def _build_calculated_summary_section(self, rendered_block, current_location):
        """Build up the list of blocks only including blocks / questions / answers which are relevant to the summary"""
        section_id = self._schema.get_section_id_for_block_id(current_location.block_id)
        group = self._schema.get_group_for_block_id(current_location.block_id)
        blocks = []
        answers_to_calculate = rendered_block["calculation"]["answers_to_calculate"]
        blocks_to_calculate = [
            self._schema.get_block_for_answer_id(answer_id)
            for answer_id in answers_to_calculate
        ]
        unique_blocks = list(
            {block["id"]: block for block in blocks_to_calculate}.values()
        )

        for block in unique_blocks:
            if QuestionnaireSchema.is_question_block_type(block["type"]):
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
    ):
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

    def _get_formatted_total(self, groups, current_location):
        calculated_total = 0
        answer_format = {"type": None}
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
                    calculated_total += answer_value

        if answer_format["type"] == "currency":
            return get_formatted_currency(calculated_total, answer_format["currency"])

        if answer_format["type"] == "unit":
            return format_unit(
                answer_format["unit"], calculated_total, answer_format["unit_length"]
            )

        if answer_format["type"] == "percentage":
            return format_percentage(calculated_total)

        return format_number(calculated_total)

    @staticmethod
    def _get_calculated_question(calculation_question, formatted_total):
        calculation_title = calculation_question.get("title")

        return {
            "title": calculation_title,
            "id": "calculated-summary-question",
            "answers": [{"id": "calculated-summary-answer", "value": formatted_total}],
        }
