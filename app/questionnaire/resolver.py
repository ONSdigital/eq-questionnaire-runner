from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable, Mapping, TypeAlias

from markupsafe import Markup

from app.data_models.data_stores import DataStores
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.utilities.types import LocationType

ResolverTypes = None | str | int | Decimal | list | dict
ResolveTypes = Markup | list[Markup]
IntOrDecimal = int | Decimal
ResolvedAnswerList = list[ResolveTypes | None]

ResolveEscapedTypes: TypeAlias = Markup | list[Markup]


@dataclass
class Resolver(ABC):
    data_stores: DataStores
    schema: QuestionnaireSchema
    location: LocationType | None
    list_item_id: str | None
    routing_path_block_ids: Iterable[str] | None = None
    use_default_answer: bool = False
    escape_answer_values: bool = False
    assess_routing_path: bool | None = True

    @abstractmethod
    def resolve(self, value_source: Mapping) -> ResolveEscapedTypes | ResolverTypes:
        pass
