from datetime import datetime
from functools import wraps
from typing import Any, Callable, Union

ValueTypes = Union[bool, str, int, float, None, datetime]


def _casefold(value: Union[list, ValueTypes]) -> Union[list, ValueTypes]:
    if isinstance(value, str):
        return value.casefold()

    if isinstance(value, list):
        return [_casefold(v) for v in value]

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
