from typing import IO, Any

import simplejson as json


def json_load(file: IO[str], **kwargs: Any) -> dict:
    return json.load(file, use_decimal=True, **kwargs)  # type: ignore


def json_loads(data: str, **kwargs: Any) -> dict:
    return json.loads(data, use_decimal=True, **kwargs)  # type: ignore


def json_dumps(data: Any, **kwargs: Any) -> str:
    return json.dumps(data, for_json=True, use_decimal=True, **kwargs)
