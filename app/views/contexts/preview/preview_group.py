from typing import Any, Mapping

from app.views.contexts.preview.preview_block import PreviewBlock


class PreviewGroup:
    def __init__(
        self,
        *,
        group_schema: Mapping[str, Any],
    ):
        self._blocks = self._build_blocks(
            group_schema=group_schema,
        )

    @staticmethod
    def _build_blocks(
        group_schema: Mapping[str, Any],
    ) -> list[dict]:
        return [
            PreviewBlock(
                block=block,
            ).serialize()
            for block in group_schema["blocks"]
            if block["type"] == "Question"
        ]

    def serialize(
        self,
    ) -> dict[str, Any]:
        return {"blocks": self._blocks}
