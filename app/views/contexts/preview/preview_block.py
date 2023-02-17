from typing import Any, Mapping, Union

from app.data_models import QuestionnaireStore
from app.questionnaire import Location, QuestionnaireSchema
from app.views.contexts.preview.preview_question import PreviewQuestion


class PreviewBlock:
    def __init__(
        self,
        block_schema: Mapping[str, Any],
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        current_location: Location,
        section_id: str,
        language: str,
        block_id: str,
    ):
        self.title = block_schema.get("title")

        self.schema = schema

        self.questionnaire_store = questionnaire_store

        self.current_location = current_location

        self.section_id = section_id

        self.block_id = block_id

        self.question = self.get_question(
            schema=self.schema,
            questionnaire_store=self.questionnaire_store,
            section_id=self.section_id,
            block_id=block_id,
            language=language,
        )

    @staticmethod
    def get_question(
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        section_id: str,
        block_id: str,
        language: str,
    ) -> dict[str, Union[str, dict]]:
        return PreviewQuestion(
            schema, questionnaire_store, section_id, block_id, language
        ).serialize()

    def serialize(self) -> dict[str, Union[str, dict, Any]]:
        return {
            "title": self.title,
            "question": self.question,
        }
