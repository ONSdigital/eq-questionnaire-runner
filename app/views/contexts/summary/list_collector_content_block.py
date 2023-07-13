from typing import Any, Mapping

from werkzeug.datastructures import ImmutableDict

from app.views.contexts.summary.list_collector_base_block import ListCollectorBaseBlock


class ListCollectorContentBlock(ListCollectorBaseBlock):
    # pylint: disable=too-many-locals
    def list_summary_element(self, summary: Mapping[str, Any]) -> dict[str, Any]:
        related_answers = None

        current_list = self._list_store[summary["for_list"]]

        list_collector_blocks = list(
            self._schema.get_list_collectors_for_list(
                self._section, for_list=summary["for_list"]
            )
        )

        list_collector_blocks_on_path = [
            list_collector_block
            for list_collector_block in list_collector_blocks
            if list_collector_block["id"] in self._routing_path_block_ids
        ]

        list_collector_block = (
            list_collector_blocks_on_path[0]
            if list_collector_blocks_on_path
            else list_collector_blocks[0]
        )

        rendered_summary = self._placeholder_renderer.render(
            data_to_render=summary, list_item_id=self._location.list_item_id
        )

        if list_collector_blocks_on_path:
            repeating_blocks = list_collector_block.get("repeating_blocks", [])
            related_answers = self._get_related_answers(current_list, repeating_blocks)

        list_summary_context = self.list_context(
            list_collector_block["summary"],
            for_list=list_collector_block["for_list"],
            section_id=self._location.section_id,
            has_repeating_blocks=bool(list_collector_block.get("repeating_blocks")),
            return_to="section-summary",
            content_definition=ImmutableDict({}),
        )

        return {
            "title": rendered_summary["title"],
            "type": rendered_summary["type"],
            "empty_list_text": None,
            "list_name": rendered_summary["for_list"],
            "related_answers": related_answers,
            **list_summary_context,
        }