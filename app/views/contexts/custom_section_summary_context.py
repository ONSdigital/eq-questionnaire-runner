from typing import Iterator, Mapping

from flask import url_for

from app.questionnaire import QuestionnaireSchema
from app.views.contexts.list_context import ListContext
from app.views.contexts.section_summary_context import SectionSummaryContext


class CustomSectionSummaryContext(SectionSummaryContext):
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
        custom_section_summary_context = self._section_summary_context(current_location)
        section = self._schema.get_section(current_location.section_id)

        custom_section_summary = list(
            self._custom_summary_elements(section["summary"], current_location, section)
        )

        custom_section_summary_context["summary"][
            "custom_summary"
        ] = custom_section_summary
        return custom_section_summary_context

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
