from datetime import datetime, timezone
from decimal import Decimal
from typing import Sequence, Union, Optional, Sized
from urllib.parse import quote

from babel.dates import format_datetime
from babel.numbers import format_currency, format_decimal
from dateutil.relativedelta import relativedelta
from flask_babel import ngettext

from app.settings import DEFAULT_LOCALE


class PlaceholderTransforms:
    """
    A class to group the transforms that can be used within placeholders
    """

    def __init__(self, language: str):
        self.language = language
        self.locale = DEFAULT_LOCALE if language in ["en", "eo"] else language

    input_date_format = "%Y-%m-%d"
    input_date_format_month_year_only = "%Y-%m"

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
            PlaceholderTransforms.parse_date(second_date),
            PlaceholderTransforms.parse_date(first_date),
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

    @staticmethod
    def parse_date(date: str) -> datetime:
        """
        :param date: string representing a date
        :return: datetime of that date

        Convert `date` from string into `datetime` object. `date` can be 'YYYY-MM-DD', 'YYYY-MM'
        or 'now'. Note that in the shorthand YYYY-MM format, day_of_month is assumed to be 1.
        """
        if date == "now":
            return datetime.now(tz=timezone.utc)

        try:
            return datetime.strptime(
                date, PlaceholderTransforms.input_date_format
            ).replace(tzinfo=timezone.utc)
        except ValueError:
            return datetime.strptime(
                date, PlaceholderTransforms.input_date_format_month_year_only
            ).replace(tzinfo=timezone.utc)

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

    @staticmethod
    def list_item_count(list_to_count: Optional[Sized]) -> int:
        if list_to_count is not None:
            return len(list_to_count or [])
