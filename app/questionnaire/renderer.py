from abc import ABC, abstractmethod
from typing import Mapping

from app.data_models.data_stores import DataStores
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.utilities.types import LocationType


class Renderer(ABC):
    @abstractmethod
    def __init__(
        self,
        language: str,
        data_stores: DataStores,
        schema: QuestionnaireSchema,
        location: LocationType | None = None,
        placeholder_preview_mode: bool | None = False,
    ):
        self._placeholder_preview_mode = placeholder_preview_mode
        self._language = language
        self._data_stores = data_stores
        self._schema = schema
        self._location = location

    @abstractmethod
    def render(  # pragma: no cover
        self,
        *,
        data_to_render: Mapping,
        list_item_id: str | None,
    ) -> dict:
        pass
