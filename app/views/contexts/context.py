from abc import ABC

from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.router import Router


class Context(ABC):
    def __init__(
        self, language, schema, answer_store, list_store, progress_store, metadata
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
        )

