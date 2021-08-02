from datetime import datetime
from decimal import Decimal
from typing import Iterable, Optional, Sequence, TypeVar, Union

from dateutil.relativedelta import relativedelta

from app.questionnaire.routing.helpers import ValueTypes, casefold, datetime_as_midnight
from app.questionnaire.rules import convert_to_datetime

ComparableValue = TypeVar("ComparableValue", str, int, float, Decimal, datetime)
NonArrayPrimitiveTypes = Union[str, int, float, Decimal, None]


@casefold
def evaluate_equal(lhs: ValueTypes, rhs: ValueTypes) -> bool:
    return lhs == rhs


@casefold
def evaluate_not_equal(lhs: ValueTypes, rhs: ValueTypes) -> bool:
    return lhs != rhs


def evaluate_greater_than(lhs: ComparableValue, rhs: ComparableValue) -> bool:
    return lhs > rhs


def evaluate_greater_than_or_equal(lhs: ComparableValue, rhs: ComparableValue) -> bool:
    return lhs >= rhs


def evaluate_less_than(lhs: ComparableValue, rhs: ComparableValue) -> bool:
    return lhs < rhs


def evaluate_less_than_or_equal(lhs: ComparableValue, rhs: ComparableValue) -> bool:
    return lhs <= rhs


def evaluate_not(value: bool) -> bool:
    return not value


def evaluate_and(values: Iterable[bool]) -> bool:
    return all(iter(values))


def evaluate_or(values: Iterable[bool]) -> bool:
    return any(iter(values))


@casefold
def evaluate_in(lhs: NonArrayPrimitiveTypes, rhs: Sequence) -> bool:
    return rhs is not None and lhs in rhs


@casefold
def evaluate_all_in(lhs: Sequence, rhs: Sequence) -> bool:
    return all(x in rhs for x in lhs)


@casefold
def evaluate_any_in(lhs: Sequence, rhs: Sequence) -> bool:
    return any(x in rhs for x in lhs)


def resolve_datetime_from_string(
    date_string: Optional[str], offset: Optional[dict[str, int]] = None
) -> Optional[datetime]:
    value = (
        datetime_as_midnight(datetime.utcnow())
        if date_string == "now"
        else convert_to_datetime(date_string)
    )

    if offset and value:
        value += relativedelta(
            days=offset.get("days", 0),
            months=offset.get("months", 0),
            years=offset.get("years", 0),
        )

    return value
