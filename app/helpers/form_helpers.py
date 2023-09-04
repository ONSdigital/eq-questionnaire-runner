import re
from decimal import Decimal

import flask_babel
from babel import numbers

from app.jinja_filters import format_number
from app.utilities import safe_content
from app.utilities.decimal_places import get_formatted_currency


def sanitise_number(number: str) -> str:
    return (
        number.replace(numbers.get_group_symbol(flask_babel.get_locale()), "")
        .replace("_", "")
        .replace(" ", "")
    )


def sanitise_mobile_number(data: str) -> str:
    data = re.sub(r"[\s.,\t\-{}\[\]()/]", "", data)
    return re.sub(r"^(0{1,2}44|\+44|0)", "", data)


def format_playback_value(
    value: float | Decimal,
    currency: str | None = None,
    decimal_limit: int | None = None,
) -> str:
    # For playback of values we set the decimal limit based on the number of decimal places
    # in the given value rather than any limit that has been set in the schema as we do for other methods
    if currency:
        return get_formatted_currency(
            value=value, currency=currency, decimal_limit=decimal_limit
        )

    formatted_number: str = format_number(value)
    return formatted_number


def format_message_with_title(error_message: str, question_title: str) -> str:
    return error_message % {"question_title": safe_content(question_title)}
