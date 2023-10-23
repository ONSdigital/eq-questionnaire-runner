from abc import ABC

from app.data_models.data_stores import DataStores
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.router import Router


class Context(ABC):
    def __init__(
        self,
        language: str,
        schema: QuestionnaireSchema,
        data_stores: DataStores,
        placeholder_preview_mode: bool = False,
    ) -> None:
        self._language = language
        self._schema = schema
        self._data_stores = data_stores
        self._placeholder_preview_mode = placeholder_preview_mode

        self._router = Router(schema=self._schema, data_stores=self._data_stores)

        self._placeholder_renderer = self._data_stores.placeholder_renderer(
            language=self._language,
            schema=self._schema,
            placeholder_preview_mode=self._placeholder_preview_mode,
        )
