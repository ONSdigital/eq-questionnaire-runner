from functools import cached_property
from typing import Any, Mapping, Optional

from flask import url_for
from flask_babel import lazy_gettext

from app.data_models import AnswerStore, ListStore, ProgressStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.location import Location
from app.questionnaire.routing_path import RoutingPath
from app.utilities import safe_content

from .context import Context
from .list_context import ListContext
from .summary import Group


class SectionSummaryContext(Context):
    def __init__(
        self,
        language: str,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        metadata: Mapping[str, Any],
        response_metadata: Mapping,
        routing_path: RoutingPath,
        current_location: Location,
    ):
        super().__init__(
            language,
            schema,
            answer_store,
            list_store,
            progress_store,
            metadata,
            response_metadata,
        )
        self.routing_path = routing_path
        self.current_location = current_location

    def __call__(self, return_to: Optional[str] = "section-summary") -> Mapping:
        summary = self._build_summary(return_to)
        title_for_location = self._title_for_location()
        title = (
            self._placeholder_renderer.render_placeholder(
                title_for_location, self.current_location.list_item_id
            )
            if isinstance(title_for_location, dict)
            else title_for_location
        )

        page_title = self.get_page_title(title_for_location)

        return {
            "summary": {
                "title": title,
                "page_title": page_title,
                "summary_type": "SectionSummary",
                "answers_are_editable": True,
                "headers": [
                    lazy_gettext("Question"),
                    lazy_gettext("Answer given"),
                    lazy_gettext("Change answer"),
                ],
                **summary,
            }
        }

    @cached_property
    def section(self):
        return self._schema.get_section(self.current_location.section_id)

    @property
    def list_context(self):
        return ListContext(
            self._language,
            self._schema,
            self._answer_store,
            self._list_store,
            self._progress_store,
            self._metadata,
            self._response_metadata,
        )

    def get_page_title(self, title_for_location: str) -> str:

        section_repeating_page_title = (
            self._schema.get_repeating_page_title_for_section(
                self.current_location.section_id
            )
        )
        page_title = self._schema.get_custom_page_title_for_section(
            self.current_location.section_id
        ) or self._get_safe_page_title(title_for_location)

        if section_repeating_page_title:
            page_title = f"{page_title}: {section_repeating_page_title}"

        if self.current_location.list_item_id and self.current_location.list_name:
            list_item_position = self._list_store.list_item_position(
                self.current_location.list_name, self.current_location.list_item_id
            )
            page_title = page_title.format(list_item_position=list_item_position)
        return page_title

    def _build_summary(self, return_to: Optional[str]):
        """
        Build a summary context for a particular location.

        Does not support generating multiple sections at a time (i.e. passing no list_item_id for repeating section).
        """
        summary = self.section.get("summary", {})
        collapsible = {"collapsible": summary.get("collapsible", False)}

        show_non_item_answers = summary.get("show_non_item_answers", False)

        if summary.get("items"):
            if not show_non_item_answers:
                summary_elements = {
                    "custom_summary": list(
                        self._custom_summary_elements(
                            self.section["summary"]["items"],
                        )
                    )
                }

                return collapsible | summary_elements

            summary_elements = {
                "custom_summary": list(
                    self._custom_summary_elements(
                        self.section["summary"]["items"],
                    )
                )
            }

        else:
            summary_elements = {}

        return {
            **{"show_non_item_answers": show_non_item_answers},
            **collapsible,
            **summary_elements,
            "groups": [
                Group(
                    group,
                    self.routing_path,
                    self._answer_store,
                    self._list_store,
                    self._metadata,
                    self._response_metadata,
                    self._schema,
                    self.current_location,
                    self._language,
                    return_to,
                ).serialize()
                for group in self.section["groups"]
            ],
        }

    def _title_for_location(self):
        section_id = self.current_location.section_id
        return (
            self._schema.get_repeating_title_for_section(section_id)
            or self._schema.get_summary_title_for_section(section_id)
            or self._schema.get_title_for_section(section_id)
        )

    def _custom_summary_elements(self, section_summary):
        for summary_element in section_summary:
            if summary_element["type"] == "List":
                yield self._list_summary_element(summary_element)

    def _list_summary_element(self, summary: dict[str, str]) -> Mapping[str, Any]:
        edit_block_id, remove_block_id, primary_person_edit_block_id = None, None, None
        current_list = self._list_store[summary["for_list"]]

        list_collector_blocks = list(
            self._schema.get_list_collectors_for_list(
                self.section, for_list=summary["for_list"]
            )
        )

        list_collector_blocks_on_path = [
            list_collector_block
            for list_collector_block in list_collector_blocks
            if list_collector_block["id"] in self.routing_path.block_ids
        ]

        list_collector_block = (
            list_collector_blocks_on_path[0]
            if list_collector_blocks_on_path
            else list_collector_blocks[0]
        )

        if list_collector_blocks_on_path:

            edit_block_id = list_collector_block["edit_block"]["id"]
            remove_block_id = list_collector_block["remove_block"]["id"]
            add_link = self._add_link(summary, list_collector_block)

            if len(current_list) == 1 and current_list.primary_person:

                if primary_person_block := self._schema.get_list_collector_for_list(
                    self.section, for_list=summary["for_list"], primary=True
                ):
                    (
                        primary_person_edit_block_id,
                        edit_block_id,
                    ) = self._get_add_or_edit_blocks_primary(primary_person_block)

            rendered_summary = self._placeholder_renderer.render(
                summary, self.current_location.list_item_id
            )

            list_summary_context = self.list_context(
                list_collector_block["summary"],
                for_list=list_collector_block["for_list"],
                return_to="section-summary",
                edit_block_id=edit_block_id,
                remove_block_id=remove_block_id,
                primary_person_edit_block_id=primary_person_edit_block_id,
            )

            related_answers = (
                self._get_related_answers(current_list.first) if current_list else None
            )

            return {
                "title": rendered_summary["title"],
                "type": rendered_summary["type"],
                "add_link": add_link,
                "add_link_text": rendered_summary["add_link_text"],
                "empty_list_text": rendered_summary.get("empty_list_text"),
                "list_name": rendered_summary["for_list"],
                "related_answers": related_answers,
                **list_summary_context,
            }

        if current_list.primary_person:
            remove_block_id = list_collector_block["remove_block"]["id"]
            add_link = self._add_link(summary, list_collector_block)

            primary_person_block = self._schema.get_list_collector_for_list(
                self.section, for_list=summary["for_list"], primary=True
            )

            (
                primary_person_edit_block_id,
                edit_block_id,
            ) = self._get_add_or_edit_blocks_primary(
                primary_person_block  # type: ignore
            )
            # primary person block always exists at this point, type hint conflicts with schema's get_list_collector_for_list return type (Optional)

            rendered_summary = self._placeholder_renderer.render(
                summary, self.current_location.list_item_id
            )

            list_summary_context = self.list_context(
                list_collector_block["summary"],
                for_list=list_collector_block["for_list"],
                return_to="section-summary",
                edit_block_id=edit_block_id,
                remove_block_id=remove_block_id,
                primary_person_edit_block_id=primary_person_edit_block_id,
                for_list_item_ids=current_list.primary_person,
            )

            related_answers = self._get_related_answers(current_list.first)

            return {
                "title": rendered_summary["title"],
                "type": rendered_summary["type"],
                "add_link": add_link,
                "add_link_text": rendered_summary["add_link_text"],
                "empty_list_text": rendered_summary.get("empty_list_text"),
                "list_name": rendered_summary["for_list"],
                "related_answers": related_answers,
                **list_summary_context,
            }

    @staticmethod
    def _add_link(
        summary: dict[str, str], list_collector_block: Mapping[str, Any]
    ) -> str:

        return url_for(
            "questionnaire.block",
            list_name=summary["for_list"],
            block_id=list_collector_block["add_block"]["id"],
            return_to="section-summary",
        )

    def _get_safe_page_title(self, title):
        return (
            safe_content(self._schema.get_single_string_value(title)) if title else ""
        )

    def _get_related_answers(self, list_id: str) -> list[str]:
        section = self.section["id"]

        # pylint: disable=protected-access
        if related_answers := self._schema._get_related_answers_for_section(section):
            return [
                self._schema.get_answers_by_answer_id(answer.answer_id)[0]["label"]
                for answer in self._answer_store
                if answer.answer_id in related_answers
                and answer.list_item_id == list_id
            ]

    @staticmethod
    def _get_add_or_edit_blocks_primary(
        primary_person_block: Mapping[str, Any]
    ) -> tuple[str, str]:
        primary_person_edit_block_id = primary_person_block["add_or_edit_block"]["id"]
        edit_block_id = primary_person_block["add_or_edit_block"]["id"]

        return primary_person_edit_block_id, edit_block_id
