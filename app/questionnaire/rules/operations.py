from collections.abc import Sized
from copy import deepcopy
from datetime import date
from decimal import Decimal
from typing import (
    TYPE_CHECKING,
    Iterable,
    Mapping,
    Sequence,
    TypeAlias,
    TypedDict,
    TypeVar,
)

from babel.dates import format_datetime
from dateutil.relativedelta import relativedelta

from app.questionnaire import QuestionnaireSchema
from app.questionnaire.rules.helpers import ValueTypes, casefold
from app.questionnaire.rules.operator import OPERATION_MAPPING
from app.questionnaire.rules.utils import parse_datetime
from app.questionnaire.value_source_resolver import ValueSourceTypes
from app.settings import DEFAULT_LOCALE

if TYPE_CHECKING:
    from app.questionnaire.placeholder_renderer import (
        PlaceholderRenderer,  # pragma: no cover
    )

ComparableValue = TypeVar("ComparableValue", str, int, float, Decimal, date)
NonArrayPrimitiveTypes: TypeAlias = str | int | float | Decimal | None

DAYS_OF_WEEK = {
    "MONDAY": 0,
    "TUESDAY": 1,
    "WEDNESDAY": 2,
    "THURSDAY": 3,
    "FRIDAY": 4,
    "SATURDAY": 5,
    "SUNDAY": 6,
}

SELF_REFERENCE_KEY = "self"


class DateOffset(TypedDict, total=False):
    days: int
    months: int
    years: int
    day_of_week: str


class Operations:
    """
    A class to group the operations
    """

    NEGATIVE_DAYS_OFFSET_ERROR_MESSAGE  = "Negative days offset must be less than or equal to -7 when used with `day_of_week` offset"

    def __init__(
        self,
        language: str,
        schema: QuestionnaireSchema,
        renderer: "PlaceholderRenderer",
    ) -> None:
        self._language = language
        self._locale = DEFAULT_LOCALE if language in {"en", "eo"} else language
        self.renderer = renderer
        self.schema = schema

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
    def evaluate_count(values: Sized | None) -> int:
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
        date_string: str | None,
        offset: DateOffset | None = None,
        offset_by_full_weeks: bool = False,
    ) -> date | None:
        datetime_value = parse_datetime(date_string)
        if not datetime_value:
            return None

        value_as_date = datetime_value.date()

        if offset:
            days_offset = offset.get("days", 0)

            if day_of_week_offset := offset.get("day_of_week"):
                if 0 > days_offset > -7:
                    raise ValueError(Operations.NEGATIVE_DAYS_OFFSET_ERROR_MESSAGE )

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

    def _resolve_self_reference(
        self,
        self_reference_value: ValueSourceTypes | date,
        operands: Sequence[ValueSourceTypes | date],
    ) -> list[ValueSourceTypes | date]:
        resolved_operands = []
        for operand in operands:
            if isinstance(operand, dict) and QuestionnaireSchema.has_operator(operand):
                operator_name = next(iter(operand))
                resolved_nested_operands = self._resolve_self_reference(
                    self_reference_value, operand[operator_name]
                )
                resolved_value = getattr(self, OPERATION_MAPPING[operator_name])(
                    *resolved_nested_operands
                )
            else:
                resolved_value = (
                    self_reference_value if operand == SELF_REFERENCE_KEY else operand
                )

            resolved_operands.append(resolved_value)

        return resolved_operands

    def evaluate_map(
        self,
        function: Mapping[str, list],
        iterables: Sequence[ValueSourceTypes | date],
    ) -> list[str]:
        function_operator = next(iter(function))
        function_operands = deepcopy(function[function_operator])

        results = []
        for item in iterables:
            resolved_operands = self._resolve_self_reference(item, function_operands)

            results.append(
                getattr(self, OPERATION_MAPPING[function_operator])(*resolved_operands)
            )

        return results

    def evaluate_option_label_from_value(self, value: str, answer_id: str) -> str:
        answers = self.schema.get_answers_by_answer_id(answer_id)
        label_options: str | dict = [
            options["label"]
            for answer in answers
            for options in answer["options"]
            if value == options["value"]
        ][0]

        if isinstance(label_options, str):
            label = label_options

        else:
            label = self.renderer.render_placeholder(label_options, list_item_id=None)
        return label

    def evaluate_sum(self, *args: tuple) -> int | float | Decimal:
        """recursively evaluate the sum of any list-like arguments"""
        return sum(
            # Cannot use Iterable or Sequence as the type check for value as this would include primitive types like str
            self.evaluate_sum(*value) if isinstance(value, (list, tuple)) else value
            for value in args
            if isinstance(value, (int, float, Decimal, list, tuple))
        )
