from datetime import date
from typing import Callable, Generator, Iterable, Optional, Sequence, Union

from app.questionnaire.routing.helpers import ValueTypes


class Operator:
    NOT: str = "not"
    AND: str = "and"
    OR: str = "or"
    EQUAL: str = "=="
    NOT_EQUAL: str = "!="
    GREATER_THAN: str = ">"
    LESS_THAN: str = "<"
    GREATER_THAN_OR_EQUAL: str = ">="
    LESS_THAN_OR_EQUAL: str = "<="
    IN: str = "in"
    ALL_IN: str = "all-in"
    ANY_IN: str = "any-in"
    COUNT: str = "count"
    DATE: str = "date"

    def __init__(self, name: str, operation: Callable) -> None:
        self.name = name
        self._operation = operation
        self._ensure_operands_not_none = self.name in {
            Operator.GREATER_THAN,
            Operator.GREATER_THAN_OR_EQUAL,
            Operator.LESS_THAN,
            Operator.LESS_THAN_OR_EQUAL,
            Operator.ALL_IN,
            Operator.ANY_IN,
        }

    def evaluate(
        self, operands: Union[Generator, Iterable]
    ) -> Union[bool, Optional[date]]:
        if self._ensure_operands_not_none:
            operands = list(operands)
            if self._any_operands_none(*operands):
                return False

        value: Union[bool, Optional[date]] = (
            self._operation(operands)
            if self.name in {Operator.AND, Operator.OR}
            else self._operation(*operands)
        )
        return value

    @staticmethod
    def _any_operands_none(*operands: Union[Sequence, ValueTypes]) -> bool:
        return any(operand is None for operand in operands)
