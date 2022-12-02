from typing import Optional

from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.views.contexts.summary.block import Block
from app.views.contexts.summary.list_collector_block import ListCollectorBlock


class Group:
    def __init__(
        self,
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
    @staticmethod
    def _build_blocks_and_links(
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

            elif block["type"] in ["ListCollector"]:
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

                section = schema.get_section(location.section_id)
                summary = section.get("summary", {})
                if summary_items := summary.get("items"):
                    for summary_item in summary_items:
                        if (
                            summary_item["type"] == "List"
                            and summary_item["for_list"] == block["for_list"]
                        ):

                            list_summary_element = (
                                list_collector_block.list_summary_element(summary_item)
                            )
                            blocks.extend([list_summary_element])
                            links["add_link"] = list_summary_element["add_link"]
                            links["add_link_text"] = list_summary_element[
                                "add_link_text"
                            ]
                            links["empty_list_text"] = list_summary_element[
                                "empty_list_text"
                            ]

        return blocks, links

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
