from typing import Any, Mapping, Optional

from app.views.contexts.preview.preview_block import PreviewBlock


class PreviewGroup:
    def __init__(
        self,
        *,
        group_schema: Mapping[str, Any],
        section_title: Optional[str],
        language: str,
    ):
        self.title = section_title
        self.language = language

        self.blocks = self._build_blocks(
            group_schema=group_schema,
        )

    @staticmethod
    def _build_blocks(
        group_schema: Mapping[str, Any],
    ) -> list[dict]:
        blocks = []

        for block in group_schema["blocks"]:
            if block["type"] == "Question":
                blocks.extend(
                    [
                        PreviewBlock(
                            block=block,
                        ).serialize()
                    ]
                )
        return blocks

    def serialize(
        self,
    ) -> dict[str, Any]:
        return {"title": self.title, "blocks": self.blocks}
