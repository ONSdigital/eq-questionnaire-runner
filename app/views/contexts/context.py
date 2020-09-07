from abc import ABC
from typing import Mapping

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
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
        metadata: Mapping,
    ):
        self._language = language
        self._schema = schema
        self._answer_store = answer_store
        self._list_store = list_store
        self._progress_store = progress_store
        self._metadata = metadata

        self._router = Router(
            self._schema,
            self._answer_store,
            self._list_store,
            self._progress_store,
            self._metadata,
        )

        self._placeholder_renderer = PlaceholderRenderer(
            language=self._language,
            schema=self._schema,
            answer_store=self._answer_store,
            metadata=self._metadata,
            list_store=self._list_store,
        )
