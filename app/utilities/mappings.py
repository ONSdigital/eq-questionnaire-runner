from collections import defaultdict
from typing import Iterable, Mapping


def get_flattened_mapping_value(
    map_to_flatten: defaultdict[str, Iterable[str]] | Mapping[str, Iterable[str]]
) -> set[str]:
    return {x for v in map_to_flatten.values() for x in v}
