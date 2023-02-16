from typing import Any, Mapping, Optional

from app.data_models import QuestionnaireStore
from app.questionnaire import Location, QuestionnaireSchema
from app.views.contexts.preview.preview_block import PreviewBlock


class PreviewGroup:
    def __init__(
        self,
        group_schema: Mapping[str, Any],
        section_title: Optional[str],
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        current_location: Location,
        section_id: str,
        language: str,
    ):
        self.title = section_title
        self.schema = schema
        self.questionnaire_store = questionnaire_store
        self.current_location = current_location
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
                            block,
                            self.schema,
                            self.questionnaire_store,
                            self.current_location,
                            section_id,
                            self.language,
                            block_id=block["id"],
                        ).serialize()
                    ]
                )
        return blocks

    def serialize(
        self,
    ) -> Any:  # QuestionnaireSchema.get_mutable_deepcopy returns "Any"

        return QuestionnaireSchema.get_mutable_deepcopy(
            {"title": self.title, "blocks": self.blocks}
        )
