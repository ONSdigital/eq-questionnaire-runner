from __future__ import annotations

import math
import re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import TYPE_CHECKING, Iterable, List, Mapping, Optional, Sequence, Union

import flask_babel
from babel import numbers
from dateutil.relativedelta import relativedelta
from flask_babel import ngettext
from flask_wtf import FlaskForm
from structlog import get_logger
from wtforms import Field, StringField, validators

from app.forms import error_messages
from app.forms.fields import (
    DateField,
    DecimalFieldWithSeparator,
    IntegerFieldWithSeparator,
)
from app.helpers.form_helpers import (
    format_message_with_title,
    format_playback_value,
    sanitise_mobile_number,
    sanitise_number,
)
from app.questionnaire.questionnaire_store_updater import QuestionnaireStoreUpdater
from app.questionnaire.rules.utils import parse_datetime

if TYPE_CHECKING:
    from app.forms.questionnaire_form import QuestionnaireForm  # pragma: no cover

logger = get_logger()

tld_part_regex = re.compile(
    r"^([a-z]{2,63}|xn--([a-z0-9]+-)*[a-z0-9]+)$", re.IGNORECASE
)
email_regex = re.compile(r"^.+@([^.@][^@\s]+)$")

OptionalMessage = Optional[Mapping[str, str]]
NumType = Union[int, Decimal]
PeriodType = Mapping[str, int]


class NumberCheck:
    def __init__(self, message: Optional[str] = None):
        self.message = message or error_messages["INVALID_NUMBER"]

    def __call__(
        self,
        form: FlaskForm,
        field: Union[DecimalFieldWithSeparator, IntegerFieldWithSeparator],
    ) -> None:
        try:
            # number is sanitised to guard against inputs like `,NaN_` etc
            number = Decimal(sanitise_number(number=field.raw_data[0]))
        except (ValueError, TypeError, InvalidOperation, AttributeError) as exc:
            raise validators.StopValidation(self.message) from exc

        if "e" in field.raw_data[0].lower() or math.isnan(number):
            raise validators.StopValidation(self.message)


class ResponseRequired:
    """
    Validates that input was provided for this field. This is a copy of the
    InputRequired validator provided by wtforms, which checks that form-input data
    was provided, but additionally adds a kwarg to strip whitespace, as is available
    on the Optional() validator wtforms provides. Oddly, stripping whitespace is not
    an option for DataRequired or InputRequired validators in wtforms.
    """

    field_flags = ("required",)

    def __init__(self, message: str, strip_whitespace: bool = True):
        self.message = message

        if strip_whitespace:
            self.string_check = lambda s: s.strip()
        else:
            self.string_check = lambda s: s

    def __call__(self, form: "QuestionnaireForm", field: Field) -> None:
        if (
            not field.raw_data
            or not field.raw_data[0]
            or not self.string_check(field.raw_data[0])
        ):
            field.errors[:] = []
            raise validators.StopValidation(self.message)


class NumberRange:
    """
    Validates that a number is of a minimum and/or maximum value, inclusive.
    This will work with any comparable number type, such as floats and
    decimals, not just integers.

    :param minimum:
        The minimum required value of the number. If not provided, minimum
        value will not be checked.
    :param maximum:
        The maximum value of the number. If not provided, maximum value
        will not be checked.
    """

    def __init__(
        self,
        minimum: Optional[NumType] = None,
        minimum_exclusive: bool = False,
        maximum: Optional[NumType] = None,
        maximum_exclusive: bool = False,
        messages: OptionalMessage = None,
        currency: Optional[str] = None,
    ):
        self.minimum = minimum
        self.maximum = maximum
        self.minimum_exclusive = minimum_exclusive
        self.maximum_exclusive = maximum_exclusive
        self.messages: Mapping[str, str] = {**error_messages, **(messages or {})}
        self.currency = currency

    def __call__(
        self,
        form: "QuestionnaireForm",
        field: Union[DecimalFieldWithSeparator, IntegerFieldWithSeparator],
    ) -> None:
        value: int | Decimal | None = field.data

        if value is not None:
            decimal_limit = (
                field.places if isinstance(field, DecimalFieldWithSeparator) else None
            )

            if error_message := self.validate_minimum(
                value=value, decimal_limit=decimal_limit
            ) or self.validate_maximum(value=value, decimal_limit=decimal_limit):
                raise validators.ValidationError(error_message)

    def validate_minimum(
        self, *, value: NumType, decimal_limit: int | None
    ) -> Optional[str]:
        if self.minimum is None:
            return None

        minimum_value = format_playback_value(
            value=self.minimum,
            currency=self.currency,
            decimal_limit=decimal_limit,
        )

        if self.minimum_exclusive and value <= self.minimum:
            return self.messages["NUMBER_TOO_SMALL_EXCLUSIVE"] % {"min": minimum_value}

        if value < self.minimum:
            return self.messages["NUMBER_TOO_SMALL"] % {"min": minimum_value}

        return None

    def validate_maximum(
        self, *, value: NumType, decimal_limit: int | None
    ) -> Optional[str]:
        if self.maximum is None:
            return None

        maximum_value = format_playback_value(
            value=self.maximum,
            currency=self.currency,
            decimal_limit=decimal_limit,
        )

        if self.maximum_exclusive and value >= self.maximum:
            return self.messages["NUMBER_TOO_LARGE_EXCLUSIVE"] % {"max": maximum_value}
        if value > self.maximum:
            return self.messages["NUMBER_TOO_LARGE"] % {"max": maximum_value}

        return None


class DecimalPlaces:
    """
    Validates that an input has less than or equal to a
    set number of decimal places

    :param max_decimals:
        The maximum allowed number of decimal places.
    """

    def __init__(self, max_decimals: int = 0, messages: OptionalMessage = None):
        self.max_decimals = max_decimals
        self.messages = {**error_messages, **(messages or {})}

    def __call__(
        self, form: "QuestionnaireForm", field: DecimalFieldWithSeparator
    ) -> None:
        data = sanitise_number(field.raw_data[0])
        decimal_symbol = numbers.get_decimal_symbol(flask_babel.get_locale())
        if data and decimal_symbol in data:
            if self.max_decimals == 0:
                raise validators.ValidationError(self.messages["INVALID_INTEGER"])
            if len(data.split(decimal_symbol)[1]) > self.max_decimals:
                raise validators.ValidationError(
                    self.messages["INVALID_DECIMAL"] % {"max": self.max_decimals}
                )


class OptionalForm:
    """
    Allows completely empty form and stops the validation chain from continuing.
    Will not stop the validation chain if any one of the fields is populated.
    """

    field_flags = ("optional",)

    def __call__(self, form: Sequence["QuestionnaireForm"], field: Field) -> None:
        empty_form = True

        for formfield in form:
            has_raw_data = hasattr(formfield, "raw_data")

            is_empty = has_raw_data and len(formfield.raw_data) == 0
            is_blank = (
                has_raw_data
                and len(formfield.raw_data) >= 1
                and isinstance(formfield.raw_data[0], str)
                and not formfield.raw_data[0]
            )

            # By default we'll receive empty arrays for values not posted, so need to allow empty lists
            empty_field = True if is_empty else is_blank

            empty_form &= empty_field

        if empty_form:
            raise validators.StopValidation()


class DateRequired:
    field_flags = ("required",)

    def __init__(self, message: Optional[str] = None):
        self.message = message or error_messages["MANDATORY_DATE"]

    def __call__(self, form: "QuestionnaireForm", field: DateField) -> None:
        """
        Raise exception if ALL fields have not been filled out.
        Not having that field is the same as not filling it out
        as the remaining fields would also have to be empty for
        exception to be raised.
        """
        day_not_entered = not form.day.data if hasattr(form, "day") else True
        month_not_entered = not form.month.data if hasattr(form, "month") else True
        year_not_entered = not form.year.data

        if day_not_entered and month_not_entered and year_not_entered:
            raise validators.StopValidation(self.message)


class DateCheck:
    def __init__(self, message: Optional[str] = None):
        self.message = message or error_messages["INVALID_DATE"]

    def __call__(self, form: "QuestionnaireForm", field: StringField) -> None:
        if not form.data:
            raise validators.StopValidation(self.message)

        if hasattr(form, "year") and len(form["year"].data) < 4:
            raise validators.StopValidation(error_messages["INVALID_YEAR_FORMAT"])

        try:
            if hasattr(form, "day"):
                datetime.strptime(form.data, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            elif hasattr(form, "month"):
                datetime.strptime(form.data, "%Y-%m").replace(tzinfo=timezone.utc)
            else:
                datetime.strptime(form.data, "%Y").replace(tzinfo=timezone.utc)
        except ValueError as exc:
            raise validators.StopValidation(self.message) from exc


class SingleDatePeriodCheck:
    def __init__(
        self,
        messages: OptionalMessage = None,
        date_format: str = "d MMMM yyyy",
        minimum_date: Optional[datetime] = None,
        maximum_date: Optional[datetime] = None,
    ):
        self.messages = {**error_messages, **(messages or {})}
        self.minimum_date = minimum_date
        self.maximum_date = maximum_date
        self.date_format = date_format

    def __call__(self, form: "QuestionnaireForm", field: StringField) -> None:
        date = parse_datetime(form.data)

        if self.minimum_date and date and date < self.minimum_date:
            raise validators.ValidationError(
                self.messages["SINGLE_DATE_PERIOD_TOO_EARLY"]
                % {
                    "min": self._format_playback_date(
                        self.minimum_date + relativedelta(days=-1), self.date_format
                    )
                }
            )

        if self.maximum_date and date and date > self.maximum_date:
            raise validators.ValidationError(
                self.messages["SINGLE_DATE_PERIOD_TOO_LATE"]
                % {
                    "max": self._format_playback_date(
                        self.maximum_date + relativedelta(days=+1), self.date_format
                    )
                }
            )

    @staticmethod
    def _format_playback_date(date: datetime, date_format: str = "d MMMM yyyy") -> str:
        formatted_date: str = flask_babel.format_date(date, format=date_format)
        return formatted_date


class DateRangeCheck:
    def __init__(
        self,
        messages: OptionalMessage = None,
        period_min: Optional[dict[str, int]] = None,
        period_max: Optional[dict[str, int]] = None,
    ):
        self.messages = {**error_messages, **(messages or {})}
        self.period_min = period_min
        self.period_max = period_max

    def __call__(
        self, form: "QuestionnaireForm", from_field: DateField, to_field: DateField
    ) -> None:
        from_date = parse_datetime(from_field.data)
        to_date = parse_datetime(to_field.data)

        if from_date and to_date:
            if from_date >= to_date:
                raise validators.ValidationError(self.messages["INVALID_DATE_RANGE"])

        answered_range_relative = relativedelta(to_date, from_date)

        if self.period_min:
            min_range = self._return_relative_delta(self.period_min)
            if self._is_first_relative_delta_largest(
                min_range, answered_range_relative
            ):
                raise validators.ValidationError(
                    self.messages["DATE_PERIOD_TOO_SMALL"]
                    % {"min": self._build_range_length_error(self.period_min)}
                )

        if self.period_max:
            max_range = self._return_relative_delta(self.period_max)
            if self._is_first_relative_delta_largest(
                answered_range_relative, max_range
            ):
                raise validators.ValidationError(
                    self.messages["DATE_PERIOD_TOO_LARGE"]
                    % {"max": self._build_range_length_error(self.period_max)}
                )

    @staticmethod
    def _return_relative_delta(period_object: PeriodType) -> relativedelta:
        return relativedelta(
            years=period_object.get("years", 0),
            months=period_object.get("months", 0),
            days=period_object.get("days", 0),
        )

    @staticmethod
    def _is_first_relative_delta_largest(
        relativedelta1: relativedelta, relativedelta2: relativedelta
    ) -> bool:
        epoch = datetime.min  # generic epoch for comparison purposes only
        date1 = epoch + relativedelta1
        date2 = epoch + relativedelta2
        return date1 > date2

    @staticmethod
    def _build_range_length_error(period_object: PeriodType) -> str:
        error_message = ""
        if "years" in period_object:
            error_message = ngettext(
                "%(num)s year", "%(num)s years", period_object["years"]
            )
        if "months" in period_object:
            message_addition = ngettext(
                "%(num)s month", "%(num)s months", period_object["months"]
            )
            error_message += (
                message_addition if error_message == "" else ", " + message_addition
            )
        if "days" in period_object:
            message_addition = ngettext(
                "%(num)s day", "%(num)s days", period_object["days"]
            )
            error_message += (
                message_addition if error_message == "" else ", " + message_addition
            )

        return error_message


class SumCheck:
    def __init__(
        self, messages: OptionalMessage = None, currency: Optional[str] = None
    ):
        self.messages = {**error_messages, **(messages or {})}
        self.currency = currency

    def __call__(
        self,
        form: QuestionnaireForm,
        conditions: List[str],
        total: Decimal | int,
        target_total: Decimal | float | int,
        decimal_limit: int | None = None,
    ) -> None:
        if len(conditions) > 1:
            try:
                conditions.remove("equals")
            except ValueError as exc:
                raise ValueError(
                    "There are multiple conditions, but equals is not one of them. "
                    "We only support <= and >="
                ) from exc

            condition = f"{conditions[0]} or equals"
        else:
            condition = conditions[0]

        is_valid, message = self._is_valid(condition, total, target_total)

        if not is_valid:
            decimal_limit = decimal_limit or (
                None
                if isinstance(target_total, int)
                else str(target_total)[::-1].find(".")
            )
            raise validators.ValidationError(
                self.messages[message]
                % {
                    "total": format_playback_value(
                        value=target_total,
                        currency=self.currency,
                        decimal_limit=decimal_limit,
                    )
                }
            )

    @staticmethod
    def _is_valid(
        condition: str,
        total: Union[Decimal, float],
        target_total: Union[Decimal, float],
    ) -> tuple[bool, str]:
        if condition == "equals":
            return total == target_total, "TOTAL_SUM_NOT_EQUALS"
        if condition == "less than":
            return total < target_total, "TOTAL_SUM_NOT_LESS_THAN"
        if condition == "greater than":
            return total > target_total, "TOTAL_SUM_NOT_GREATER_THAN"
        if condition == "greater than or equals":
            return total >= target_total, "TOTAL_SUM_NOT_GREATER_THAN_OR_EQUALS"
        if condition == "less than or equals":
            return total <= target_total, "TOTAL_SUM_NOT_LESS_THAN_OR_EQUALS"

        raise NotImplementedError(f"Condition '{condition}' is not implemented")


class MutuallyExclusiveCheck:
    def __init__(self, question_title: str, messages: OptionalMessage = None):
        self.messages = {**error_messages, **(messages or {})}
        self.question_title = question_title

    def __call__(
        self,
        answer_values: Iterable,
        is_mandatory: bool,
        is_only_checkboxes_or_radios: bool,
    ) -> None:
        total_answered = sum(
            value not in QuestionnaireStoreUpdater.EMPTY_ANSWER_VALUES
            for value in answer_values
        )

        if total_answered > 1:
            raise validators.ValidationError(self.messages["MUTUALLY_EXCLUSIVE"])
        if is_mandatory and total_answered < 1:
            message = format_message_with_title(
                (
                    self.messages["MANDATORY_CHECKBOX"]
                    if is_only_checkboxes_or_radios
                    else self.messages["MANDATORY_QUESTION"]
                ),
                self.question_title,
            )
            raise validators.ValidationError(message)


class MobileNumberCheck:
    def __init__(self, message: OptionalMessage = None):
        self.message = message or error_messages["INVALID_MOBILE_NUMBER"]

    def __call__(self, form: "QuestionnaireForm", field: StringField) -> None:
        data = sanitise_mobile_number(field.data)

        if len(data) != 10 or not re.match("^7[0-9]+$", data):
            raise validators.ValidationError(self.message)


class EmailTLDCheck:
    def __init__(self, message: Optional[str] = None):
        self.message = message or error_messages["INVALID_EMAIL_FORMAT"]

    def __call__(self, form: "QuestionnaireForm", field: StringField) -> None:
        if match := email_regex.match(field.data):
            hostname = match.group(1)
            try:
                hostname = hostname.encode("idna").decode("ascii")
            except UnicodeError as exc:
                raise validators.StopValidation(self.message) from exc
            parts = hostname.split(".")
            if len(parts) > 1 and not tld_part_regex.match(parts[-1]):
                raise validators.StopValidation(self.message)
