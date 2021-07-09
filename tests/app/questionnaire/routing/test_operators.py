from datetime import datetime, timedelta

import pytest
from dateutil.relativedelta import relativedelta

from app.questionnaire.routing.helpers import datetime_as_midnight
from app.questionnaire.routing.operator import Operator
from app.questionnaire.rules import convert_to_datetime

now = datetime.utcnow()
now_as_yyyy_mm_dd = now.strftime("%Y-%m-%d")
now_as_yyyy_mm = now.strftime("%Y-%m")
now_as_yyyy = now.strftime("%Y")

test_data_equals_operation_numeric_and_date_matching_values = [
    [(0.5, 0.5), True],
    [(1.0, 1), True],
    [(3, 3), True],
    [(now, now), True],
]

test_data_equals_operation_numeric_and_date = [
    *test_data_equals_operation_numeric_and_date_matching_values,
    [(0.5, 0.7), False],
    [(1.0, 3), False],
    [(3, 7), False],
    [(now, datetime.utcnow()), False],
]

equals_operations = [
    *test_data_equals_operation_numeric_and_date,
    [("Yes", "Yes"), True],
    [("CaseInsensitive", "caseInsensitive"), True],
    [(None, None), True],
    [(True, True), True],
    [("Yes", "No"), False],
    [(None, 1), False],
    [(True, False), False],
]

test_data_greater_than_less_than_operations = [
    [(0.7, 0.5), True],
    [(2, 1.0), True],
    [(7, 3), True],
    [(datetime.utcnow(), now), True],
    [(0.5, 0.7), False],
    [(1.0, 2), False],
    [(3, 7), False],
    [(now, datetime.utcnow()), False],
]


@pytest.mark.parametrize(
    "operands, expected_result",
    equals_operations,
)
def test_operation_equal(operands, expected_result):
    operator = Operator(Operator.EQUAL)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    equals_operations,
)
def test_operation_not_equal(operands, expected_result):
    operator = Operator(Operator.NOT_EQUAL)
    assert operator.evaluate(operands) is not expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    test_data_greater_than_less_than_operations,
)
def test_operation_greater_than(operands, expected_result):
    operator = Operator(Operator.GREATER_THAN)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    [
        *test_data_greater_than_less_than_operations,
        *test_data_equals_operation_numeric_and_date_matching_values,
    ],
)
def test_operation_greater_than_or_equal(operands, expected_result):
    operator = Operator(Operator.GREATER_THAN_OR_EQUAL)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    test_data_greater_than_less_than_operations,
)
def test_operation_less_than(operands, expected_result):
    operator = Operator(Operator.LESS_THAN)
    assert operator.evaluate(operands) is not expected_result


@pytest.mark.parametrize(
    "operands, expected_result", test_data_greater_than_less_than_operations
)
def test_operation_less_than_or_equal_operands_equal(operands, expected_result):
    operator = Operator(Operator.LESS_THAN_OR_EQUAL)
    assert operator.evaluate(operands) is not expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    test_data_equals_operation_numeric_and_date_matching_values,
)
def test_operation_less_than_or_equal_operands_not_equal(operands, expected_result):
    operator = Operator(Operator.LESS_THAN_OR_EQUAL)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize("operand, expected_result", [[False, True], [True, False]])
def test_operation_not(operand, expected_result):
    operator = Operator(Operator.NOT)
    assert operator.evaluate([operand]) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    [
        [(True, True), True],
        [(True, True, True, True), True],
        [(True, False), False],
        [(False, True, True, True), False],
    ],
)
def test_operation_and(operands, expected_result):
    operator = Operator(Operator.AND)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    [
        [(True, True), True],
        [(True, True, True, True), True],
        [(True, False), True],
        [(False, False, False, True), True],
    ],
)
def test_operation_or(operands, expected_result):
    operator = Operator(Operator.OR)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    [
        [("Yes", ["Yes", "No"]), True],
        [("CaseInsensitive", ["caseInsensitive", "Other"]), True],
        [(0.5, [0.5, 1]), True],
        [(1, [1, 3]), True],
        [(None, [None, 1]), True],
        [("Yes", ["Nope", "No"]), False],
        [(0.5, [0.3, 1]), False],
        [(1, [1.5, 3]), False],
        [(None, ["Yes", "No"]), False],
    ],
)
def test_operation_in(operands, expected_result):
    operator = Operator(Operator.IN)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    [
        [(["Yes", "No"], ["Yes", "No", "Okay"]), True],
        [(["CaseInsensitive", "other"], ["caseInsensitive", "Other"]), True],
        [([0.5], [0.5, 1]), True],
        [([1, 3, 5], [5, 3, 1, 7]), True],
        [([None, 1], [1, None, 3]), True],
        [(["Yes", "No"], ["Nope", "No"]), False],
        [([0.5, 1], [0.3, 1]), False],
        [([1, 1.5, 3, 5], [1.5, 3, 5, 7]), False],
        [([None, "No"], ["Yes", "No"]), False],
    ],
)
def test_operation_all_in(operands, expected_result):
    operator = Operator(Operator.ALL_IN)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    [
        [(["Yes", "No"], ["Yes", "No", "Okay"]), True],
        [(["CaseInsensitive", "other"], ["No", "Other"]), True],
        [([0.5], [0.5, 1]), True],
        [([0, 3, 10], [5, 3, 1, 7]), True],
        [([None, 10], [1, None, 3]), True],
        [(["Yes", "Okay"], ["Nope", "No"]), False],
        [([0.5, 3], [0.3, 1]), False],
        [([1, 10, 100, 500], [1.5, 3, 5, 7]), False],
        [([None, 0], ["Yes", "No"]), False],
    ],
)
def test_operation_any_in(operands, expected_result):
    operator = Operator(Operator.ANY_IN)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "date_string",
    [None, now_as_yyyy_mm_dd, now_as_yyyy_mm, now_as_yyyy],
)
@pytest.mark.parametrize(
    "offset",
    [
        None,
        {"days": -1},
        {"months": -1},
        {"years": -1},
        {"days": -1, "months": -1, "years": -1},
        {"days": 1},
        {"months": 1},
        {"years": 1},
        {"days": 1, "months": 1, "years": 1},
    ],
)
def test_operation_date(date_string: str, offset):
    operands = (date_string, offset)
    operator = Operator(Operator.DATE)

    offset = offset or {}
    expected_result = (
        datetime_as_midnight(
            convert_to_datetime(date_string)
            + relativedelta(
                days=offset.get("days", 0),
                months=offset.get("months", 0),
                years=offset.get("years", 0),
            )
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
    operator = Operator(operator_name)
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
    "operator_name", [Operator.ALL_IN, Operator.ANY_IN, Operator.IN]
)
def test_nonetype_operands_for_array_operators(operator_name, operands):
    operator = Operator(operator_name)
    assert operator.evaluate(operands) is False
