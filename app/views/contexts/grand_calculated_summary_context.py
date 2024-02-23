from typing import Iterable, Mapping

from werkzeug.datastructures import ImmutableDict

from app.questionnaire.location import SectionKey
from app.questionnaire.questionnaire_schema import (
    get_calculated_summary_ids_for_grand_calculated_summary,
)
from app.questionnaire.return_location import ReturnLocation
from app.views.contexts.calculated_summary_context import CalculatedSummaryContext
from app.views.contexts.summary.group import Group


class GrandCalculatedSummaryContext(CalculatedSummaryContext):
    def _build_grand_calculated_summary_section(self) -> dict[str, str | list]:
        """
        Build list of calculated summary blocks that the grand calculated summary will be adding up
        """
        # Type ignore: the block, group and section will all exist at this point
        calculated_summary_group: ImmutableDict = self._schema.get_group_for_block_id(
            self.current_location.block_id  # type: ignore
        )

        calculated_summary_ids = (
            get_calculated_summary_ids_for_grand_calculated_summary(self.rendered_block)
        )
        blocks_to_calculate = [
            self._schema.get_block(block_id) for block_id in calculated_summary_ids
        ]

        return {
            "id": self.current_location.section_id,
            "groups": [
                {"id": calculated_summary_group["id"], "blocks": blocks_to_calculate}
            ],
        }

    def _blocks_on_routing_path(
        self, calculated_summary_ids: Iterable[str]
    ) -> list[str]:
        """
        Find all blocks on the routing path for each of the calculated summaries
        """
        # Type ignore: each block must have a section id
        section_ids: set[str] = {
            self._schema.get_section_id_for_block_id(block_id)  # type: ignore
            for block_id in calculated_summary_ids
        }
        # find any sections involved in the grand calculated summary (but only if they have started, to avoid evaluating the path if not necessary)
        started_sections = [
            key
            for key, _ in self._data_stores.progress_store.started_section_keys(
                section_ids
            )
        ]
        routing_path_block_ids: list[str] = []

        for section_id in started_sections:
            if section_id == self.current_location.section_id:
                routing_path_block_ids.extend(self.routing_path_block_ids)
            else:
                routing_path_block_ids.extend(
                    # repeating calculated summaries are not supported at the moment, so no list item is needed
                    self._router.routing_path(SectionKey(section_id)).block_ids
                )

        return routing_path_block_ids

    def build_groups_for_section(
        self,
        *,
        section: Mapping,
        routing_path_block_ids: Iterable[str],
    ) -> list[Mapping]:
        return [
            Group(
                group_schema=group,
                routing_path_block_ids=routing_path_block_ids,
                data_stores=self._data_stores,
                schema=self._schema,
                location=self.current_location,
                language=self._language,
                summary_type="GrandCalculatedSummary",
                return_location=ReturnLocation(
                    return_to="grand-calculated-summary",
                    return_to_block_id=self.current_location.block_id,
                    return_to_list_item_id=self.current_location.list_item_id,
                ),
            ).serialize()
            for group in section["groups"]
        ]

    def build_view_context(self) -> dict[str, dict]:
        """
        Build summary section with formatted total and change links for each calculated summary
        """
        calculation = self.rendered_block["calculation"]
        calculated_summary_ids = (
            get_calculated_summary_ids_for_grand_calculated_summary(self.rendered_block)
        )
        routing_path_block_ids = self._blocks_on_routing_path(calculated_summary_ids)

        calculated_section = self._build_grand_calculated_summary_section()

        groups = self.build_groups_for_section(
            section=calculated_section,
            routing_path_block_ids=routing_path_block_ids,
        )
        total = self._get_evaluated_total(
            calculation=calculation["operation"],
            routing_path_block_ids=routing_path_block_ids,
        )

        # validator ensures all calculated summaries are of the same type, so the first can be used for the format
        answer_format = self._schema.get_answer_format_for_calculated_summary(
            calculated_summary_ids[0]
        )
        answer_format["decimal_places"] = (
            self._schema.get_decimal_limit_from_calculated_summaries(
                calculated_summary_ids
            )
        )
        formatted_total = self._format_total(answer_format=answer_format, total=total)

        return self._build_formatted_summary(
            groups=groups,
            calculation=calculation,
            formatted_total=formatted_total,
        )
