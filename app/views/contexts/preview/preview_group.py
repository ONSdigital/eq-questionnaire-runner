from typing import Any, Mapping, Optional, Union

from app.data_models import AnswerStore, ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import QuestionnaireSchema
from app.views.contexts.preview.preview_block import PreviewBlock


class PreviewGroup:
    def __init__(
        self,
        *,
        group_schema: Mapping[str, Any],
        section_title: Optional[str],
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: Optional[MetadataProxy],
        response_metadata: Mapping[str, Union[str, int, list]],
        section_id: str,
        language: str,
    ):
        self.title = section_title
        self.schema = schema
        self.answer_store = answer_store
        self.list_store = list_store
        self.metadata = metadata
        self.response_metadata = response_metadata
        self.language = language

        self.blocks = self._build_blocks(
            group_schema=group_schema,
            section_id=section_id,
        )

    def _build_blocks(
        self,
        group_schema: Mapping[str, Any],
        section_id: str,
    ) -> list[dict]:
        blocks = []

        for block in group_schema["blocks"]:
            if block["type"] == "Question":
                blocks.extend(
                    [
                        PreviewBlock(
                            schema=self.schema,
                            answer_store=self.answer_store,
                            list_store=self.list_store,
                            metadata=self.metadata,
                            response_metadata=self.response_metadata,
                            section_id=section_id,
                            language=self.language,
                            block_id=block["id"],
                        ).serialize()
                    ]
                )
        return blocks

    def serialize(
        self,
    ) -> dict[str, Any]:
        return {"title": self.title, "blocks": self.blocks}
