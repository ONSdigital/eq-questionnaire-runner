from functools import cached_property
from typing import Any, Generator, Iterable, Mapping, MutableMapping, Optional, Union

from werkzeug.datastructures import ImmutableDict

from app.data_models import (
    AnswerStore,
    ListStore,
    ProgressStore,
    SupplementaryDataStore,
)
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.questionnaire_schema import LIST_COLLECTORS_WITH_REPEATING_BLOCKS
from app.questionnaire.routing_path import RoutingPath
from app.utilities import safe_content

from ...data_models.metadata_proxy import MetadataProxy
from .context import Context
from .summary import Group
from .summary.list_collector_block import ListCollectorBlock


class SectionSummaryContext(Context):
    def __init__(
        self,
        language: str,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        metadata: Optional[MetadataProxy],
        response_metadata: MutableMapping,
        routing_path: RoutingPath,
        current_location: Location,
        supplementary_data_store: SupplementaryDataStore,
    ) -> None:
        super().__init__(
            language,
            schema,
            answer_store,
            list_store,
            progress_store,
            metadata,
            response_metadata,
            supplementary_data_store,
        )
        self.routing_path = routing_path
        self.current_location = current_location

    def __call__(
        self,
        return_to: str | None = "section-summary",
        view_submitted_response: bool = False,
    ) -> Mapping[str, Any]:
        summary = self.build_summary(return_to, view_submitted_response)
        title_for_location = self.title_for_location()
        title = (
            self._placeholder_renderer.render_placeholder(
                title_for_location, self.current_location.list_item_id
            )
            if isinstance(title_for_location, dict)
            else title_for_location
        )

        page_title = self.get_page_title(title_for_location)

        summary_context = {
            "summary": {
                "title": title,
                "page_title": page_title,
                "summary_type": "SectionSummary",
                "answers_are_editable": True,
                "collapsible": summary.get("collapsible"),
            },
        }

        if custom_summary := summary.get("custom_summary"):
            summary_context["summary"]["custom_summary"] = custom_summary
        elif groups := summary.get("groups"):
            summary_context["summary"]["sections"] = [
                {
                    "title": title,
                    "groups": groups,
                }
            ]

        return summary_context

    @cached_property
    def section(self) -> ImmutableDict:
        # Type ignore: The section has to exist at this point
        section: ImmutableDict = self._schema.get_section(self.current_location.section_id)  # type: ignore
        return section

    def get_page_title(self, title_for_location: Union[Mapping, str]) -> str:
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

    def build_summary(
        self,
        return_to: str | None,
        view_submitted_response: bool,
    ) -> dict:
        """
        Build a summary context for a particular location.

        Does not support generating multiple sections at a time (i.e. passing no list_item_id for repeating section).
        """
        summary = self.section.get("summary", {})
        collapsible = {"collapsible": summary.get("collapsible", False)}

        show_non_item_answers = summary.get("show_non_item_answers", False)

        if summary.get("items") and not show_non_item_answers:
            summary_elements = {
                "custom_summary": list(
                    self._custom_summary_elements(
                        self.section["summary"]["items"],
                    )
                )
            }

            return collapsible | summary_elements

        refactored_groups = self._get_refactored_groups(self.section["groups"])

        groups = {
            **collapsible,
            "groups": [
                Group(
                    group_schema=group,
                    routing_path_block_ids=self.routing_path.block_ids,
                    answer_store=self._answer_store,
                    list_store=self._list_store,
                    metadata=self._metadata,
                    response_metadata=self._response_metadata,
                    schema=self._schema,
                    location=self.current_location,
                    language=self._language,
                    progress_store=self._progress_store,
                    supplementary_data_store=self._supplementary_data_store,
                    return_to=return_to,
                    return_to_block_id=None,
                    view_submitted_response=view_submitted_response,
                ).serialize()
                for group in refactored_groups
            ],
        }

        return groups

    def title_for_location(self) -> Union[str, dict]:
        section_id = self.current_location.section_id
        return (
            # Type ignore: section id should exist at this point
            self._schema.get_repeating_title_for_section(section_id)  # type: ignore
            or self._schema.get_summary_title_for_section(section_id)
            or self._schema.get_title_for_section(section_id)
        )

    def _custom_summary_elements(
        self, section_summary: Iterable[Mapping]
    ) -> Generator[dict[str, Any], Any, None]:
        for summary_element in section_summary:
            if summary_element["type"] == "List":
                list_collector_block = ListCollectorBlock(
                    routing_path_block_ids=self.routing_path.block_ids,
                    answer_store=self._answer_store,
                    list_store=self._list_store,
                    progress_store=self._progress_store,
                    metadata=self._metadata,
                    response_metadata=self._response_metadata,
                    schema=self._schema,
                    location=self.current_location,
                    language=self._language,
                    supplementary_data_store=self._supplementary_data_store,
                    return_to="section-summary",
                )
                yield list_collector_block.list_summary_element(summary_element)

    def _get_safe_page_title(self, title: Union[Mapping, str]) -> str:
        return (
            safe_content(self._schema.get_single_string_value(title)) if title else ""
        )

    @staticmethod
    def _get_refactored_groups(original_groups: dict) -> list[dict[str, Any]]:
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
                if block["type"] in LIST_COLLECTORS_WITH_REPEATING_BLOCKS:
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
