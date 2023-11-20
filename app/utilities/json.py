from typing import IO, Any

import simplejson as json


def json_load(file: IO[str], **kwargs: Any) -> Any:
    return json.load(file, use_decimal=True, **kwargs)


def json_loads(data: str, **kwargs: Any) -> Any:
    return json.loads(data, use_decimal=True, **kwargs)


def json_dumps(data: Any, **kwargs: Any) -> str:
    return json.dumps(data, for_json=True, use_decimal=True, **kwargs)
