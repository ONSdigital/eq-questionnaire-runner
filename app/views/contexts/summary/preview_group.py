import re

from app.questionnaire import QuestionnaireSchema
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.views.contexts.summary.preview_block import PreviewBlock


class PreviewGroup:
    def __init__(
        self,
        group_schema,
        answer_store,
        list_store,
        metadata,
        response_metadata,
        schema,
        location,
        language,
        section_title,
    ):
        self.id = group_schema["id"]
        self.title = section_title
        self.location = location
        self.blocks = self._build_blocks(
            group_schema=group_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            schema=schema,
            location=location,
        )
        self.placeholder_renderer = PlaceholderRenderer(
            language=language,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            schema=schema,
        )
        self.survey_data = metadata["survey_metadata"].data

    @staticmethod
    def _build_blocks(
        *,
        group_schema,
        answer_store,
        list_store,
        metadata,
        response_metadata,
        schema,
        location,
    ):
        blocks = []

        for block in group_schema["blocks"]:
            if block["id"] and block["type"] == "Question":
                blocks.extend(
                    [
                        PreviewBlock(
                            block,
                            answer_store=answer_store,
                            list_store=list_store,
                            metadata=metadata,
                            response_metadata=response_metadata,
                            schema=schema,
                            location=location,
                        ).serialize()
                    ]
                )
        return blocks

    def serialize(self):

        dict_to_render = QuestionnaireSchema.get_mutable_deepcopy(
            {"id": self.id, "title": self.title, "blocks": self.blocks}
        )
        for block in dict_to_render.get("blocks"):
            if question := block.get("question"):
                self.resolve_title(question)

        return dict_to_render

    def resolve_title(self, question):
        if isinstance(question["title"], str):
            placeholders = re.findall(r"\{.*?}", question["title"])
            title = question["title"]

            for placeholder in placeholders:
                stripped_placeholder = placeholder.replace("{", "").replace("}", "")
                if stripped_placeholder in self.survey_data:
                    title = title.replace(
                        placeholder, self.survey_data[stripped_placeholder]
                    )

            question["title"] = title

        elif isinstance(question["title"], dict):
            placeholders = re.findall(r"\{.*?}", question["title"].get("text"))

            title = question["title"].get("text")

            for placeholder in placeholders:
                stripped_placeholder = placeholder.replace("{", "").replace("}", "")
                if stripped_placeholder in self.survey_data:
                    title = title.replace(
                        placeholder, self.survey_data[stripped_placeholder]
                    )

            question["title"] = title
