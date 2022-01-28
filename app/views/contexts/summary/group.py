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
    ):
        blocks = []

        for block in group_schema["blocks"]:
            if block["id"] in routing_path and block["type"] == "Question":
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
                        ).serialize()
                    ]
                )

        return blocks

    def serialize(self):
        return self.placeholder_renderer.render(
            {"id": self.id, "title": self.title, "blocks": self.blocks},
            self.location.list_item_id,
        )
