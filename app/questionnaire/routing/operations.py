from datetime import datetime
from typing import Iterable, Optional, Sequence, Union

from dateutil.relativedelta import relativedelta

from app.questionnaire.routing.helpers import casefold, datetime_as_midnight
from app.questionnaire.rules import convert_to_datetime

answer_types = Union[bool, str, int, float, None, datetime]


def _are_non_none_operands(*operands: Union[Sequence, answer_types]) -> bool:
    return all(operand is not None for operand in operands)


@casefold
def evaluate_equal(lhs: answer_types, rhs: answer_types) -> bool:
    return lhs == rhs


@casefold
def evaluate_not_equal(lhs: answer_types, rhs: answer_types) -> bool:
    return lhs != rhs


def evaluate_greater_than(lhs: answer_types, rhs: answer_types) -> bool:
    return _are_non_none_operands(lhs, rhs) and lhs > rhs  # type: ignore


def evaluate_greater_than_or_equal(lhs: answer_types, rhs: answer_types) -> bool:
    return _are_non_none_operands(lhs, rhs) and lhs >= rhs  # type: ignore


def evaluate_less_than(lhs: answer_types, rhs: answer_types) -> bool:
    return _are_non_none_operands(lhs, rhs) and lhs < rhs  # type: ignore


def evaluate_less_than_or_equal(lhs: answer_types, rhs: answer_types) -> bool:
    return _are_non_none_operands(lhs, rhs) and lhs <= rhs  # type: ignore


def evaluate_not(value: bool) -> bool:
    return not value


def evaluate_and(values: Iterable[bool]) -> bool:
    return all(iter(values))


def evaluate_or(values: Iterable[bool]) -> bool:
    return any(iter(values))


@casefold
def evaluate_in(lhs: Union[str, int, float, None], rhs: Sequence) -> bool:
    return _are_non_none_operands(rhs) and lhs in rhs


@casefold
def evaluate_all_in(lhs: Sequence, rhs: Sequence) -> bool:
    return _are_non_none_operands(lhs, rhs) and all(x in rhs for x in lhs)


@casefold
def evaluate_any_in(lhs: Sequence, rhs: Sequence) -> bool:
    return _are_non_none_operands(lhs, rhs) and any(x in rhs for x in lhs)


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
