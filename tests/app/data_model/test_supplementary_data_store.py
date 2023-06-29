import pytest
from werkzeug.datastructures import ImmutableDict

from app.data_models.supplementary_data_store import (
    InvalidSupplementaryDataSelector,
    SupplementaryDataStore,
)
from app.utilities.make_immutable import make_immutable


def test_supplementary_data_serialisation(
    supplementary_data_store_with_data,
    supplementary_data,
    supplementary_data_list_mappings,
):
    serialized = supplementary_data_store_with_data.serialize()

    assert serialized == {
        "data": supplementary_data,
        "list_mappings": supplementary_data_list_mappings,
    }


def test_supplementary_data_deserialisation():
    raw_data = {
        "identifier": "12346789012A",
        "items": {
            "products": [
                {"identifier": "89929001"},
                {"identifier": "201630601"},
            ]
        },
    }
    list_mappings = {"products": {"89929001": "item-1", "201630601": "item-2"}}

    serialized = {
        "data": raw_data,
        "list_mappings": list_mappings,
    }

    deserialized = SupplementaryDataStore.deserialize(serialized)

    assert deserialized.raw_data == make_immutable(raw_data)
    assert deserialized.list_mappings == make_immutable(list_mappings)
    assert deserialized._data_map == {  # pylint: disable=protected-access
        ("identifier", None): "12346789012A",
        ("products", "item-1"): {"identifier": "89929001"},
        ("products", "item-2"): {"identifier": "201630601"},
    }


def test_empty_supplementary_data_deserialisation():
    empty_store = SupplementaryDataStore.deserialize({})
    assert not empty_store.raw_data
    assert not empty_store.list_mappings
    assert not empty_store._data_map  # pylint: disable=protected-access


@pytest.mark.parametrize(
    "identifier,list_item_id,selectors,expected",
    [
        ("identifier", None, None, "12346789012A"),
        ("note", None, ["title"], "Volume of total production"),
        ("products", "item-2", ["name"], "Other Minerals"),
        ("products", "item-1", ["value_sales", "answer_code"], "89929001"),
        ("INVALID", None, None, None),
    ],
)
def test_get_supplementary_data(
    supplementary_data_store_with_data, identifier, list_item_id, selectors, expected
):
    assert (
        supplementary_data_store_with_data.get_data(
            identifier=identifier,
            list_item_id=list_item_id,
            selectors=selectors,
        )
        == expected
    )


def test_get_supplementary_data_invalid_selectors(supplementary_data_store_with_data):
    with pytest.raises(InvalidSupplementaryDataSelector) as exception:
        supplementary_data_store_with_data.get_data(
            identifier="identifier", selectors=["INVALID"], list_item_id=None
        )
        assert "Cannot use the selector `INVALID` on non-nested data" == str(exception)
