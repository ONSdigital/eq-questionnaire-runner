from abc import ABC
from typing import Mapping

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.data_models.progress_store import ProgressStore
from app.questionnaire import Location
from app.questionnaire.path_finder import PathFinder
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
        response_metadata: Mapping,
        location: Location | None = None,
    ) -> None:
        self._language = language
        self._schema = schema
        self._answer_store = answer_store
        self._list_store = list_store
        self._progress_store = progress_store
        self._metadata = metadata
        self._response_metadata = response_metadata
        self._location = location
        self._placeholder_preview_mode = self._schema.preview_enabled

        self._router = Router(
            self._schema,
            self._answer_store,
            self._list_store,
            self._progress_store,
            self._metadata,
            self._response_metadata,
        )

        self._path_finder = PathFinder(
            self._schema,
            self._answer_store,
            self._list_store,
            self._progress_store,
            self._metadata,
            self._response_metadata,
        )

        if self._location:
            self._routing_path = self._path_finder.routing_path(
                self._location.section_id, self._location.list_item_id
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
            location=self._location,
        )
