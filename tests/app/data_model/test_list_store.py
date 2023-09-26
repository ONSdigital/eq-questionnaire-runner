import pytest

from app.data_models.list_store import ListModel, ListStore


def test_list_serialisation():
    store = ListStore()

    first_id = store.add_list_item("people")
    second_id = store.add_list_item("people", primary_person=True)
    additional_list_id = store.add_list_item("pets")

    serialized = store.serialize()

    assert serialized == [
        {"name": "people", "primary_person": second_id, "items": [second_id, first_id]},
        {"name": "pets", "items": [additional_list_id]},
    ]


def test_deserialisation():
    store = ListStore()
    # pylint: disable=protected-access
    first_id = store._generate_identifier()
    second_id = store._generate_identifier()
    additional_id = store._generate_identifier()

    serialized = [
        {"name": "people", "primary_person": second_id, "items": [first_id, second_id]},
        {"name": "pets", "items": [additional_id]},
    ]

    deserialized = ListStore.deserialize(serialized)

    assert deserialized["people"].items == [first_id, second_id]
    assert deserialized["people"].primary_person == second_id
    assert deserialized["pets"].items == [additional_id]


def test_unique_id_generation(mocker):
    """
    Ensure that every id generated is unique per questionnaire.
    """
    # Mock the app.data_models.list_store.random_string method to return duplicates.
    with mocker.patch(
        "app.data_models.list_store.random_string",
        side_effect=["first", "first", "second"],
    ):
        store = ListStore()
        # pylint: disable=protected-access
        store._lists["test"] = ListModel(name="test", items=["first"])
        result = store._generate_identifier()

    assert result == "second"


def test_get_item():
    store = ListStore()
    assert store["not_a_list"] == ListModel("not_a_list")


def test_list_item_position():
    store = ListStore()

    first_id = store.add_list_item("people")
    second_id = store.add_list_item("people")

    assert store.list_item_position("people", first_id) == 1
    assert store.list_item_position("people", second_id) == 2

    with pytest.raises(ValueError):
        assert store.list_item_position("people", "not-an-id")


def test_list_item_positions_update_after_deletion():
    store = ListStore()

    first_id = store.add_list_item("people")
    second_id = store.add_list_item("people")

    assert store.list_item_position("people", first_id) == 1

    store.delete_list_item("people", first_id)
    assert store.list_item_position("people", second_id) == 1


def test_delete_list_item_id():
    store = ListStore()
    person = store.add_list_item("people")
    store.delete_list_item("people", person)
    assert not store._lists  # pylint: disable=protected-access


def test_delete_list():
    store = ListStore()
    store.add_list_item("people")
    store.add_list_item("people")
    store.delete_list("people")
    assert not store._lists  # pylint: disable=protected-access


def test_delete_list_item_id_does_not_raise():
    store = ListStore()
    store.add_list_item("people")
    try:
        store.delete_list_item("people", "123456")
    except ValueError:
        # Not necessary, but keeps it explicit.
        pytest.fail("Deleting a non-existent list item raised an error")


def test_list_representation_equality():
    assert ListModel("list", ["1", "2"]) == ListModel("list", ["1", "2"])
    assert ListModel("list", ["1", "2"]) != ListModel("list", ["1"])

    assert ListModel("list", ["1"], primary_person="1") == ListModel(
        "list", ["1"], primary_person="1"
    )
    assert ListModel("list", ["1"], primary_person="1") != ListModel(
        "list", ["1"], primary_person="2"
    )

    assert ListModel("list", ["1"]) != ["1"]


def test_list_model_get_item():
    assert ListModel("list", ["1", "2"])[0] == "1"
    assert ListModel("list", ["1", "2"])[-1] == "2"


def test_repr():
    test_list = ListModel("people", ["primaryperson"], primary_person="primaryperson")
    serialized = [
        {
            "name": "people",
            "primary_person": "primaryperson",
            "items": ["123", "primaryperson"],
        }
    ]

    list_store = ListStore.deserialize(serialized)

    assert "primary_person=primaryperson" in repr(test_list)
    assert "items=['primaryperson']" in repr(test_list)
    assert "primaryperson" in repr(list_store)


def test_first():
    test_list = ListModel("people", ["abcde", "12345"])
    assert test_list.first == "abcde"


def test_first_raises_index_error_when_list_is_empty():
    new_list = ListModel("people", [])

    with pytest.raises(IndexError) as error:
        new_list.first  # pylint: disable=pointless-statement

    assert "unable to access first item in list, list 'people' is empty" in str(
        error.value
    )


def test_get_item_using_method():
    store = ListStore()

    first_id = store.add_list_item("people")

    item = store.get("people")

    assert item.items[0] == first_id


def test_lookup_valid_list_item():
    store = ListStore()

    person_id = store.add_list_item("people")
    item_id = store.add_list_item("items")

    assert store.get_list_name_for_list_item_id(person_id) == "people"
    assert store.get_list_name_for_list_item_id(item_id) == "items"


def test_lookup_invalid_list_item():
    store = ListStore()

    with pytest.raises(ValueError) as error:
        store.get_list_name_for_list_item_id("not-a-list-item-id")

    assert f"list_item_id not-a-list-item-id not found in any lists" in str(error.value)
