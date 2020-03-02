from typing import Iterator, Mapping

from flask import url_for

from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.contexts import Context
from app.views.contexts import ListContext
from app.views.contexts.summary.group import Group


class SummaryContext(Context):
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

    def build_groups_for_location(self, location):
        """
        Build a groups context for a particular location.

        Does not support generating multiple sections at a time (i.e. passing no list_item_id for repeating section).
        """
        section = self._schema.get_section(location.section_id)
        routing_path = self._router.routing_path(
            location.section_id, location.list_item_id
        )

        return [
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

    def build_all_groups(self):
        """ NB: Does not support repeating sections """
        all_groups = []

        for section_id in self._router.enabled_section_ids:
            all_groups.extend(
                self.build_groups_for_location(Location(section_id=section_id))
            )

        return all_groups

    def summary(self, collapsible):
        groups = self.build_all_groups()

        context = {
            "summary": {
                "groups": groups,
                "answers_are_editable": True,
                "collapsible": collapsible,
                "summary_type": "Summary",
            }
        }
        return context

    def section_summary(self, current_location):
        section_id = self._schema.get_section_id_for_block_id(current_location.block_id)
        section = self._schema.get_section(section_id)
        section_summary = self._schema.get_summary_for_section(section_id)
        block = self._schema.get_block(current_location.block_id)

        summary_context = {
            "summary": {
                "title": self._title_for_location(current_location),
                "summary_type": "SectionSummary",
                "answers_are_editable": True,
                "collapsible": block.get("collapsible", False),
            }
        }

        if not section_summary:
            summary_context["summary"]["groups"] = self.build_groups_for_location(
                current_location
            )
            return summary_context

        custom_summary = list(
            self._custom_summary_elements(section_summary, current_location, section)
        )

        summary_context["summary"]["custom_summary"] = custom_summary
        return summary_context

    def _title_for_location(self, location):
        title = self._schema.get_block(location.block_id).get("title")

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
            list_collector_block, current_location.block_id
        )
        rendered_summary = self._placeholder_renderer.render(
            summary, current_location.list_item_id
        )

        return {
            "title": rendered_summary["title"],
            "type": summary["type"],
            "add_link": add_link,
            "add_link_text": rendered_summary["add_link_text"],
            "empty_list_text": rendered_summary["empty_list_text"],
            "list_name": summary["for_list"],
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
