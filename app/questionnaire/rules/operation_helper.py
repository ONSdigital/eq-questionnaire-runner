"""
Operations.py can't be used in placeholder_transformer due to circular reference issue
these methods will be temporarily placed here and are duplicated from operations.py,
they will be moved back to operations once placeholder is refactored
"""
from datetime import date
from typing import Optional, TypedDict

from dateutil.relativedelta import relativedelta

from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.rules.operations import Operations
from app.questionnaire.rules.utils import parse_datetime

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

            days_difference = value_as_date.weekday() - DAYS_OF_WEEK[day_of_week_offset]
            days_to_reduce = days_difference % 7

            if not offset_by_full_weeks and (days_offset < 0 and days_difference < 0):
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


def get_option_label_from_value(
    schema: QuestionnaireSchema, language: str, renderer, value: str, answer_id: str
) -> str:
    ops = Operations(language, schema, renderer)
    return ops.evaluate_option_label_from_value(value, answer_id)
