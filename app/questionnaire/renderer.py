from abc import ABC, abstractmethod
from typing import Mapping

from app.data_models.data_stores import DataStores
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.utilities.types import LocationType


class Renderer(ABC):
    @abstractmethod
    def render(  # pragma: no cover
        self,
        *,
        data_to_render: Mapping,
        list_item_id: str | None,
    ) -> dict:
        pass
