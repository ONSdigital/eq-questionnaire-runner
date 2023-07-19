from typing import Any, Mapping

from app.views.contexts.summary.list_collector_base_block import ListCollectorBaseBlock


class ListCollectorContentBlock(ListCollectorBaseBlock):
    # pylint: disable=too-many-locals
    def list_summary_element(self, summary: Mapping[str, Any]) -> dict[str, Any]:
        related_answers = None

        item_label = None

        current_list = self._list_store[summary["for_list"]]

        list_collector_blocks_on_path = self._list_collector_block_on_path(
            summary["for_list"]
        )

        list_collector_block = self._list_collector_block(
            summary["for_list"], list_collector_blocks_on_path
        )

        rendered_summary = self._placeholder_renderer.render(
            data_to_render=summary, list_item_id=self._location.list_item_id
        )

        if list_collector_blocks_on_path:
            repeating_blocks = list_collector_block.get("repeating_blocks", [])
            related_answers = self._get_related_answer_blocks_by_list_item_id(
                list_model=current_list, repeating_blocks=repeating_blocks
            )
            item_label = self._schema.get_item_label(
                self._section["id"], current_list.name
            )

        list_summary_context = self.list_context(
            list_collector_block["summary"],
            for_list=list_collector_block["for_list"],
            section_id=self._location.section_id,
            has_repeating_blocks=bool(list_collector_block.get("repeating_blocks")),
            return_to="section-summary",
        )

        return {
            "title": rendered_summary["title"],
            "type": rendered_summary["type"],
            "empty_list_text": rendered_summary.get("empty_list_text"),
            "list_name": rendered_summary["for_list"],
            "related_answers": related_answers,
            "item_label": item_label,
            **list_summary_context,
        }
