from datetime import datetime, timezone
from typing import Optional, overload

from dateutil import parser


def parse_iso_8601_datetime(iso_8601_date_string: str) -> datetime:
    return parser.isoparse(iso_8601_date_string).replace(tzinfo=timezone.utc)


@overload
def parse_datetime(date_string: None) -> None: ...  # pragma: no cover


@overload
def parse_datetime(date_string: str) -> datetime: ...  # pragma: no cover


def parse_datetime(date_string: Optional[str]) -> Optional[datetime]:
    """
    :param date_string: string representing a date
    :return: datetime of that date string

    Convert `date` from string into `datetime` object. `date` can be 'YYYY-MM-DD', 'YYYY-MM','now' or ISO 8601 format.
    Note that in the shorthand YYYY-MM format, day_of_month is assumed to be 1.
    """
    if not date_string:
        return None

    if date_string == "now":
        return datetime.now(tz=timezone.utc)

    try:
        return parse_iso_8601_datetime(date_string)
    except ValueError as ex:
        raise ValueError(f"'{date_string}' is not in a valid date format") from ex
