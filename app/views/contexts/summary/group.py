from typing import Optional

from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.views.contexts.summary.block import Block


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
        return_to,
        summary_elements=None,
        return_to_block_id: Optional[str] = None,
    ):
        self.id = group_schema["id"]
        self.title = group_schema.get("title")
        self.location = location
        self.blocks = self._build_blocks(
            group_schema=group_schema,
            routing_path=routing_path,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            schema=schema,
            location=location,
            return_to=return_to,
            summary_elements=summary_elements,
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

    @staticmethod
    def _build_blocks(
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
        summary_elements,
        return_to_block_id,
    ):
        blocks = []

        for block in group_schema["blocks"]:
            if block["id"] in routing_path and block["type"] in [
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

            elif block["id"] in routing_path and block["type"] in [
                "ListCollector",
            ]:
                for list_element in summary_elements["custom_summary"]:
                    blocks.extend([list_element])

        return blocks

    def serialize(self):
        return self.placeholder_renderer.render(
            {"id": self.id, "title": self.title, "blocks": self.blocks},
            self.location.list_item_id,
        )
