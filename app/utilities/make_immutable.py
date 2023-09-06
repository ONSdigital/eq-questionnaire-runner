from collections import abc
from typing import Any

from werkzeug.datastructures import ImmutableDict


def make_immutable(data: Any) -> Any:
    if isinstance(data, abc.Hashable):
        return data
    if isinstance(data, set):
        return frozenset(data)  # set items must be hashable
    if isinstance(data, list):
        return tuple((make_immutable(item) for item in data))
    if isinstance(data, dict):
        key_value_tuples = {k: make_immutable(v) for k, v in data.items()}
        return ImmutableDict(key_value_tuples)
