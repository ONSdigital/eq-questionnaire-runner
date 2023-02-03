from re import findall
from typing import Any, Mapping, Optional

from werkzeug.datastructures import ImmutableDict

from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import QuestionnaireSchema
from app.views.contexts.preview.preview_block import PreviewBlock


class PreviewGroup:
    def __init__(
        self,
        group_schema: Mapping[str, Any],
        metadata: Optional[MetadataProxy],
        section_title: Optional[str],
    ):
        self.survey_data = (
            metadata["survey_metadata"].data
            if metadata and metadata["survey_metadata"]
            else {}
        )
        self.title = section_title
        self.blocks = self._build_blocks(
            group_schema=group_schema, survey_data=self.survey_data
        )

    @staticmethod
    def _build_blocks(
        group_schema: Mapping[str, Any], survey_data: ImmutableDict[str, str]
    ) -> list[dict]:
        blocks = []

        for block in group_schema["blocks"]:
            if block["type"] == "Question":
                blocks.extend([PreviewBlock(block, survey_data).serialize()])
        return blocks

    def serialize(
        self,
    ) -> Any:  # QuestionnaireSchema.get_mutable_deepcopy returns "Any"

        dict_to_render = QuestionnaireSchema.get_mutable_deepcopy(
            {"title": self.title, "blocks": self.blocks}
        )
        for block in dict_to_render.get("blocks"):
            if question := block.get("question"):
                self.resolve_title(question)

        return dict_to_render

    def resolve_title(self, question: ImmutableDict) -> None:
        if isinstance(question["title"], dict):
            if title := question["title"].get("text", None):
                placeholders = findall(r"\{.*?}", title)

                title = question["title"].get("text")

                for placeholder in placeholders:
                    stripped_placeholder = placeholder.replace("{", "").replace("}", "")
                    if stripped_placeholder in self.survey_data:
                        title = title.replace(
                            placeholder, self.survey_data[stripped_placeholder]
                        )

            question["title"] = title
