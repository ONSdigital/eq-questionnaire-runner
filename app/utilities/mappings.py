from typing import Iterable, Mapping


def get_flattened_mapping_values(
    map_to_flatten: Mapping[tuple, Iterable[str]] | Mapping[str, Iterable[str]]
) -> set[str]:
    return {x for v in map_to_flatten.values() for x in v}
