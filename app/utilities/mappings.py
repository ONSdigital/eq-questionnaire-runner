from typing import Mapping


def get_flattened_mapping_value(map_to_flatten: Mapping[str, list[str]]) -> set[str]:
    return {x for v in map_to_flatten.values() for x in v}
