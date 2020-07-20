from typing import Mapping

import immutables
from flask import url_for

from app.helpers.template_helper import safe_content
from app.questionnaire import QuestionnaireSchema
from .context import Context
from .list_context import ListContext
from .summary import Group


class SectionSummaryContext(Context):
    def __call__(self, current_location):
        summary = self._build_summary(current_location)
        title_for_location = self._title_for_location(current_location)
        title = (
            self._placeholder_renderer.render_placeholder(
                title_for_location, current_location.list_item_id
            )
            if isinstance(title_for_location, (dict, immutables.Map))
            else title_for_location
        )
        return {
            "summary": {
                "title": title,
                "page_title": self._get_safe_page_title(title_for_location),
                "summary_type": "SectionSummary",
                "answers_are_editable": True,
                **summary,
            }
        }

    def _build_summary(self, location):
        """
        Build a summary context for a particular location.

        Does not support generating multiple sections at a time (i.e. passing no list_item_id for repeating section).
        """
        section = self._schema.get_section(location.section_id)
        summary = section.get("summary", {})
        collapsible = {"collapsible": summary.get("collapsible", False)}

        if summary.get("items"):
            summary_elements = {
                "custom_summary": list(
                    self._custom_summary_elements(
                        section["summary"]["items"], location, section
                    )
                )
            }

            return {**collapsible, **summary_elements}

        routing_path = self._router.routing_path(
            location.section_id, location.list_item_id
        )

        return {
            **collapsible,
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
            ],
        }

    def _title_for_location(self, location):

        section_id = location.section_id
        title = (
            self._schema.get_repeating_title_for_section(section_id)
            or self._schema.get_summary_title_for_section(section_id)
            or self._schema.get_title_for_section(section_id)
        )
        return title

    def _custom_summary_elements(self, section_summary, current_location, section):
        for summary_element in section_summary:
            if summary_element["type"] == "List":
                yield self._list_summary_element(
                    summary_element, current_location, section
                )

    def _list_summary_element(self, summary, current_location, section) -> Mapping:
        list_collector_block = self._schema.get_list_collectors_for_list(
            section, for_list=summary["for_list"]
        )[0]

        add_link = self._add_link(
            summary, current_location, section, list_collector_block
        )

        list_context = ListContext(
            self._language,
            self._schema,
            self._answer_store,
            self._list_store,
            self._progress_store,
            self._metadata,
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
            **list_context(
                list_collector_block["summary"],
                for_list=list_collector_block["for_list"],
                return_to_summary=True,
                edit_block_id=list_collector_block["edit_block"]["id"],
                remove_block_id=list_collector_block["remove_block"]["id"],
            ),
        }

    def _add_link(self, summary, current_location, section, list_collector_block):
        routing_path = self._router.routing_path(
            section["id"], current_location.list_item_id
        )

        if list_collector_block["id"] in routing_path:
            return url_for(
                "questionnaire.block",
                list_name=summary["for_list"],
                block_id=list_collector_block["add_block"]["id"],
                return_to_summary=True,
            )

        driving_question_block = QuestionnaireSchema.get_driving_question_for_list(
            section, summary["for_list"]
        )

        if driving_question_block:
            return url_for(
                "questionnaire.block",
                block_id=driving_question_block["id"],
                return_to_summary=True,
            )

    def _get_safe_page_title(self, title):
        return safe_content(
            f'{self._schema.get_single_string_value(title)} - {self._schema.json["title"]}'
        )
