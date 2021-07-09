from typing import Iterable

from app.questionnaire.routing.operations import (
    answer_types,
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
    resolve_datetime_from_string,
)


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
    DATE = "date"

    def __init__(self, name: str) -> None:
        self.name = name
        self._operation = OPERATIONS[self.name]
        self._short_circuit = self.name in {Operator.AND, Operator.OR}

    def evaluate(self, operands: Iterable) -> answer_types:
        value: answer_types = (
            self._operation(operands)
            if self._short_circuit
            else self._operation(*operands)
        )
        return value


OPERATIONS = {
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
    Operator.DATE: resolve_datetime_from_string,
}
