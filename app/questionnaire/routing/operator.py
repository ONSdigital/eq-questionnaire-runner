from datetime import date
from typing import Callable, Generator, Iterable, Optional, Sequence, Union

from app.questionnaire.routing.helpers import ValueTypes
from app.questionnaire.routing.operations import (
    evaluate_all_in,
    evaluate_and,
    evaluate_any_in,
    evaluate_equal,
    evaluate_greater_than,
    evaluate_greater_than_or_equal,
    evaluate_in,
    evaluate_less_than,
    evaluate_less_than_or_equal,
    evaluate_not,
    evaluate_not_equal,
    evaluate_or,
    resolve_date_from_string,
)


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
    DATE: str = "date"

    def __init__(self, name: str) -> None:
        self.name = name
        self._operation = OPERATIONS[self.name]
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


OPERATIONS: dict[str, Callable] = {
    Operator.NOT: evaluate_not,
    Operator.AND: evaluate_and,
    Operator.OR: evaluate_or,
    Operator.EQUAL: evaluate_equal,
    Operator.NOT_EQUAL: evaluate_not_equal,
    Operator.GREATER_THAN: evaluate_greater_than,
    Operator.LESS_THAN: evaluate_less_than,
    Operator.GREATER_THAN_OR_EQUAL: evaluate_greater_than_or_equal,
    Operator.LESS_THAN_OR_EQUAL: evaluate_less_than_or_equal,
    Operator.IN: evaluate_in,
    Operator.ALL_IN: evaluate_all_in,
    Operator.ANY_IN: evaluate_any_in,
    Operator.DATE: resolve_date_from_string,
}
