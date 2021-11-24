from datetime import datetime, timezone
from typing import Optional, overload


@overload
def parse_datetime(date_string: None) -> None:
    ...  # pragma: no cover


@overload
def parse_datetime(date_string: str) -> datetime:
    ...  # pragma: no cover


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

    date_formats = ["%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%d", "%Y-%m", "%Y"]

    for date_format in date_formats:
        try:
            return datetime.strptime(date_string, date_format).replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            continue

    raise ValueError(
        f"No valid date format for date '{date_string}', possible formats: {date_formats}"
    )
