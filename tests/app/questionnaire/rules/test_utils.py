from datetime import datetime, timezone

import pytest
from dateutil import parser
from freezegun import freeze_time

from app.questionnaire.rules.utils import parse_datetime


@pytest.mark.parametrize(
    "date_string, date_format",
    [
        ("2021-10", "%Y-%m"),
        ("2021-10-29", "%Y-%m-%d"),
        ("2021-10-29T10:53:41.511833+00:00", "iso8601"),
        ("2021-10-29T10:53:41+00:00", "iso8601"),
        ("2021-10-29T10:53:41.511833Z", "iso8601"),
        ("2021-11-22T15:34:54Z", "iso8601"),
    ],
)
def test_parse_datetime(date_string, date_format):
    expected_date = (
        parser.isoparse(date_string)
        if date_format == "iso8601"
        else datetime.strptime(date_string, date_format)
    )

    assert parse_datetime(date_string) == expected_date.replace(tzinfo=timezone.utc)


@freeze_time(datetime.now(timezone.utc))
def test_parse_datetime_now():
    assert parse_datetime("now") == datetime.now(timezone.utc)


@pytest.mark.parametrize(
    "date_string",
    [
        "2021--10",
        "2021-10-229",
        "2021-10-29T10:53:41.511833+00:0000",
        "2021-11-22T15:34:544Z",
    ],
)
def test_parse_date_exception(date_string):
    with pytest.raises(ValueError):
        parse_datetime(date_string)
