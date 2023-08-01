from typing import Mapping

from flask import url_for

from app.views.contexts.summary.list_collector_base_block import ListCollectorBaseBlock


class ListCollectorBlock(ListCollectorBaseBlock):
    # pylint: disable=too-many-locals
    def list_summary_element(self, summary: Mapping) -> dict:
        list_collector_block = None
        (
            edit_block_id,
            remove_block_id,
            primary_person_edit_block_id,
            related_answers,
            item_label,
            item_anchor,
        ) = (None, None, None, None, None, None)
        list_model = self._list_store[summary["for_list"]]

        add_link = self._add_link(summary, list_collector_block)

        list_collector_blocks_on_path = self._list_collector_block_on_path(
            summary["for_list"]
        )

        list_collector_block = self._list_collector_block(
            summary["for_list"], list_collector_blocks_on_path
        )

        rendered_summary = self._placeholder_renderer.render(
            data_to_render=summary, list_item_id=self._location.list_item_id
        )

        section_id = self._section["id"]
        if list_collector_blocks_on_path:
            edit_block_id = list_collector_block["edit_block"]["id"]
            remove_block_id = list_collector_block["remove_block"]["id"]
            add_link = self._add_link(summary, list_collector_block)
            repeating_blocks = list_collector_block.get("repeating_blocks", [])
            related_answers = self._get_related_answer_blocks_by_list_item_id(
                list_model=list_model, repeating_blocks=repeating_blocks
            )
            item_anchor = self._schema.get_item_anchor(section_id, list_model.name)
            item_label = self._schema.get_item_label(section_id, list_model.name)

        if len(list_model) == 1 and list_model.primary_person:
            if primary_person_block := self._schema.get_list_collector_for_list(
                self._section, for_list=summary["for_list"], primary=True
            ):
                primary_person_edit_block_id = edit_block_id = primary_person_block[
                    "add_or_edit_block"
                ]["id"]

        list_summary_context = self.list_context(
            list_collector_block["summary"],
            for_list=list_collector_block["for_list"],
            section_id=self._location.section_id,
            has_repeating_blocks=bool(list_collector_block.get("repeating_blocks")),
            return_to=self._return_to,
            edit_block_id=edit_block_id,
            remove_block_id=remove_block_id,
            primary_person_edit_block_id=primary_person_edit_block_id,
        )

        return {
            "title": rendered_summary["title"],
            "type": rendered_summary["type"],
            "add_link": add_link,
            "add_link_text": rendered_summary["add_link_text"],
            "empty_list_text": rendered_summary.get("empty_list_text"),
            "list_name": rendered_summary["for_list"],
            "related_answers": related_answers,
            "item_label": item_label,
            "item_anchor": item_anchor,
            **list_summary_context,
        }

    def _add_link(
        self,
        summary: Mapping,
        list_collector_block: Mapping | None,
    ) -> str | None:
        if list_collector_block:
            return url_for(
                "questionnaire.block",
                list_name=summary["for_list"],
                block_id=list_collector_block["add_block"]["id"],
                return_to=self._return_to,
            )

        if driving_question_block := self._schema.get_driving_question_for_list(
            self._section, summary["for_list"]
        ):
            return url_for(
                "questionnaire.block",
                block_id=driving_question_block["id"],
                return_to=self._return_to,
            )
