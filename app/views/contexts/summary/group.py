from typing import Optional

from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.survey_config.link import SummaryLink
from app.views.contexts.summary.block import Block
from app.views.contexts.summary.list_collector_block import ListCollectorBlock


class Group:
    def __init__(
        self,
        *,
        group_schema,
        routing_path,
        answer_store,
        list_store,
        metadata,
        response_metadata,
        schema,
        location,
        language,
        progress_store,
        return_to,
        return_to_block_id: Optional[str] = None,
    ):
        self.id = group_schema["id"]
        self.title = group_schema.get("title")
        self.location = location
        self.blocks, self.links = self._build_blocks_and_links(
            group_schema=group_schema,
            routing_path=routing_path,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            schema=schema,
            location=location,
            return_to=return_to,
            progress_store=progress_store,
            language=language,
            return_to_block_id=return_to_block_id,
        )
        self.placeholder_renderer = PlaceholderRenderer(
            language=language,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            schema=schema,
        )

    # pylint: disable=too-many-locals
    def _build_blocks_and_links(
        self,
        *,
        group_schema,
        routing_path,
        answer_store,
        list_store,
        metadata,
        response_metadata,
        schema,
        location,
        return_to,
        progress_store,
        language,
        return_to_block_id,
    ):
        blocks = []

        links = {}

        for block in group_schema["blocks"]:
            if block["id"] not in routing_path:
                continue
            if block["type"] in [
                "Question",
                "ListCollectorDrivingQuestion",
            ]:
                blocks.extend(
                    [
                        Block(
                            block,
                            answer_store=answer_store,
                            list_store=list_store,
                            metadata=metadata,
                            response_metadata=response_metadata,
                            schema=schema,
                            location=location,
                            return_to=return_to,
                            return_to_block_id=return_to_block_id,
                        ).serialize()
                    ]
                )

            else:
                section = schema.get_section(location.section_id)

                if summary_item := self.get_summary_item_for_list_for_section(
                    section, block
                ):
                    if block["type"] in ["ListCollector"]:
                        list_collector_block = ListCollectorBlock(
                            routing_path=routing_path,
                            answer_store=answer_store,
                            list_store=list_store,
                            progress_store=progress_store,
                            metadata=metadata,
                            response_metadata=response_metadata,
                            schema=schema,
                            location=location,
                            language=language,
                        )

                        list_summary_element = (
                            list_collector_block.list_summary_element(summary_item)
                        )
                        blocks.extend([list_summary_element])
                        links["add_link"] = SummaryLink(
                            text=list_summary_element["add_link_text"],
                            url=list_summary_element["add_link"],
                            attributes={"data-qa": "add-item-link"},
                        )
                        links["empty_list_text"] = list_summary_element[
                            "empty_list_text"
                        ]

        return blocks, links

    @staticmethod
    def get_summary_item_for_list_for_section(section, block):
        summary = section.get("summary", {})
        if summary_items := summary.get("items"):
            for summary_item in summary_items:
                if (
                    summary_item["type"] == "List"
                    and summary_item["for_list"] == block["for_list"]
                ):
                    return summary_item

    def serialize(self):
        return self.placeholder_renderer.render(
            {
                "id": self.id,
                "title": self.title,
                "blocks": self.blocks,
                "links": self.links,
            },
            self.location.list_item_id,
        )
