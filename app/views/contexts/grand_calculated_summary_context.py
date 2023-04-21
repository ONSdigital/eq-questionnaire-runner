from app.views.contexts.calculated_summary_context import CalculatedSummaryContext
from app.questionnaire.questionnaire_schema import (
    get_grand_calculated_summary_block_ids,
    get_calculated_summary_answer_ids,
)
from typing import Any, Mapping, Iterable
from app.views.contexts.summary.calculated_summary import CalculatedSummary
from werkzeug.datastructures import ImmutableDict


# maybe shouldn't inherit from CalculatedSummaryContext?
class GrandCalculatedSummaryContext(CalculatedSummaryContext):
    @staticmethod
    def build_calculated_summary_block(
        calculated_summary_block_id: str,
        block_id: str,
        title: str | None,
        number: int | None,
        formatted_total: Mapping,
    ) -> Mapping[str, Any]:
        calculated_summary = CalculatedSummary(
            title=title,
            block_id=block_id,
            return_to="grand_calculated_summary",
            return_to_block_id=calculated_summary_block_id,
            answers=[formatted_total],
        ).serialize()
        return {
            "id": block_id,
            "title": title,
            "number": number,
            "calculated_summary": calculated_summary,
        }

    def _build_grand_calculated_summary_section(
        self,
        rendered_block: Mapping,
        answer_format: Mapping,
        routing_path_block_ids: Iterable[str],
    ) -> list[dict]:
        """Build up the list of blocks only including blocks / questions / answers which are relevant to the summary"""
        # Type ignore: the block, group and section
        block_id: str = self.current_location.block_id  # type: ignore
        calculated_summary_group: ImmutableDict = self._schema.get_group_for_block_id(block_id)  # type: ignore
        section_id: str = self._schema.get_section_id_for_block_id(block_id)  # type: ignore

        # for grand summaries, the calculated_summary_ids will be a list of block ids, each being of a calculated summary
        calculated_summary_ids = get_grand_calculated_summary_block_ids(rendered_block)
        blocks_to_calculate = []

        for calculated_summary_id in calculated_summary_ids:
            # Type ignore: safe to assume the block exists
            calculated_summary_block: ImmutableDict = self._schema.get_block(calculated_summary_id)  # type: ignore
            calculated_summary_total = self._get_evaluated_total(
                calculated_summary_block["calculation"]["operation"],
                routing_path_block_ids,
            )
            formatted_answer = {
                "id": calculated_summary_block["id"],
                "label": calculated_summary_block["calculation"]["title"],
                "value": calculated_summary_total,
                **answer_format,
                "link": calculated_summary_block["id"],
            }

            blocks_to_calculate.append(
                self.build_calculated_summary_block(
                    block_id,
                    calculated_summary_id,
                    calculated_summary_block.get("title"),
                    calculated_summary_block.get("number"),
                    formatted_answer,
                )
            )

        # in calculated summaries, the blocks would be altered and irrelevant questions removed, in this case, its different
        # the answers don't need to be rendered, so it should be fine to just include the blocks for each calc sum
        # (then those remove children if needed)

        return [
            {
                "id": section_id,
                "title": calculated_summary_group.get("title"),
                "blocks": blocks_to_calculate,
            }
        ]

    def build_view_context_for_grand_calculated_summary(
        self,
    ) -> dict[str, dict[str, Any]]:
        """
        Calculated summaries will always be within a single section
        But grand calculated summaries may include calculated summaries from multiple sections
        """
        block_id: str = self.current_location.block_id  # type: ignore
        block: ImmutableDict = self._schema.get_block(block_id)  # type: ignore
        section: ImmutableDict = self._schema.get_section_for_block_id(block_id)  # type: ignore

        calculation = block["calculation"]
        collapsible = block.get("collapsible") or False
        block_title = block["title"]

        # Type ignore: validator ensures the block exists
        calculated_summary_ids = get_grand_calculated_summary_block_ids(block)
        routing_path_block_ids = [
            block["id"] for group in section["groups"] for block in group["blocks"]
        ]

        answer_format: dict = {}
        for calculated_summary_id in calculated_summary_ids:
            section: ImmutableDict = self._schema.get_section_for_block_id(calculated_summary_id)  # type: ignore
            if not answer_format.get("type"):
                calculated_summary_block: ImmutableDict = self._schema.get_block(calculated_summary_id)  # type: ignore
                answer_id = get_calculated_summary_answer_ids(calculated_summary_block)[
                    0
                ]
                answer = self._schema.get_answers_by_answer_id(answer_id)[0]
                answer_format = {
                    "type": answer["type"].lower(),
                    "unit": answer.get("unit"),
                    "unit_length": answer.get("unit_length"),
                    "currency": answer.get("currency"),
                }

            for group in section["groups"]:
                routing_path_block_ids.extend(
                    [block["id"] for block in group["blocks"]]
                )

        calculated_section = self._build_grand_calculated_summary_section(
            block, answer_format, routing_path_block_ids
        )

        total = self._get_evaluated_total(
            calculation["operation"], routing_path_block_ids
        )
        formatted_total = self._format_total(answer_format, total)

        return {
            "summary": {
                "groups": calculated_section,
                "answers_are_editable": True,
                "calculated_question": self._get_calculated_question(
                    calculation, formatted_total
                ),
                "title": block_title % {"total": formatted_total},
                "collapsible": collapsible,
                "summary_type": "CalculatedSummary",
            }
        }
