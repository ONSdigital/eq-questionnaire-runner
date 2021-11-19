from datetime import date
from typing import Callable, Generator, Iterable, Optional, Sequence, Union

from app.questionnaire.routing.helpers import ValueTypes
from app.questionnaire.routing.operations import Operations


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

    def __init__(self, name: str) -> None:
        self.name = name
        self._operation = OPERATIONS_MAPPINGS[self.name]
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


operations = Operations()

OPERATIONS_MAPPINGS: dict[str, Callable] = {
    Operator.NOT: operations.evaluate_not,
    Operator.AND: operations.evaluate_and,
    Operator.OR: operations.evaluate_or,
    Operator.EQUAL: operations.evaluate_equal,
    Operator.NOT_EQUAL: operations.evaluate_not_equal,
    Operator.GREATER_THAN: operations.evaluate_greater_than,
    Operator.LESS_THAN: operations.evaluate_less_than,
    Operator.GREATER_THAN_OR_EQUAL: operations.evaluate_greater_than_or_equal,
    Operator.LESS_THAN_OR_EQUAL: operations.evaluate_less_than_or_equal,
    Operator.IN: operations.evaluate_in,
    Operator.ALL_IN: operations.evaluate_all_in,
    Operator.ANY_IN: operations.evaluate_any_in,
    Operator.COUNT: operations.evaluate_count,
    Operator.DATE: operations.resolve_date_from_string,
}
