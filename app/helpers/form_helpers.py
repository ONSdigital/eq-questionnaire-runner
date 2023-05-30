import flask_babel
from babel import numbers


def sanitise_number(number: str) -> str:
    return (
        number.replace(numbers.get_group_symbol(flask_babel.get_locale()), "")
        .replace("_", "")
        .replace(" ", "")
    )
