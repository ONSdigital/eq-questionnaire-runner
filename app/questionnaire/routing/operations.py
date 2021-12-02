from datetime import date
from decimal import Decimal
from typing import Iterable, Optional, Sequence, Sized, TypedDict, TypeVar, Union

from babel.dates import format_datetime
from dateutil.relativedelta import relativedelta

from app.questionnaire.routing.helpers import ValueTypes, casefold
from app.questionnaire.routing.utils import parse_datetime
from app.settings import DEFAULT_LOCALE

ComparableValue = TypeVar("ComparableValue", str, int, float, Decimal, date)
NonArrayPrimitiveTypes = Union[str, int, float, Decimal, None]

DAYS_OF_WEEK = {
    "MONDAY": 0,
    "TUESDAY": 1,
    "WEDNESDAY": 2,
    "THURSDAY": 3,
    "FRIDAY": 4,
    "SATURDAY": 5,
    "SUNDAY": 6,
}


class DateOffset(TypedDict, total=False):
    days: int
    months: int
    years: int
    day_of_week: str


class Operations:
    """
    A class to group the operations
    """

    def __init__(self, language: str) -> None:
        self._language = language
        self._locale = DEFAULT_LOCALE if language in ["en", "eo"] else language

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
        date_string: Optional[str],
        offset: Optional[DateOffset] = None,
        offset_by_full_weeks: bool = False,
    ) -> Optional[date]:
        datetime_value = parse_datetime(date_string)
        if not datetime_value:
            return None

        value_as_date = datetime_value.date()

        if offset:
            days_offset = offset.get("days", 0)

            if day_of_week_offset := offset.get("day_of_week"):
                if 0 > days_offset > -7:
                    raise ValueError(
                        "Negative days offset must be less than or equal to -7 when used with `day_of_week` offset"
                    )

                days_difference = (
                    value_as_date.weekday() - DAYS_OF_WEEK[day_of_week_offset]
                )
                days_to_reduce = days_difference % 7

                if not offset_by_full_weeks and (
                    days_offset < 0 and days_difference < 0
                ):
                    # A negative day difference means that the `day_of_week` offset went back to the previous week;
                    # therefore, if we also have a negative days offset,
                    # then the no. of days we reduce the offset by must be adjusted by 7 to prevent going back two weeks.
                    days_to_reduce -= 7

                days_offset -= days_to_reduce

            value_as_date += relativedelta(
                days=days_offset,
                months=offset.get("months", 0),
                years=offset.get("years", 0),
            )

        return value_as_date

    @staticmethod
    def date_range(start_date: date, days_in_range: int) -> list[date]:
        return [(start_date + relativedelta(days=i)) for i in range(days_in_range)]

    def format_date(self, date_to_format: date, date_format: str) -> str:
        formatted_date: str = format_datetime(
            date_to_format, date_format, locale=self._locale
        )
        return formatted_date
