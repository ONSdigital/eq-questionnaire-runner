from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Optional, Sequence, Sized, Union
from urllib.parse import quote

from babel.dates import format_datetime
from babel.numbers import format_currency, format_decimal
from dateutil.relativedelta import relativedelta
from flask_babel import ngettext

from app.questionnaire.routing.operations import DateOffset, Operations
from app.questionnaire.routing.utils import parse_datetime
from app.settings import DEFAULT_LOCALE

# pylint: disable=too-many-public-methods


class PlaceholderTransforms:
    """
    A class to group the transforms that can be used within placeholders
    """

    def __init__(self, language: str):
        self.language = language
        self.locale = DEFAULT_LOCALE if language in ["en", "eo"] else language
        self._operations = Operations(language=self.language)

    input_date_format = "%Y-%m-%d"

    def format_currency(self, number: int = None, currency: str = "GBP") -> str:
        formatted_currency: str = format_currency(number, currency, locale=self.locale)
        return formatted_currency

    def format_date(self, date_to_format: str, date_format: str) -> str:
        date_as_datetime = datetime.strptime(
            date_to_format, self.input_date_format
        ).replace(tzinfo=timezone.utc)

        formatted_datetime: str = format_datetime(
            date_as_datetime, date_format, locale=self.locale
        )
        return formatted_datetime

    @staticmethod
    def format_list(list_to_format: Sequence[str]) -> str:
        formatted_list = "<ul>"
        for item in list_to_format:
            formatted_list += f"<li>{item}</li>"
        formatted_list += "</ul>"
        return formatted_list

    @staticmethod
    def remove_empty_from_list(list_to_filter: Sequence[str]) -> list[str]:

        """
        :param list_to_filter: anything that is iterable
        :return: a list with no empty values

        In this filter the following values are considered non empty:
        - None
        - any empty sequence, for example, '', (), [].
        - any empty mapping, for example, {}.

        This filter will treat zero of any numeric type for example, 0, 0.0, 0j and boolean 'False'
        as a valid item since they are naturally 'falsy' in Python but not empty.

        Note: Booleans are a subtype of integers. Zero of any numeric type 'is not False' but 'equals False'.
        Reference: https://docs.python.org/release/3.4.2/library/stdtypes.html?highlight=boolean#boolean-values
        """
        return [item for item in list_to_filter if item or item is False or item == 0]

    def concatenate_list(
        self, list_to_concatenate: Sequence[str], delimiter: str
    ) -> str:
        filtered_list = self.remove_empty_from_list(list_to_concatenate)
        return delimiter.join(filtered_list)

    def telephone_number_link(self, telephone_number: str) -> str:
        href = f"tel:{telephone_number.replace(' ', '')}"
        return self._create_hyperlink(href, telephone_number)

    def email_link(
        self,
        email_address: str,
        email_subject: str = None,
        email_subject_append: str = None,
    ) -> str:
        href = f"mailto:{email_address}"
        if email_subject:
            email_subject = (
                f"{email_subject} {email_subject_append}"
                if email_subject_append
                else email_subject
            )
            href = f"{href}?subject={quote(email_subject)}"

        return self._create_hyperlink(href, email_address)

    def format_possessive(self, string_to_format: str) -> str:
        if string_to_format and self.language == "en":
            lowered_string = string_to_format.lower()

            if lowered_string.endswith("'s") or lowered_string.endswith("’s"):
                return string_to_format[:-2] + "’s"

            if lowered_string[-1:] == "s":
                return string_to_format + "’"

            return string_to_format + "’s"

        return string_to_format

    def format_number(self, number: Union[int, Decimal, str]) -> str:
        if number or number == 0:
            formatted_decimal: str = format_decimal(number, locale=self.locale)
            return formatted_decimal

        return ""

    @staticmethod
    def calculate_date_difference(first_date: str, second_date: str) -> str:

        time = relativedelta(
            parse_datetime(second_date),
            parse_datetime(first_date),
        )

        if time.years:
            year_string: str = ngettext(
                "{number_of_years} year", "{number_of_years} years", time.years
            )
            return year_string.format(number_of_years=time.years)

        if time.months:
            month_string: str = ngettext(
                "{number_of_months} month", "{number_of_months} months", time.months
            )
            return month_string.format(number_of_months=time.months)

        day_string: str = ngettext(
            "{number_of_days} day", "{number_of_days} days", time.days
        )
        return day_string.format(number_of_days=time.days)

    def date_range_bounds(
        self,
        reference_date: str,
        offset_full_weeks: int,
        days_in_range: int,
        first_day_of_week: str = "MONDAY",
    ) -> tuple[str, str]:
        """Generate a start and end date for a date range given a reference date,
        weeks prior and number of days in range.

        :param reference_date: The date to reference the date range from, can be YYYY-MM-DD, YY-MM or 'now'.
        :type reference_date: datetime
        :param offset_full_weeks: Number of full weeks to offset from the reference date to start the date range.
        :type offset_full_weeks: int
        :param days_in_range: Number of days in the range, including the start date, must be a positive integer.
        :type days_in_range: int
        :param first_day_of_week: Which day of the week should be considered the first (default 'MONDAY').
            This is the day of the week which is selected as the start of the range.
        :type first_day_of_week: str
        :return: The start and end datetime objects of the range.
        :rtype: Tuple[datetime, datetime]
        """
        first_day_of_prior_full_week: date = self._operations.resolve_date_from_string(
            reference_date,
            DateOffset(days=offset_full_weeks * 7, day_of_week=first_day_of_week),
            offset_by_full_weeks=True,
        )  # type: ignore

        last_day_of_range = first_day_of_prior_full_week + relativedelta(
            days=days_in_range - 1
        )
        return (
            first_day_of_prior_full_week.strftime(self.input_date_format),
            last_day_of_range.strftime(self.input_date_format),
        )

    def format_date_range(self, date_range: tuple[str, str]) -> str:
        """Format a pair of dates as a string, clarifying differences in month or year.

        E.g.
            Monday 1 to Sunday 8 September 2021
            Monday 29 September to Sunday 6 October 2021
            Monday 29 December 2021 to Sunday 6 January 2022

        :param date_range: Pair of date strings representing a date range.
        :type date_range: tuple[str, str]
        :return: String containing the date range as text.
        :rtype: str
        """
        start_date_str, end_date_str = date_range
        start_date, end_date = list(map(parse_datetime, date_range))
        start_date_format = "EEEE d"
        end_date_format = "EEEE d MMMM y"

        if start_date.year != end_date.year:
            start_date_format += " MMMM y"
        elif start_date.month != end_date.month:
            start_date_format += " MMMM"

        start_date_formatted = self.format_date(start_date_str, start_date_format)
        end_date_formatted = self.format_date(end_date_str, end_date_format)

        return f"{start_date_formatted} to {end_date_formatted}"

    @staticmethod
    def add(lhs: Union[int, Decimal], rhs: Union[int, Decimal]) -> Union[int, Decimal]:
        return lhs + rhs

    def format_ordinal(self, number_to_format: int, determiner: str = None) -> str:

        indicator = self.get_ordinal_indicator(number_to_format)

        if determiner == "a_or_an" and self.language in ["en", "eo"]:
            a_or_an = (
                "an"
                if str(number_to_format).startswith("8") or number_to_format in [11, 18]
                else "a"
            )
            return f"{a_or_an} {number_to_format}{indicator}"

        return f"{number_to_format}{indicator}"

    def get_ordinal_indicator(self, number_to_format: int) -> str:
        if self.language in ["en", "eo"]:
            if 11 <= number_to_format % 100 <= 13:
                return "th"
            return {1: "st", 2: "nd", 3: "rd"}.get(number_to_format % 10, "th")

        if self.language == "ga":
            return "ú"

        if self.language == "cy":
            if number_to_format > 20:
                return "ain"
            return {
                1: "af",
                2: "il",
                3: "ydd",
                4: "ydd",
                5: "ed",
                6: "ed",
                11: "eg",
                13: "eg",
                14: "eg",
                16: "eg",
                17: "eg",
                19: "eg",
            }.get(number_to_format, "fed")

    def first_non_empty_item(self, items: Sequence[str]) -> str:
        """
        :param items: anything that is iterable
        :return: first non empty value

         Note: to guarantee the returned element is actually the first non empty element in the iterable,
        'items' must be a data structure that preserves order, ie tuple, list etc.
        If order is not important, this can be reused to return `one of` the elements which is non empty.
        """
        for item in self.remove_empty_from_list(items):
            return item

        return ""

    @staticmethod
    def contains(list_to_check: Sequence[str], value: str) -> bool:
        return value in list_to_check

    @staticmethod
    def list_has_items(list_to_check: Sequence[str]) -> bool:
        return len(list_to_check) > 0

    @staticmethod
    def format_name(
        first_name: str,
        middle_names: str,
        last_name: str,
        include_middle_names: bool = False,
    ) -> str:
        return (
            f"{first_name} {middle_names} {last_name}"
            if include_middle_names and middle_names
            else f"{first_name} {last_name}"
        )

    @staticmethod
    def _create_hyperlink(href: str, link_text: str) -> str:
        return f'<a href="{href}">{link_text}</a>'

    def list_item_count(self, list_to_count: Optional[Sized]) -> int:
        return self._operations.evaluate_count(list_to_count)
