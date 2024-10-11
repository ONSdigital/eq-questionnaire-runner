from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal
from typing import Sequence, TypeAlias

EvaluatorTypes: TypeAlias = (
    bool | date | list[str] | list[date] | int | float | Decimal | None
)


class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, rule: dict[str, Sequence]) -> EvaluatorTypes:
        pass
