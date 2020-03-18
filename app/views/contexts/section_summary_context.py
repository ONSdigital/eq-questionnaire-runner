from typing import Mapping

from flask import url_for

from app.questionnaire import QuestionnaireSchema
from .context import Context
from .list_context import ListContext
from .summary import Group


class SectionSummaryContext(Context):
    def __call__(self, current_location):
        try:
            block = self._schema.get_block(current_location.block_id)
            collapsible = block.get("collapsible", False)
        except AttributeError:
            collapsible = False

        summary = self._build_summary(current_location)
        return {
            "summary": {
                "title": self._title_for_location(current_location),
                "summary_type": "SectionSummary",
                "answers_are_editable": True,
                "collapsible": collapsible,
                **summary,
            }
        }

    def _build_summary(self, location):
        """
        Build a summary context for a particular location.

        Does not support generating multiple sections at a time (i.e. passing no list_item_id for repeating section).
        """
        section = self._schema.get_section(location.section_id)
        if section.get("summary"):
            return {
                "custom_summary": list(
                    self._custom_summary_elements(section["summary"], location, section)
                )
            }

        routing_path = self._router.routing_path(
            location.section_id, location.list_item_id
        )

        return {
            "groups": [
                Group(
                    group,
                    routing_path,
                    self._answer_store,
                    self._list_store,
                    self._metadata,
                    self._schema,
                    location,
                    self._language,
                ).serialize()
                for group in section["groups"]
            ]
        }

    def _title_for_location(self, location):
        title = None
        if location.block_id:
            title = self._schema.get_block(location.block_id).get("title")
        if not title:
            title = self._schema.get_section(location.section_id).get("title")

        if location.list_item_id:
            repeating_title = self._schema.get_repeating_title_for_section(
                location.section_id
            )
            if repeating_title:
                title = self._placeholder_renderer.render_placeholder(
                    repeating_title, location.list_item_id
                )
        return title

    def _custom_summary_elements(self, section_summary, current_location, section):
        for summary_element in section_summary:
            if summary_element["type"] == "List":
                yield self._list_summary_element(
                    summary_element, current_location, section
                )

    def _list_summary_element(
        self, summary: Mapping, current_location, section: Mapping
    ) -> Mapping:
        list_context = ListContext(
            self._language,
            self._schema,
            self._answer_store,
            self._list_store,
            self._progress_store,
            self._metadata,
        )

        list_collector_blocks = self._get_blocks_on_path(
            section["id"],
            current_location.list_item_id,
            for_list=summary["for_list"],
            block_type="ListCollector",
        )

        if list_collector_blocks:
            list_summary = list_collector_blocks[0]["summary"]
            edit_block_id = list_collector_blocks[0]["edit_block"]["id"]
            remove_block_id = list_collector_blocks[0]["remove_block"]["id"]
        else:
            list_collector_blocks = self._get_blocks_on_path(
                section["id"],
                current_location.list_item_id,
                summary["for_list"],
                "ListCollectorDrivingQuestion",
            )

            list_collector_block = self._schema.get_list_collectors_for_list(
                section, for_list=summary["for_list"]
            )

            list_summary = list_collector_block[0]["summary"]
            edit_block_id = list_collector_block[0]["edit_block"]
            remove_block_id = list_collector_block[0]["remove_block"]["id"]

        add_link = self._add_link(summary, current_location, list_collector_blocks[0])

        rendered_summary = self._placeholder_renderer.render(
            summary, current_location.list_item_id
        )

        return {
            "title": rendered_summary["title"],
            "type": rendered_summary["type"],
            "add_link": add_link,
            "add_link_text": rendered_summary["add_link_text"],
            "empty_list_text": rendered_summary["empty_list_text"],
            "list_name": rendered_summary["for_list"],
            **list_context(
                list_summary,
                for_list=list_collector_blocks[0]["for_list"],
                return_to=current_location.block_id,
                edit_block_id=edit_block_id,
                remove_block_id=remove_block_id,
            ),
        }

    def _get_blocks_on_path(self, section_id, list_item_id, for_list, block_type):
        return [
            block
            for block in [
                self._schema.get_block(block_id)
                for block_id in self._router.routing_path(section_id, list_item_id)
            ]
            if block["type"] == block_type and block["for_list"] == for_list
        ]

    @staticmethod
    def _add_link(summary, current_location, list_collector_block):
        if list_collector_block["type"] == "ListCollector":
            return url_for(
                "questionnaire.block",
                list_name=summary["for_list"],
                block_id=list_collector_block["add_block"]["id"],
                return_to=current_location.block_id,
            )

        return url_for(
            "questionnaire.block",
            block_id=list_collector_block["id"],
            return_to=current_location.block_id,
        )
