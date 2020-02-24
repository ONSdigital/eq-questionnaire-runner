from itertools import chain
from typing import Iterable, Mapping

from flask import url_for

from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.contexts.context import Context
from app.views.contexts.list_collector_context import ListCollectorContext
from app.views.contexts.summary.group import Group


class SummaryContext(Context):
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

    def get_title_for_location(self, location):
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

    def section_summary(self, current_location):
        section_id = self._schema.get_section_id_for_block_id(current_location.block_id)
        section = self._schema.get_section(section_id)
        section_summary = self._schema.get_summary_for_section(section_id)
        block = self._schema.get_block(current_location.block_id)

        if section_summary:
            return {
                "summary": {
                    "title": block["title"],
                    "list_summaries": self.custom_section_summary(
                        current_location, section_summary, section
                    ),
                    "summary_type": "SectionSummary",
                }
            }

        return {
            "summary": {
                "groups": self.build_groups_for_location(current_location),
                "answers_are_editable": True,
                "collapsible": block.get("collapsible", False),
                "summary_type": "SectionSummary",
                "title": self.get_title_for_location(current_location),
            }
        }

    def custom_section_summary(
        self, current_location, section_summary: Iterable[Mapping], section
    ):
        summaries = [
            self.get_list_summaries(summary, current_location, section)
            for summary in section_summary
            if summary["type"] == "List"
        ]

        return list(chain.from_iterable(summaries))

    def get_list_summaries(
        self, summary: Mapping, current_location, section: Mapping
    ) -> Iterable[Mapping]:
        routing_path = self._router.routing_path(
            section["id"], current_location.list_item_id
        )

        list_collector_blocks = [
            list_collector
            for list_collector in self._schema.get_list_collectors_for_section(section)
            if list_collector["for_list"] == summary["for_list"]
        ]

        list_summaries = []
        for list_collector_block in list_collector_blocks:
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
                        "questionnaire.block", block_id=driving_question_block["id"]
                    )

            rendered_summary = self._placeholder_renderer.render(
                summary, current_location.list_item_id
            )

            list_context = ListCollectorContext(
                self._language,
                self._schema,
                self._answer_store,
                self._list_store,
                self._progress_store,
                self._metadata,
            )

            list_items = list_context.build_list_items_summary_context(
                list_collector_block, current_location.block_id
            )

            list_summary = {
                "title": rendered_summary["title"],
                "add_link": add_link,
                "add_link_text": rendered_summary["add_link_text"],
                "empty_list_text": rendered_summary["empty_list_text"],
                "list_name": summary["for_list"],
            }

            if list_items:
                list_summary["list"] = {"list_items": list_items, "editable": True}

            list_summaries.append(list_summary)
        return list_summaries
