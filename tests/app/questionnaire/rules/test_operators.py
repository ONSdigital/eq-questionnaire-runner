from datetime import date, datetime, timezone

import pytest
from dateutil.relativedelta import relativedelta
from freezegun import freeze_time

from app.questionnaire.rules.operations import Operations
from app.questionnaire.rules.operator import Operator
from app.questionnaire.when_rules import convert_to_datetime

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
    operator = get_operator(Operator.EQUAL)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    equals_operations,
)
def test_operation_not_equal(operands, expected_result):
    operator = get_operator(Operator.NOT_EQUAL)
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
    operator = get_operator(Operator.GREATER_THAN)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    greater_than_and_less_than_operations_equals,
)
def test_operation_greater_than_same_number(operands, expected_result):
    operator = get_operator(Operator.GREATER_THAN)
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    greater_than_and_less_than_operations,
)
def test_operation_less_than(operands, expected_result):
    operator = get_operator(Operator.LESS_THAN)
    assert operator.evaluate(operands) is not expected_result


@pytest.mark.parametrize(
    "operands, expected_result",
    greater_than_and_less_than_operations_equals,
)
def test_operation_less_than_same_number(operands, expected_result):
    operator = get_operator(Operator.LESS_THAN)
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
    operator = get_operator(Operator.LESS_THAN_OR_EQUAL)
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
    operator = get_operator(
        Operator.GREATER_THAN_OR_EQUAL,
    )
    assert operator.evaluate(operands) is expected_result


@pytest.mark.parametrize("operand, expected_result", [[False, True], [True, False]])
def test_operation_not(operand, expected_result):
    operator = get_operator(Operator.NOT)
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
    operator = get_operator(Operator.AND)
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
    operator = get_operator(Operator.OR)
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
    operator = get_operator(Operator.IN)
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
    operator = get_operator(Operator.ALL_IN)
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
    operator = get_operator(Operator.ANY_IN)
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
    operator = get_operator(Operator.DATE)

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
    "offset, expected_result",
    [
        # Last Thursday (Yesterday from reference date)
        ({"day_of_week": "THURSDAY"}, datetime(year=2020, month=12, day=31)),
        # Last Saturday
        ({"day_of_week": "SATURDAY"}, datetime(year=2020, month=12, day=26)),
        # Last Week Thursday
        (
            {"day_of_week": "THURSDAY", "days": -7},
            datetime(year=2020, month=12, day=24),
        ),
        # Last Week Saturday (Same as Last Saturday since reference date is a Friday)
        (
            {"day_of_week": "SATURDAY", "days": -7},
            datetime(year=2020, month=12, day=26),
        ),
        # Next Thursday / Next Week Thursday
        ({"day_of_week": "THURSDAY", "days": 7}, datetime(year=2021, month=1, day=7)),
        # Next Saturday (Tomorrow from reference date)
        ({"day_of_week": "SATURDAY", "days": 7}, datetime(year=2021, month=1, day=2)),
        # Next Week Saturday
        ({"day_of_week": "SATURDAY", "days": 14}, datetime(year=2021, month=1, day=9)),
        # 1 full week Thursday
        ({"day_of_week": "THURSDAY", "days": 14}, datetime(year=2021, month=1, day=14)),
    ],
)
def test_operation_date_offsets_literal_date(offset, expected_result):
    """
    This is to test a literal date instead of dynamically generating the expected date.

    Initial date: 2021-01-01 is a Friday
    """

    date_string = "2021-01-01"
    operands = (
        date_string,
        offset,
    )
    operator = get_operator(Operator.DATE)

    assert operator.evaluate(operands) == expected_result.date()


def test_operation_date_day_of_week_offsets_with_invalid_days_offset():
    date_string = "2021-01-01"
    operands = (
        date_string,
        {"day_of_week": "MONDAY", "days": -1},
    )
    operator = get_operator(Operator.DATE)

    with pytest.raises(ValueError):
        operator.evaluate(operands)


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
    operator = get_operator(operator_name)
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
    operator = get_operator(operator_name)
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
    operator = get_operator(Operator.COUNT)
    assert operator.evaluate(operands) is expected_result


@freeze_time("2021-01-01")
def test_date_range():
    operator = get_operator(Operator.DATE_RANGE)

    assert operator.evaluate([datetime.now(timezone.utc).date(), 3]) == [
        datetime(year=2021, month=1, day=1, tzinfo=timezone.utc).date(),
        datetime(year=2021, month=1, day=2, tzinfo=timezone.utc).date(),
        datetime(year=2021, month=1, day=3, tzinfo=timezone.utc).date(),
    ]


@freeze_time("2021-01-01")
@pytest.mark.parametrize(
    "date_format, expected_result",
    [
        ("EEEE d MMMM", "Friday 1 January"),
        ("EEEE d MMMM yyyy", "Friday 1 January 2021"),
        ("d MMMM yyyy", "1 January 2021"),
        ("yyyy-MM-dd", "2021-01-01"),
        ("yyyy-MM", "2021-01"),
        ("yyyy", "2021"),
    ],
)
def test_format_date(date_format, expected_result):
    operator = get_operator(Operator.FORMAT_DATE)

    assert (
        operator.evaluate([datetime.now(timezone.utc).date(), date_format])
        == expected_result
    )


def test_map_without_nested_date_operator():
    operator = get_operator(Operator.MAP)

    function = {Operator.FORMAT_DATE: ["self", "yyyy-MM-dd"]}
    iterables = [
        date(year=2021, month=1, day=1),
        date(year=2021, month=1, day=2),
        date(year=2021, month=1, day=3),
    ]

    assert operator.evaluate([function, iterables]) == [
        "2021-01-01",
        "2021-01-02",
        "2021-01-03",
    ]


def test_map_with_nested_date_operator():
    operator = get_operator(Operator.MAP)

    function = {
        Operator.FORMAT_DATE: [
            {
                Operator.DATE: [
                    "self",
                ]
            },
            "d MMMM yyyy",
        ]
    }
    iterables = ["2021-01-01", "2021-01-02", "2021-01-03"]

    assert operator.evaluate([function, iterables]) == [
        "1 January 2021",
        "2 January 2021",
        "3 January 2021",
    ]


def get_operator(operator_name, language="en"):
    return Operator(operator_name, operations=Operations(language=language))
