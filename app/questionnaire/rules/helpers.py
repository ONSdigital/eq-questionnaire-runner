from datetime import datetime
from decimal import Decimal
from functools import wraps
from typing import Any, Callable, Sequence

ValueTypes = bool | str | int | float | Decimal | None | datetime


def _casefold(value: list | ValueTypes) -> list | ValueTypes:
    if isinstance(value, str):
        return value.casefold()

    if isinstance(value, Sequence):
        return [_casefold(v) for v in value]

    return value


def casefold(func: Callable) -> Any:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        casefolded_args = [_casefold(arg) for arg in args]
        casefolded_kwargs = {k: _casefold(v) for k, v in kwargs.items()}
        return func(*casefolded_args, **casefolded_kwargs)

    return wrapper
