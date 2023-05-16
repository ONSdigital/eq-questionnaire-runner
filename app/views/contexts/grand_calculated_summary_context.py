from typing import Any, Iterable, Mapping

from werkzeug.datastructures import ImmutableDict

from app.questionnaire.questionnaire_schema import (
    get_calculated_summary_answer_ids,
    get_grand_calculated_summary_block_ids,
)
from app.views.contexts.calculated_summary_context import CalculatedSummaryContext
from app.views.contexts.summary.group import Group


class GrandCalculatedSummaryContext(CalculatedSummaryContext):
    def _build_grand_calculated_summary_section(self, rendered_block: Mapping) -> dict:
        """
        Build list of calculated summary blocks that the grand calculated summary will be adding up
        """
        # Type ignore: the block, group and section will all exist at this point
        block_id: str = self.current_location.block_id  # type: ignore
        calculated_summary_group: ImmutableDict = self._schema.get_group_for_block_id(block_id)  # type: ignore
        section_id: str = self._schema.get_section_id_for_block_id(block_id)  # type: ignore

        calculated_summary_ids = get_grand_calculated_summary_block_ids(rendered_block)
        blocks_to_calculate = [
            self._schema.get_block(block_id) for block_id in calculated_summary_ids
        ]

        return {
            "id": section_id,
            "groups": [
                {"id": calculated_summary_group["id"], "blocks": blocks_to_calculate}
            ],
        }

    def _blocks_on_routing_path(self, calculated_summary_ids: list[str]) -> list[str]:
        """
        Find all blocks on the routing path for each of the calculated summaries
        """
        # Type ignore: each block must have a section id
        section_ids: set[str] = {self._schema.get_section_id_for_block_id(block_id) for block_id in calculated_summary_ids}  # type: ignore
        # find any sections involved in the grand calculated summary (but only if they have started, to avoid evaluating the path if not necessary)
        started_sections = [
            key for key, _ in self._progress_store.started_section_keys(section_ids)
        ]
        routing_path_block_ids: list[str] = []

        for section_id in started_sections:
            if section_id == self.current_location.section_id:
                routing_path_block_ids.extend(self.routing_path_block_ids)
            else:
                routing_path_block_ids.extend(
                    # repeating calculated summaries are not supported at the moment, so no list item is needed
                    self._router.routing_path(section_id).block_ids
                )

        return routing_path_block_ids

    def build_groups_for_section(
        self,
        section: Mapping,
        return_to_block_id: str,
        routing_path_block_ids: Iterable[str],
    ) -> list[Mapping[str, Group]]:
        return [
            Group(
                group_schema=group,
                routing_path_block_ids=routing_path_block_ids,
                answer_store=self._answer_store,
                list_store=self._list_store,
                metadata=self._metadata,
                response_metadata=self._response_metadata,
                schema=self._schema,
                location=self.current_location,
                language=self._language,
                progress_store=self._progress_store,
                return_to="grand-calculated-summary",
                return_to_block_id=return_to_block_id,
                summary_type="GrandCalculatedSummary",
            ).serialize()
            for group in section["groups"]
        ]

    def build_view_context_for_grand_calculated_summary(self) -> dict[str, dict]:
        """
        Build summary section with formatted total and change links for each calculated summary
        """
        # Type ignore: Block will exist at this point
        block_id: str = self.current_location.block_id  # type: ignore
        block: ImmutableDict = self._schema.get_block(block_id)  # type: ignore

        calculation = block["calculation"]
        calculated_summary_ids = get_grand_calculated_summary_block_ids(block)
        routing_path_block_ids = self._blocks_on_routing_path(calculated_summary_ids)

        calculated_section = self._build_grand_calculated_summary_section(block)

        groups = self.build_groups_for_section(
            calculated_section, block_id, routing_path_block_ids
        )
        total = self._get_evaluated_total(
            calculation["operation"], routing_path_block_ids
        )

        answer_format = self._get_summary_format(groups)
        formatted_total = self._format_total(answer_format, total)

        return self._build_formatted_summary(
            block=block,
            groups=groups,
            calculation=calculation,
            formatted_total=formatted_total,
            summary_type="GrandCalculatedSummary",
        )

    @staticmethod
    def _get_summary_format(groups: list[Mapping]) -> dict:
        """
        Get the format of the final value from the first calculated summary.
        Validator ensures that they are all the same
        """
        first_calculated_summary = groups[0]["blocks"][0]["calculated_summary"]
        first_answer = first_calculated_summary["answers"][0]
        return {
            "type": first_answer["type"],
            "unit": first_answer["unit"],
            "unit_length": first_answer["unit_length"],
            "currency": first_answer["currency"],
        }
