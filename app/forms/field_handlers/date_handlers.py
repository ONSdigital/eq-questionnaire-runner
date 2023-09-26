from datetime import datetime, timezone
from functools import cached_property
from typing import Any, Optional, Union

from dateutil.relativedelta import relativedelta

from app.forms.field_handlers.field_handler import FieldHandler
from app.forms.fields import DateField, MonthYearDateField, YearDateField
from app.forms.validators import (
    DateCheck,
    DateRequired,
    OptionalForm,
    SingleDatePeriodCheck,
    format_message_with_title,
)
from app.questionnaire.rules.utils import parse_datetime

DateValidatorTypes = list[
    Union[OptionalForm, DateRequired, DateCheck, SingleDatePeriodCheck]
]


class DateHandler(FieldHandler):
    MANDATORY_MESSAGE_KEY = "MANDATORY_DATE"
    DATE_FORMAT = "yyyy-mm-dd"
    DISPLAY_FORMAT = "d MMMM yyyy"

    @cached_property
    def validators(self) -> DateValidatorTypes:
        validate_with: DateValidatorTypes = [OptionalForm()]

        if self.answer_schema["mandatory"] is True:
            validate_with = [
                DateRequired(
                    message=self.get_validation_message(
                        format_message_with_title(
                            self.MANDATORY_MESSAGE_KEY, self.question_title
                        )
                    )
                )
            ]

        error_message = self.get_validation_message("INVALID_DATE")

        validate_with.append(DateCheck(error_message))

        minimum_date = self.get_date_value("minimum")
        maximum_date = self.get_date_value("maximum")

        if minimum_date or maximum_date:
            min_max_validator = self.get_min_max_validator(minimum_date, maximum_date)
            validate_with.append(min_max_validator)
        return validate_with

    def get_field(self) -> DateField:
        return DateField(
            validators=self.validators, label=self.label, description=self.guidance
        )

    def get_min_max_validator(
        self, minimum_date: Optional[datetime], maximum_date: Optional[datetime]
    ) -> SingleDatePeriodCheck:
        messages = self.answer_schema.get("validation", {}).get("messages")

        return SingleDatePeriodCheck(
            messages=messages,
            date_format=self.DISPLAY_FORMAT,
            minimum_date=minimum_date,
            maximum_date=maximum_date,
        )

    def get_referenced_date(self, key: str) -> Optional[datetime]:
        """
        Gets value of the referenced date type, whether it is a value,
        id of an answer or a meta date.

        :return: date value
        """
        value: Any = self.get_schema_value(self.answer_schema[key])

        if value == "now":
            value = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        return parse_datetime(value) if isinstance(value, str) else None

    @staticmethod
    def transform_date_by_offset(
        date_to_offset: Optional[datetime], offset: dict[str, int]
    ) -> Optional[datetime]:
        """
        Adds/subtracts offset from a date and returns
        the new offset value

        :param date_to_offset: The date to offset
        :param offset: The object which contains the offset.
        :return: date value
        """
        if date_to_offset:
            date_to_offset += relativedelta(
                years=offset.get("years", 0),
                months=offset.get("months", 0),
                days=offset.get("days", 0),
            )

        return date_to_offset

    def get_date_value(self, key: str) -> Optional[datetime]:
        """
        Gets attributes within a minimum or maximum of a date field and validates that the entered date
        is valid.
        """
        date_value = None

        if key in self.answer_schema:
            date_value = self.get_referenced_date(key)

            if "offset_by" in self.answer_schema[key]:
                offset = self.answer_schema[key]["offset_by"]
                date_value = self.transform_date_by_offset(date_value, offset)

        return date_value


class MonthYearDateHandler(DateHandler):
    DATE_FORMAT = "yyyy-mm"
    DISPLAY_FORMAT = "MMMM yyyy"

    def get_field(self) -> MonthYearDateField:
        return MonthYearDateField(
            validators=self.validators, label=self.label, description=self.guidance
        )

    def get_min_max_validator(
        self, minimum_date: Optional[datetime], maximum_date: Optional[datetime]
    ) -> SingleDatePeriodCheck:
        messages = self.answer_schema.get("validation", {}).get("messages")

        minimum_date = (
            minimum_date.replace(day=1) if minimum_date else None
        )  # First day of Month
        maximum_date = (
            maximum_date + relativedelta(day=31) if maximum_date else None
        )  # Last day of month

        return SingleDatePeriodCheck(
            messages=messages,
            date_format=self.DISPLAY_FORMAT,
            minimum_date=minimum_date,
            maximum_date=maximum_date,
        )


class YearDateHandler(DateHandler):
    DATE_FORMAT = "yyyy"
    DISPLAY_FORMAT = "yyyy"

    def get_field(self) -> YearDateField:
        return YearDateField(
            validators=self.validators, label=self.label, description=self.guidance
        )

    def get_min_max_validator(
        self, minimum_date: Optional[datetime], maximum_date: Optional[datetime]
    ) -> SingleDatePeriodCheck:
        messages = self.answer_schema.get("validation", {}).get("messages")

        minimum_date = (
            minimum_date.replace(month=1, day=1) if minimum_date else None
        )  # January 1st
        maximum_date = (
            maximum_date.replace(month=12, day=31) if maximum_date else None
        )  # Last day of december

        return SingleDatePeriodCheck(
            messages=messages,
            date_format=self.DISPLAY_FORMAT,
            minimum_date=minimum_date,
            maximum_date=maximum_date,
        )
