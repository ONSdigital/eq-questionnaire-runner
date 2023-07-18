from typing import Generator, Iterable, Mapping, Sequence

from ordered_set import OrderedSet

from app.utilities.types import SectionKey


def get_flattened_mapping_values(
    map_to_flatten: Mapping[SectionKey, Iterable[str]] | Mapping[str, Iterable[str]]
) -> OrderedSet[str]:
    return OrderedSet([x for v in map_to_flatten.values() for x in v])


def get_mappings_with_key(  # noqa: C901 pylint: disable=too-complex
    key: str, data: Mapping | Sequence, ignore_keys: list[str] | None = None
) -> Generator[Mapping, None, None]:
    ignore_keys = ignore_keys or []

    def _handle_sequence(value: Sequence) -> Generator[Mapping, None, None]:
        for element in value:
            if isinstance(element, Mapping):
                yield from get_mappings_with_key(key, element, ignore_keys)

    if isinstance(data, Sequence):
        yield from _handle_sequence(data)

    if isinstance(data, Mapping):
        if key not in ignore_keys and key in data:
            yield data

        for k, v in data.items():
            if k in ignore_keys:
                continue
            if isinstance(v, Mapping):
                yield from get_mappings_with_key(key, v, ignore_keys)
            if isinstance(v, Sequence):
                yield from _handle_sequence(v)
