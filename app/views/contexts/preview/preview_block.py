from typing import Any, Mapping, Optional, Union

from app.data_models import AnswerStore, ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import QuestionnaireSchema
from app.views.contexts.preview.preview_question import PreviewQuestion


class PreviewBlock:
    def __init__(
        self,
        *,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: Optional[MetadataProxy],
        response_metadata: Mapping[str, Union[str, int, list]],
        section_id: str,
        language: str,
        block_id: str,
    ):
        self.schema = schema
        self.answer_store = answer_store
        self.list_store = list_store
        self.metadata = metadata
        self.response_metadata = response_metadata
        self.section_id = section_id
        self.block_id = block_id
        self.question = self.get_question(
            schema=self.schema,
            answer_store=self.answer_store,
            list_store=self.list_store,
            metadata=self.metadata,
            response_metadata=self.response_metadata,
            section_id=self.section_id,
            block_id=block_id,
            language=language,
        )

    @staticmethod
    def get_question(
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: Optional[MetadataProxy],
        response_metadata: Mapping[str, Union[str, int, list]],
        section_id: str,
        block_id: str,
        language: str,
    ) -> dict[str, Union[str, dict]]:
        return PreviewQuestion(
            schema=schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            section_id=section_id,
            block_id=block_id,
            language=language,
        ).serialize()

    def serialize(self) -> dict[str, Union[str, dict, Any]]:
        return {
            "question": self.question,
        }
