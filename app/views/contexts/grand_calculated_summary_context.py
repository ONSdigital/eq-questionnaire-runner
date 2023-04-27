from typing import Any, Mapping

from werkzeug.datastructures import ImmutableDict

from app.questionnaire.questionnaire_schema import (
    get_calculated_summary_answer_ids,
    get_grand_calculated_summary_block_ids,
)
from app.views.contexts.calculated_summary_context import CalculatedSummaryContext


class GrandCalculatedSummaryContext(CalculatedSummaryContext):
    def _build_grand_calculated_summary_section(self, rendered_block: Mapping) -> dict:
        """Build up the list of blocks only including blocks / questions / answers which are relevant to the summary"""
        # Type ignore: the block, group and section will all exist at this point
        block_id: str = self.current_location.block_id  # type: ignore
        calculated_summary_group: ImmutableDict = self._schema.get_group_for_block_id(block_id)  # type: ignore
        section_id: str = self._schema.get_section_id_for_block_id(block_id)  # type: ignore

        # for grand summaries, the calculated_summary_ids will be a list of block ids, each being of a calculated summary
        calculated_summary_ids = get_grand_calculated_summary_block_ids(rendered_block)
        blocks_to_calculate = [
            self._schema.get_block(block_id) for block_id in calculated_summary_ids
        ]

        # this currently includes calculated summaries and answers that are not on the path
        # TODO Fix

        return {
            "id": section_id,
            "groups": [
                {"id": calculated_summary_group["id"], "blocks": blocks_to_calculate}
            ],
        }

    def build_view_context_for_grand_calculated_summary(
        self,
    ) -> dict[str, dict[str, Any]]:
        """
        Calculated summaries will always be within a single section
        But grand calculated summaries may include calculated summaries from multiple sections
        """
        block_id: str = self.current_location.block_id  # type: ignore
        block: ImmutableDict = self._schema.get_block(block_id)  # type: ignore

        calculation = block["calculation"]
        collapsible = block.get("collapsible") or False
        block_title = block["title"]

        calculated_summary_ids = get_grand_calculated_summary_block_ids(block)
        # TODO exclude if not on path
        routing_path_block_ids = [
            block["id"]
            for calculated_summary_id in calculated_summary_ids
            # Type ignore: section must exist at this time
            for group in self._schema.get_section_for_block_id(calculated_summary_id)["groups"]  # type: ignore
            for block in group["blocks"]
        ]

        answer_format = self._get_summary_format(calculated_summary_ids)
        calculated_section = self._build_grand_calculated_summary_section(block)

        groups = self.build_groups_for_section(
            calculated_section, block_id, routing_path_block_ids, answer_format
        )

        total = self._get_evaluated_total(
            calculation["operation"], routing_path_block_ids
        )
        formatted_total = self._format_total(answer_format, total)

        return {
            "summary": {
                "groups": groups,
                "answers_are_editable": True,
                "calculated_question": self._get_calculated_question(
                    calculation, formatted_total
                ),
                "title": block_title % {"total": formatted_total},
                "collapsible": collapsible,
                "summary_type": "CalculatedSummary",
            }
        }

    def _get_summary_format(self, calculated_summary_ids: list[str]) -> dict:
        """
        Validator ensures that the format of every answer making up the grand calculated summary will be the same
        so taking the format of the first question will suffice
        """
        # Type ignore: validator ensures the grand calculated summary has at least one calculated summary
        first_calculated_summary: ImmutableDict = self._schema.get_block(calculated_summary_ids[0])  # type: ignore
        first_answer_id = get_calculated_summary_answer_ids(first_calculated_summary)[0]
        first_answer = self._schema.get_answers_by_answer_id(first_answer_id)[0]
        return {
            "type": first_answer["type"].lower(),
            "unit": first_answer.get("unit"),
            "unit_length": first_answer.get("unit_length"),
            "currency": first_answer.get("currency"),
        }
