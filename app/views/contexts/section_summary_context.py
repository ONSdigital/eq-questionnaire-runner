from functools import cached_property
from typing import Any, Mapping, Optional

from flask import url_for

from app.data_models import AnswerStore, ListStore, ProgressStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.location import Location
from app.questionnaire.routing_path import RoutingPath
from app.questionnaire.variants import choose_variant
from app.utilities import safe_content

from ...data_models.list_store import ListModel
from ...data_models.metadata_proxy import MetadataProxy
from .context import Context
from .list_context import ListContext
from .summary import Group
from .summary.block import Block


class SectionSummaryContext(Context):
    def __init__(
        self,
        language: str,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        metadata: Optional[MetadataProxy],
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

        refactored_groups = self._get_refactored_groups(self.section["groups"])

        groups = {
            "show_non_item_answers": show_non_item_answers,
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
                    summary_elements,
                    return_to_block_id=None,
                ).serialize()
                for group in refactored_groups
            ],
        }

        return groups

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

    # pylint: disable=too-many-locals
    def _list_summary_element(self, summary: dict[str, str]) -> Mapping[str, Any]:
        list_collector_block = None
        (
            edit_block_id,
            remove_block_id,
            primary_person_edit_block_id,
            related_answers,
            answer_title,
            answer_focus,
        ) = (None, None, None, None, None, None)
        current_list = self._list_store[summary["for_list"]]

        list_collector_blocks = list(
            self._schema.get_list_collectors_for_list(
                self.section, for_list=summary["for_list"]
            )
        )

        add_link = self._add_link(summary, list_collector_block)

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

        rendered_summary = self._placeholder_renderer.render(
            summary, self.current_location.list_item_id
        )

        if list_collector_blocks_on_path:

            edit_block_id = list_collector_block["edit_block"]["id"]
            remove_block_id = list_collector_block["remove_block"]["id"]
            add_link = self._add_link(summary, list_collector_block)

        if len(current_list) == 1 and current_list.primary_person:

            if primary_person_block := self._schema.get_list_collector_for_list(
                self.section, for_list=summary["for_list"], primary=True
            ):
                primary_person_edit_block_id = edit_block_id = primary_person_block[
                    "add_or_edit_block"
                ]["id"]

        list_summary_context = self.list_context(
            list_collector_block["summary"],
            for_list=list_collector_block["for_list"],
            return_to="section-summary",
            edit_block_id=edit_block_id,
            remove_block_id=remove_block_id,
            primary_person_edit_block_id=primary_person_edit_block_id,
        )

        related_answers = (
            self._get_related_answers(current_list, list_collector_block.get("id"))
            if current_list
            else None
        )

        if related_answers:
            answer_focus = f"#{self._get_answer_id(list_collector_block)}"

        answer_title = (
            self._get_answer_title(list_collector_block) if related_answers else None
        )

        return {
            "title": rendered_summary["title"],
            "type": rendered_summary["type"],
            "add_link": add_link,
            "add_link_text": rendered_summary["add_link_text"],
            "empty_list_text": rendered_summary.get("empty_list_text"),
            "list_name": rendered_summary["for_list"],
            "related_answers": related_answers,
            "answer_title": answer_title,
            "answer_focus": answer_focus,
            **list_summary_context,
        }

    def _add_link(self, summary, list_collector_block):

        if list_collector_block:
            return url_for(
                "questionnaire.block",
                list_name=summary["for_list"],
                block_id=list_collector_block["add_block"]["id"],
                return_to="section-summary",
            )

        driving_question_block = QuestionnaireSchema.get_driving_question_for_list(
            self.section, summary["for_list"]
        )

        if driving_question_block:
            return url_for(
                "questionnaire.block",
                block_id=driving_question_block["id"],
                return_to="section-summary",
            )

    def _get_safe_page_title(self, title):
        return (
            safe_content(self._schema.get_single_string_value(title)) if title else ""
        )

    def _get_related_answers(
        self, current_list: ListModel, list_collector_block_id
    ) -> dict[str, list]:
        section = self.section["id"]

        if related_answers := self._schema.get_related_answers_for_section(
            section, current_list
        ):
            related_answers_dict = {}

            for list_id in current_list:
                for answer in self._answer_store:
                    if (
                        answer.answer_id in related_answers
                        and answer.list_item_id == list_id
                        and list_collector_block_id in self.routing_path.block_ids
                    ):
                        edit_block = self._schema.get_edit_block_for_list_collector(
                            list_collector_block_id
                        )
                        edit_block_id = edit_block.get("id") if edit_block else None

                        question = dict(
                            self._schema.get_add_block_for_list_collector(  # type: ignore
                                list_collector_block_id
                            ).get(
                                "question"
                            )
                        )

                        question["answers"] = list(question["answers"])[1:]

                        block_schema = {
                            "id": edit_block_id,
                            "title": None,
                            "number": None,
                            "type": "ListCollector",
                            "for_list": current_list.name,
                            "question": question,
                        }
                        block = [
                            Block(
                                block_schema,
                                answer_store=self._answer_store,
                                list_store=self._list_store,
                                metadata=self._metadata,
                                response_metadata=self._response_metadata,
                                schema=self._schema,
                                location=Location(
                                    list_name=current_list.name,
                                    list_item_id=list_id,
                                    section_id=self.section["id"],
                                ),
                                return_to="section-summary",
                                return_to_block_id=None,
                            ).serialize()
                        ]

                        related_answers_dict[list_id] = block

            return related_answers_dict

    def _get_answer_title(self, list_collector_block: Mapping[str, Any]) -> str:
        if list_collector_block["add_block"].get("question_variants"):
            variant_label = choose_variant(
                list_collector_block["add_block"],
                self._schema,
                self._metadata,
                self._response_metadata,
                self._answer_store,
                self._list_store,
                variants_key="question_variants",
                single_key="question",
                current_location=self.current_location,
            )["answers"][0]["label"]

            return variant_label

        return list_collector_block["add_block"]["question"]["answers"][0]["label"]

    def _get_answer_id(self, list_collector_block: Mapping[str, Any]) -> str:
        if list_collector_block["add_block"].get("question_variants"):
            variant_label = choose_variant(
                list_collector_block["add_block"],
                self._schema,
                self._metadata,
                self._response_metadata,
                self._answer_store,
                self._list_store,
                variants_key="question_variants",
                single_key="question",
                current_location=self.current_location,
            )["answers"][0]["id"]

            return variant_label

        return list_collector_block["add_block"]["question"]["answers"][0]["id"]

    @staticmethod
    def _get_refactored_groups(original_groups: dict) -> list[dict]:
        """original schema groups are refactored into groups based on block types, it follows the order/sequence of blocks in the original groups, all the
        non list collector blocks are put together into groups, list collectors are put into separate groups, this way summary groups are displayed correctly
        on section summary"""
        refactored_groups = []
        group_number = 0

        for group in list(original_groups):
            group_name = group["id"]
            non_list_collector_blocks: list[dict[str, str]] = []
            list_collector_blocks: list[dict[str, str]] = []
            for block in group["blocks"]:
                if block["type"] == "ListCollector":
                    # if list collector block encountered, close the previously started non list collector blocks list if exists
                    if non_list_collector_blocks:
                        previously_started_group = {
                            "id": f"{group_name}-{group_number}",
                            "blocks": non_list_collector_blocks,
                        }
                        # add previous non list collector blocks group to all groups and increase the group number for the list collector group
                        # that you handle next
                        refactored_groups.append(previously_started_group)
                        group_number += 1
                    list_collector_blocks.append(block)
                    list_collector_group = {
                        "id": f"{group_name}-{group_number}",
                        "blocks": list_collector_blocks,
                    }
                    # add current list collector group to all groups and increase the group number for the next group
                    refactored_groups.append(list_collector_group)
                    group_number += 1
                    # reset both types of block lists for next iterations of this loop if any
                    list_collector_blocks = []
                    non_list_collector_blocks = []

                else:
                    # if list collector not encountered keep adding blocks or add first one to an empty non list collector blocks list
                    non_list_collector_blocks.append(block)

            # on exiting the loop, accumulated list of blocks gets added as a group
            non_list_collector_group = {
                "id": f"{group_name}-{group_number}",
                "blocks": non_list_collector_blocks,
                "title": group.get("title"),
            }
            refactored_groups.append(non_list_collector_group)

        return refactored_groups
