from typing import Any, Union

from app.data_models import QuestionnaireStore
from app.questionnaire import QuestionnaireSchema
from app.views.contexts.preview.preview_question import PreviewQuestion


class PreviewBlock:
    def __init__(
        self,
        *,
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        section_id: str,
        language: str,
        block_id: str,
    ):
        self.schema = schema
        self.questionnaire_store = questionnaire_store
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
            schema=schema,
            questionnaire_store=questionnaire_store,
            section_id=section_id,
            block_id=block_id,
            language=language,
        ).serialize()

    def serialize(self) -> dict[str, Union[str, dict, Any]]:
        return {
            "question": self.question,
        }
