from typing import Iterator, Mapping

from flask import url_for

from app.questionnaire import QuestionnaireSchema
from .context import Context
from .list_context import ListContext
from .summary import Group


class SectionSummaryContext(Context):
    def __init__(
        self, language, schema, answer_store, list_store, progress_store, metadata
    ):
        super().__init__(
            language, schema, answer_store, list_store, progress_store, metadata
        )
        self.list_context = ListContext(
            self._language,
            self._schema,
            self._answer_store,
            self._list_store,
            self._progress_store,
            self._metadata,
        )

    def __call__(self, current_location):
        section_summary_context = self._section_summary_context(current_location)
        section_summary_context["summary"].update(
            self._build_groups_for_location(current_location)
        )
        return section_summary_context

    def _build_groups_for_location(self, location):
        """
        Build a groups context for a particular location.

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

    def _section_summary_context(self, current_location):
        try:
            block = self._schema.get_block(current_location.block_id)
            collapsible = block.get("collapsible", False)
        except AttributeError:
            collapsible = False

        return {
            "summary": {
                "title": self._title_for_location(current_location),
                "summary_type": "SectionSummary",
                "answers_are_editable": True,
                "collapsible": collapsible,
            }
        }

    def _title_for_location(self, location):
        if location.block_id:
            title = self._schema.get_block(location.block_id).get("title")
        else:
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
    ) -> Iterator[Mapping]:
        list_collector_block = self._schema.get_list_collectors_for_section(
            section, for_list=summary["for_list"]
        )[0]

        add_link = self._add_link(
            summary, current_location, section, list_collector_block
        )

        rendered_list_context = self.list_context(
            list_collector_block["summary"],
            for_list=list_collector_block["for_list"],
            return_to=current_location.block_id,
            edit_block=list_collector_block["edit_block"],
            remove_block=list_collector_block["remove_block"],
        )

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
            **rendered_list_context,
        }

    def _add_link(self, summary, current_location, section, list_collector_block):
        routing_path = self._router.routing_path(
            section["id"], current_location.list_item_id
        )

        add_link = url_for(
            "questionnaire.block",
            list_name=summary["for_list"],
            block_id=list_collector_block["add_block"]["id"],
            return_to=current_location.block_id,
        )

        if list_collector_block["id"] not in routing_path:
            driving_question_block = QuestionnaireSchema.get_driving_question_for_list(
                section, summary["for_list"]
            )

            if driving_question_block:
                add_link = url_for(
                    "questionnaire.block",
                    block_id=driving_question_block["id"],
                    return_to=current_location.block_id,
                )
        return add_link
