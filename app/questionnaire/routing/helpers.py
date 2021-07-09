from datetime import datetime
from functools import wraps
from typing import Any, Callable

from app.questionnaire.value_source_resolver import answer_value_types


def _casefold(value: answer_value_types) -> answer_value_types:
    try:
        return (
            [_casefold(v) for v in value]
            if isinstance(value, (list, tuple))
            else value.casefold()  # type: ignore
        )
    except AttributeError:
        return value


def casefold(func: Callable) -> Any:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        casefolded_args = [_casefold(arg) for arg in args]
        casefolded_kwargs = {k: _casefold(v) for k, v in kwargs.items()}
        return func(*casefolded_args, **casefolded_kwargs)

    return wrapper


def datetime_as_midnight(date: datetime) -> datetime:
    return date.replace(hour=0, minute=0, second=0, microsecond=0)
