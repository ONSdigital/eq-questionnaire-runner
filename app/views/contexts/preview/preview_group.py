from re import findall

from app.questionnaire import QuestionnaireSchema
from app.views.contexts.preview.preview_block import PreviewBlock


class PreviewGroup:
    def __init__(
        self,
        group_schema,
        metadata,
        section_title,
    ):
        self.survey_data = metadata["survey_metadata"].data
        self.title = section_title
        self.blocks = self._build_blocks(
            group_schema=group_schema, survey_data=self.survey_data
        )

    @staticmethod
    def _build_blocks(group_schema, survey_data):
        blocks = []

        for block in group_schema["blocks"]:
            if block["type"] == "Question":
                blocks.extend([PreviewBlock(block, survey_data).serialize()])
        return blocks

    def serialize(self):

        dict_to_render = QuestionnaireSchema.get_mutable_deepcopy(
            {"title": self.title, "blocks": self.blocks}
        )
        for block in dict_to_render.get("blocks"):
            if question := block.get("question"):
                self.resolve_title(question)

        return dict_to_render

    def resolve_title(self, question):
        if isinstance(question["title"], dict):
            placeholders = findall(r"\{.*?}", question["title"].get("text"))

            title = question["title"].get("text")

            for placeholder in placeholders:
                stripped_placeholder = placeholder.replace("{", "").replace("}", "")
                if stripped_placeholder in self.survey_data:
                    title = title.replace(
                        placeholder, self.survey_data[stripped_placeholder]
                    )

            question["title"] = title
