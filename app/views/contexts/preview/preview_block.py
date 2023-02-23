from typing import Any, Mapping, Optional, Union

from werkzeug.datastructures import ImmutableDict

from app.data_models import AnswerStore, ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.views.contexts.preview.preview_question import PreviewQuestion


class PreviewBlock:
    def __init__(
        self,
        *,
        block: ImmutableDict,
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: Optional[MetadataProxy],
        response_metadata: Mapping[str, Union[str, int, list]],
        section_id: str,
        block_id: str,
    ):
        self.block = block
        self.answer_store = answer_store
        self.list_store = list_store
        self.metadata = metadata
        self.response_metadata = response_metadata
        self.section_id = section_id
        self.block_id = block_id
        self.question = self.get_question(
            block=self.block,
            answer_store=self.answer_store,
            list_store=self.list_store,
            metadata=self.metadata,
            response_metadata=self.response_metadata,
            section_id=self.section_id,
            block_id=block_id,
        )

    @staticmethod
    def get_question(
        block: ImmutableDict,
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: Optional[MetadataProxy],
        response_metadata: Mapping[str, Union[str, int, list]],
        section_id: str,
        block_id: str,
    ) -> dict[str, Union[str, dict]]:
        return PreviewQuestion(
            block=block,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            section_id=section_id,
            block_id=block_id,
        ).serialize()

    def serialize(self) -> dict[str, Union[str, dict, Any]]:
        return {
            "question": self.question,
        }
