from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Iterable, Optional, Sequence, Sized, TypeVar, Union

from dateutil.relativedelta import relativedelta

from app.questionnaire.routing.helpers import ValueTypes, casefold
from app.questionnaire.rules import convert_to_datetime

ComparableValue = TypeVar("ComparableValue", str, int, float, Decimal, date)
NonArrayPrimitiveTypes = Union[str, int, float, Decimal, None]


class Operations:
    """
    A class to group the operations
    """

    @staticmethod
    @casefold
    def evaluate_equal(lhs: ValueTypes, rhs: ValueTypes) -> bool:
        return lhs == rhs

    @staticmethod
    @casefold
    def evaluate_not_equal(lhs: ValueTypes, rhs: ValueTypes) -> bool:
        return lhs != rhs

    @staticmethod
    def evaluate_greater_than(lhs: ComparableValue, rhs: ComparableValue) -> bool:
        return lhs > rhs

    @staticmethod
    def evaluate_greater_than_or_equal(
        lhs: ComparableValue, rhs: ComparableValue
    ) -> bool:
        return lhs >= rhs

    @staticmethod
    def evaluate_less_than(lhs: ComparableValue, rhs: ComparableValue) -> bool:
        return lhs < rhs

    @staticmethod
    def evaluate_less_than_or_equal(lhs: ComparableValue, rhs: ComparableValue) -> bool:
        return lhs <= rhs

    @staticmethod
    def evaluate_not(value: bool) -> bool:
        return not value

    @staticmethod
    def evaluate_and(values: Iterable[bool]) -> bool:
        return all(iter(values))

    @staticmethod
    def evaluate_or(values: Iterable[bool]) -> bool:
        return any(iter(values))

    @staticmethod
    def evaluate_count(values: Optional[Sized]) -> int:
        return len(values or [])

    @staticmethod
    @casefold
    def evaluate_in(lhs: NonArrayPrimitiveTypes, rhs: Sequence) -> bool:
        """
        The NoneType check for rhs is done inline because this supports operations such as `None in [None, "Yes"]`
        which is the short form of `value == None or value == "Yes"`.
        """
        return rhs is not None and lhs in rhs

    @staticmethod
    @casefold
    def evaluate_all_in(lhs: Sequence, rhs: Sequence) -> bool:
        return all(x in rhs for x in lhs)

    @staticmethod
    @casefold
    def evaluate_any_in(lhs: Sequence, rhs: Sequence) -> bool:
        return any(x in rhs for x in lhs)

    @staticmethod
    def resolve_date_from_string(
        date_string: Optional[str], offset: Optional[dict[str, int]] = None
    ) -> Optional[date]:
        datetime_value = (
            datetime.now(timezone.utc)
            if date_string == "now"
            else convert_to_datetime(date_string)
        )
        value_as_date = datetime_value.date() if datetime_value else None

        if offset and value_as_date:
            value_as_date += relativedelta(
                days=offset.get("days", 0),
                months=offset.get("months", 0),
                years=offset.get("years", 0),
            )

        return value_as_date
