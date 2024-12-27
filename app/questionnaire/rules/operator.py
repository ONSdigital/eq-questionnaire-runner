from datetime import date
from typing import TYPE_CHECKING, Generator, Iterable, Sequence

from app.questionnaire.rules.helpers import ValueTypes

if TYPE_CHECKING:
    from app.questionnaire.rules.operations import Operations  # pragma: no cover


class Operator:
    NOT = "not"
    AND = "and"
    OR = "or"
    EQUAL = "=="
    NOT_EQUAL = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_THAN_OR_EQUAL = ">="
    LESS_THAN_OR_EQUAL = "<="
    IN = "in"
    ALL_IN = "all-in"
    ANY_IN = "any-in"
    COUNT = "count"
    DATE = "date"
    DATE_RANGE = "date-range"
    FORMAT_DATE = "format-date"
    MAP = "map"
    OPTION_LABEL_FROM_VALUE = "option-label-from-value"
    SUM = "+"

    def __init__(self, name: str, operations: "Operations") -> None:
        self.name = name
        self._operation = getattr(operations, OPERATION_MAPPING[self.name])
        self._ensure_operands_not_none = self.name in {
            Operator.GREATER_THAN,
            Operator.GREATER_THAN_OR_EQUAL,
            Operator.LESS_THAN,
            Operator.LESS_THAN_OR_EQUAL,
            Operator.ALL_IN,
            Operator.ANY_IN,
        }

    def evaluate(self, operands: Generator | Iterable) -> bool | date | None:
        if self._ensure_operands_not_none:
            operands = list(operands)
            if self._any_operands_none(*operands):
                return False

        value: bool | date | None = (
            self._operation(operands)
            if self.name in {Operator.AND, Operator.OR}
            else self._operation(*operands)
        )
        return value

    @staticmethod
    def _any_operands_none(*operands: Sequence | ValueTypes) -> bool:
        return any(operand is None for operand in operands)


OPERATION_MAPPING: dict[str, str] = {
    Operator.NOT: "evaluate_not",
    Operator.AND: "evaluate_and",
    Operator.OR: "evaluate_or",
    Operator.EQUAL: "evaluate_equal",
    Operator.NOT_EQUAL: "evaluate_not_equal",
    Operator.GREATER_THAN: "evaluate_greater_than",
    Operator.LESS_THAN: "evaluate_less_than",
    Operator.GREATER_THAN_OR_EQUAL: "evaluate_greater_than_or_equal",
    Operator.LESS_THAN_OR_EQUAL: "evaluate_less_than_or_equal",
    Operator.IN: "evaluate_in",
    Operator.ALL_IN: "evaluate_all_in",
    Operator.ANY_IN: "evaluate_any_in",
    Operator.COUNT: "evaluate_count",
    Operator.DATE: "resolve_date_from_string",
    Operator.DATE_RANGE: "date_range",
    Operator.FORMAT_DATE: "format_date",
    Operator.MAP: "evaluate_map",
    Operator.OPTION_LABEL_FROM_VALUE: "evaluate_option_label_from_value",
    Operator.SUM: "evaluate_sum",
}
