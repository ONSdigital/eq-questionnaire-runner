from datetime import datetime, timezone

import pytest
from dateutil.relativedelta import relativedelta

from app.questionnaire.routing.operations import Operations
from app.questionnaire.routing.operator import Operator
from app.questionnaire.rules import convert_to_datetime

current_date = datetime.now(timezone.utc)
current_date_as_yyyy_mm_dd = current_date.strftime("%Y-%m-%d")
current_date_as_yyyy_mm = current_date.strftime("%Y-%m")
current_date_as_yyyy = current_date.strftime("%Y")

next_week = current_date + relativedelta(weeks=1)

equals_operations = [
    # Test True
    [(0.5, 0.5), True],
    [(1.0, 1), True],
    [(3, 3), True],
    [("Yes", "Yes"), True],
    [("CaseInsensitive", "caseInsensitive"), True],
    [(None, None), True],
    [(True, True), True],
    [(current_date, current_date), True],
    # Test False
    [(0.5, 0.7), False],
    [(1.0, 3), False],
    [(3, 7), False],
    [("Yes", "No"), False],
    [(None, 1), False],
    [(True, False), False],
    [(current_date, next_week), False],
]


@pytest.mark.parametrize(
    "operands, expected_result",
    equals_operations,
)
def test_operation_equal(operands, expected_result):
    operation = get_operations(Operator.EQUAL)
    operator = Operator(Operator.EQUAL, operation)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    equals_operations,
)
def test_operation_not_equal(operands, expected_result):
    operation = get_operations(Operator.NOT_EQUAL)
    operator = Operator(Operator.NOT_EQUAL, operation)
    assert operator.evaluate(operands) is not expected_result


greater_than_and_less_than_operations = [
    # Test True
    [(0.7, 0.5), True],
    [(2, 1.0), True],
    [(7, 3), True],
    [(next_week, current_date), True],
    # Test False
    [(0.5, 0.7), False],
    [(1.0, 2), False],
    [(3, 7), False],
    [(current_date, next_week), False],
]

greater_than_and_less_than_operations_equals = [
    [(1, 1), False],
    [(current_date, current_date), False],
]


@pytest.mark.parametrize(
    "operands, expected_result",
    greater_than_and_less_than_operations,
)
def test_operation_greater_than(operands, expected_result):
    operation = get_operations(Operator.GREATER_THAN)
    operator = Operator(Operator.GREATER_THAN, operation)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    greater_than_and_less_than_operations_equals,
)
def test_operation_greater_than_same_number(operands, expected_result):
    operation = get_operations(Operator.GREATER_THAN)
    operator = Operator(Operator.GREATER_THAN, operation)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    greater_than_and_less_than_operations,
)
def test_operation_less_than(operands, expected_result):
    operation = get_operations(Operator.LESS_THAN)
    operator = Operator(Operator.LESS_THAN, operation)
    assert operator.evaluate(operands) is not expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    greater_than_and_less_than_operations_equals,
)
def test_operation_less_than_same_number(operands, expected_result):
    operation = get_operations(Operator.LESS_THAN)
    operator = Operator(Operator.LESS_THAN, operation)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    [
        # Test True
        [(0.5, 0.7), True],
        [(1.0, 2), True],
        [(3, 7), True],
        [(0.5, 0.5), True],
        [(1.0, 1), True],
        [(3, 3), True],
        [(current_date, current_date), True],
        [(current_date, next_week), True],
        # Test False
        [(0.7, 0.5), False],
        [(2, 1.0), False],
        [(7, 3), False],
        [(next_week, current_date), False],
    ],
)
def test_operation_less_than_or_equal(operands, expected_result):
    operation = get_operations(Operator.LESS_THAN_OR_EQUAL)
    operator = Operator(Operator.LESS_THAN_OR_EQUAL, operation)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    [
        # Test True
        [(0.7, 0.5), True],
        [(2, 1.0), True],
        [(7, 3), True],
        [(0.5, 0.5), True],
        [(1.0, 1), True],
        [(3, 3), True],
        [(current_date, current_date), True],
        [(next_week, current_date), True],
        # Test False
        [(0.5, 0.7), False],
        [(1.0, 2), False],
        [(3, 7), False],
        [(current_date, next_week), False],
    ],
)
def test_operation_greater_than_or_equal(operands, expected_result):
    operation = get_operations(Operator.GREATER_THAN_OR_EQUAL)
    operator = Operator(
        Operator.GREATER_THAN_OR_EQUAL,
        operation,
    )
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize("operand, expected_result", [[False, True], [True, False]])
def test_operation_not(operand, expected_result):
    operation = get_operations(Operator.NOT)
    operator = Operator(Operator.NOT, operation)
    assert operator.evaluate([operand]) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    [
        # Test True
        [(True, True), True],
        [(True, True, True, True), True],
        [(True, False), False],
        # Test False
        [(False, True, True, True), False],
    ],
)
def test_operation_and(operands, expected_result):
    operation = get_operations(Operator.AND)
    operator = Operator(Operator.AND, operation)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    [
        # Test True
        [(True, True), True],
        [(True, True, True, True), True],
        [(True, False), True],
        [(False, False, False, True), True],
        # Test False
        [(False, False), False],
    ],
)
def test_operation_or(operands, expected_result):
    operation = get_operations(Operator.OR)
    operator = Operator(Operator.OR, operation)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    [
        # Test True
        [("Yes", ["Yes", "No"]), True],
        [("CaseInsensitive", ["caseInsensitive", "Other"]), True],
        [(0.5, [0.5, 1]), True],
        [(1, [1, 3]), True],
        [(None, [None, 1]), True],
        # Test False
        [("Yes", ["Nope", "No"]), False],
        [(0.5, [0.3, 1]), False],
        [(1, [1.5, 3]), False],
        [(None, ["Yes", "No"]), False],
    ],
)
def test_operation_in(operands, expected_result):
    operation = get_operations(Operator.IN)
    operator = Operator(Operator.IN, operation)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    [
        # Test True
        [(["Yes", "No"], ["Yes", "No", "Okay"]), True],
        [(["CaseInsensitive", "other"], ["caseInsensitive", "Other"]), True],
        [([0.5], [0.5, 1]), True],
        [([1, 3, 5], [5, 3, 1, 7]), True],
        [([None, 1], [1, None, 3]), True],
        [(["Yes", "No"], ("Yes", "No")), True],
        # Test False
        [(["Yes", "No"], ["Nope", "No"]), False],
        [([0.5, 1], [0.3, 1]), False],
        [([1, 1.5, 3, 5], [1.5, 3, 5, 7]), False],
        [([None, "No"], ["Yes", "No"]), False],
    ],
)
def test_operation_all_in(operands, expected_result):
    operation = get_operations(Operator.ALL_IN)
    operator = Operator(Operator.ALL_IN, operation)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    [
        # Test True
        [(["Yes", "No"], ["Yes", "No", "Okay"]), True],
        [(["CaseInsensitive", "other"], ["No", "Other"]), True],
        [([0.5], [0.5, 1]), True],
        [([0, 3, 10], [5, 3, 1, 7]), True],
        [([None, 10], [1, None, 3]), True],
        # Test False
        [(["Yes", "Okay"], ["Nope", "No"]), False],
        [([0.5, 3], [0.3, 1]), False],
        [([1, 10, 100, 500], [1.5, 3, 5, 7]), False],
        [([None, 0], ["Yes", "No"]), False],
    ],
)
def test_operation_any_in(operands, expected_result):
    operation = get_operations(Operator.ANY_IN)
    operator = Operator(Operator.ANY_IN, operation)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "date_string",
    [None, current_date_as_yyyy_mm_dd, current_date_as_yyyy_mm, current_date_as_yyyy],
)
@pytest.mark.parametrize(
    "offset",
    [
        None,
        {"days": -1},
        {"months": -1},
        {"years": -1},
        {"days": -1, "months": 1, "years": -1},
        {"days": 1},
        {"months": 1},
        {"years": 1},
        {"days": 1, "months": -1, "years": 1},
    ],
)
def test_operation_date(date_string: str, offset):
    operands = (date_string, offset)
    operation = get_operations(Operator.DATE)
    operator = Operator(Operator.DATE, operation)

    offset = offset or {}
    expected_result = (
        convert_to_datetime(date_string).date()
        + relativedelta(
            days=offset.get("days", 0),
            months=offset.get("months", 0),
            years=offset.get("years", 0),
        )
        if date_string
        else None
    )

    assert operator.evaluate(operands) == expected_result


@pytest.mark.parametrize(
    "operands",
    [
        [None, 2],
        [2, None],
        [None, None],
    ],
)
@pytest.mark.parametrize(
    "operator_name",
    [
        Operator.GREATER_THAN,
        Operator.GREATER_THAN_OR_EQUAL,
        Operator.LESS_THAN,
        Operator.LESS_THAN_OR_EQUAL,
    ],
)
def test_nonetype_operands_for_comparison_operators(operator_name, operands):
    operation = get_operations(operator_name)
    operator = Operator(operator_name, operation)
    assert operator.evaluate(operands) is False


@pytest.mark.parametrize(
    "operands",
    [
        [None, ["Yes"]],
        [["Yes"], None],
        [None, None],
    ],
)
@pytest.mark.parametrize(
    "operator_name",
    [
        Operator.ALL_IN,
        Operator.ANY_IN,
        Operator.IN,
    ],
)
def test_nonetype_operands_for_array_operators(operator_name, operands):
    operation = get_operations(operator_name)
    operator = Operator(operator_name, operation)
    assert operator.evaluate(operands) is False


@pytest.mark.parametrize(
    "operands, expected_result",
    [
        ([("tuple element 1", "tuple element 2")], 2),
        ([["list element 1", "list element 2"]], 2),
        ([[]], 0),
        ([None], 0),
    ],
)
def test_operation_count(operands, expected_result):
    operation = get_operations(Operator.COUNT)
    operator = Operator(Operator.COUNT, operation)
    assert operator.evaluate(operands) is expected_result


def get_operations(operator):
    operations = Operations()
    operation_mapping = {
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
    return operation_mapping[operator]
