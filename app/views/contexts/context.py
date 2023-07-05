from abc import ABC
from typing import MutableMapping

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.data_models.progress_store import ProgressStore
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.router import Router


class Context(ABC):
    def __init__(
        self,
        language: str,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        metadata: MetadataProxy | None,
        response_metadata: MutableMapping,
        placeholder_preview_mode: bool = False,
    ) -> None:
        self._language = language
        self._schema = schema
        self._answer_store = answer_store
        self._list_store = list_store
        self._progress_store = progress_store
        self._metadata = metadata
        self._response_metadata = response_metadata
        self._placeholder_preview_mode = placeholder_preview_mode

        self._router = Router(
            schema=self._schema,
            answer_store=self._answer_store,
            list_store=self._list_store,
            progress_store=self._progress_store,
            metadata=self._metadata,
            response_metadata=self._response_metadata,
        )

        self._placeholder_renderer = PlaceholderRenderer(
            language=self._language,
            answer_store=self._answer_store,
            list_store=self._list_store,
            metadata=self._metadata,
            response_metadata=self._response_metadata,
            schema=self._schema,
            progress_store=self._progress_store,
            placeholder_preview_mode=self._placeholder_preview_mode,
        )
