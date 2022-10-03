from collections import abc
from typing import Any

from werkzeug.datastructures import ImmutableDict


def serialize(data: Any) -> Any:
    if isinstance(data, abc.Hashable):
        return data
    if isinstance(data, list):
        return tuple((serialize(item) for item in data))
    if isinstance(data, dict):
        key_value_tuples = {k: serialize(v) for k, v in data.items()}
        return ImmutableDict(key_value_tuples)
