import pytest

from app.data_models.progress import Progress
from app.data_models.progress_store import CompletionStatus, ProgressStore
from app.questionnaire.location import Location


def test_serialisation():
    store = ProgressStore()

    store.add_completed_location(Location(section_id="s1", block_id="one"))
    store.add_completed_location(Location(section_id="s1", block_id="two"))
    store.update_section_status(
        section_status=CompletionStatus.COMPLETED, section_id="s1"
    )

    store.add_completed_location(
        Location(
            section_id="s2",
            block_id="another-one",
            list_name="people",
            list_item_id="abc123",
        )
    )
    store.update_section_status(
        section_status=CompletionStatus.IN_PROGRESS,
        section_id="s2",
        list_item_id="abc123",
    )

    serialized = store.serialize()

    assert serialized == [
        Progress.from_dict(
            {
                "section_id": "s1",
                "list_item_id": None,
                "status": CompletionStatus.COMPLETED,
                "block_ids": ["one", "two"],
            }
        ),
        Progress.from_dict(
            {
                "section_id": "s2",
                "list_item_id": "abc123",
                "status": CompletionStatus.IN_PROGRESS,
                "block_ids": ["another-one"],
            }
        ),
    ]


def test_deserialisation():
    in_progress_sections = [
        {
            "section_id": "s1",
            "list_item_id": None,
            "status": CompletionStatus.IN_PROGRESS,
            "block_ids": ["one", "two"],
        },
        {
            "section_id": "s2",
            "list_item_id": "abc123",
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["three", "four"],
        },
    ]
    store = ProgressStore(in_progress_sections)

    assert store.get_section_status(section_id="s1") == CompletionStatus.IN_PROGRESS
    assert store.get_completed_block_ids("s1") == ["one", "two"]

    assert (
        store.get_section_status(section_id="s2", list_item_id="abc123")
        == CompletionStatus.COMPLETED
    )
    assert store.get_completed_block_ids(section_id="s2", list_item_id="abc123") == [
        "three",
        "four",
    ]


def test_clear():
    in_progress_sections = [
        {
            "section_id": "s1",
            "list_item_id": None,
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["one", "two"],
        },
        {
            "section_id": "s2",
            "list_item_id": "abc123",
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["three", "four"],
        },
    ]
    store = ProgressStore(in_progress_sections)

    store.clear()

    assert not store.serialize()
    assert store.is_dirty


def test_add_completed_location():
    store = ProgressStore()

    non_repeating_location = Location(section_id="s1", block_id="one")
    repeating_location = Location(
        section_id="s2",
        block_id="another-one",
        list_name="people",
        list_item_id="abc123",
    )

    store.add_completed_location(non_repeating_location)
    store.add_completed_location(repeating_location)

    assert store.get_completed_block_ids(section_id="s1") == [
        non_repeating_location.block_id
    ]
    assert store.get_completed_block_ids(section_id="s2", list_item_id="abc123") == [
        repeating_location.block_id
    ]

    assert store.is_dirty


def test_add_completed_location_existing():
    completed = [
        {
            "section_id": "s1",
            "list_item_id": None,
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["one"],
        },
        {
            "section_id": "s2",
            "list_item_id": "abc123",
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["three", "four"],
        },
    ]
    store = ProgressStore(completed)

    non_repeating_location = Location(section_id="s1", block_id="one")
    repeating_location = Location(
        section_id="s2", block_id="three", list_name="people", list_item_id="abc123"
    )

    store.add_completed_location(non_repeating_location)
    store.add_completed_location(repeating_location)

    assert store.get_section_status(section_id="s1") == CompletionStatus.COMPLETED
    assert (
        store.get_section_status(section_id="s2", list_item_id="abc123")
        == CompletionStatus.COMPLETED
    )

    assert len(store.get_completed_block_ids(section_id="s1")) == 1
    assert (
        len(store.get_completed_block_ids(section_id="s2", list_item_id="abc123")) == 2
    )

    assert not store.is_dirty


def test_add_completed_location_new():
    completed = [
        {
            "section_id": "s1",
            "list_item_id": None,
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["one"],
        },
        {
            "section_id": "s2",
            "list_item_id": "abc123",
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["three", "four"],
        },
    ]
    store = ProgressStore(completed)

    non_repeating_location = Location(section_id="s1", block_id="two")
    repeating_location = Location(
        section_id="s2", block_id="five", list_name="people", list_item_id="abc123"
    )

    store.add_completed_location(non_repeating_location)
    store.add_completed_location(repeating_location)

    assert store.get_section_status(section_id="s1") == CompletionStatus.COMPLETED
    assert (
        store.get_section_status(section_id="s2", list_item_id="abc123")
        == CompletionStatus.COMPLETED
    )

    assert len(store.get_completed_block_ids(section_id="s1")) == 2
    assert (
        len(store.get_completed_block_ids(section_id="s2", list_item_id="abc123")) == 3
    )

    assert store.is_dirty


def test_remove_completed_location():
    completed = [
        {
            "section_id": "s1",
            "list_item_id": None,
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["one", "two"],
        },
        {
            "section_id": "s2",
            "list_item_id": "abc123",
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["three", "four"],
        },
    ]
    store = ProgressStore(completed)

    non_repeating_location = Location(section_id="s1", block_id="one")
    repeating_location = Location(
        section_id="s2", block_id="three", list_name="people", list_item_id="abc123"
    )

    store.remove_completed_location(non_repeating_location)
    store.remove_completed_location(repeating_location)

    assert store.get_completed_block_ids(section_id="s1") == ["two"]
    assert store.get_completed_block_ids(section_id="s2", list_item_id="abc123") == [
        "four"
    ]

    assert store.is_dirty


def test_remove_final_completed_location_removes_section():
    completed = [
        {
            "section_id": "s1",
            "list_item_id": None,
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["one"],
        },
        {
            "section_id": "s2",
            "list_item_id": "abc123",
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["three"],
        },
    ]
    store = ProgressStore(completed)

    non_repeating_location = Location(section_id="s1", block_id="one")
    repeating_location = Location(
        section_id="s2", block_id="three", list_name="people", list_item_id="abc123"
    )

    store.remove_completed_location(non_repeating_location)
    store.remove_completed_location(repeating_location)

    assert ("s1", None) not in store
    assert store.get_completed_block_ids(section_id="s1") == []

    assert ("s2", "abc123") not in store
    assert store.get_completed_block_ids(section_id="s1", list_item_id="abc123") == []

    assert store.is_dirty


def test_remove_non_existent_completed_location():
    completed = [
        {
            "section_id": "s1",
            "list_item_id": None,
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["one"],
        }
    ]
    store = ProgressStore(completed)

    non_repeating_location = Location(section_id="s1", block_id="two")
    repeating_location = Location(
        section_id="s2", block_id="three", list_name="people", list_item_id="abc123"
    )

    store.remove_completed_location(non_repeating_location)
    store.remove_completed_location(repeating_location)

    assert len(store.get_completed_block_ids(section_id="s1")) == 1
    assert not store.is_dirty


def test_update_section_status():
    completed = [
        {
            "section_id": "s1",
            "list_item_id": None,
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["one"],
        },
        {
            "section_id": "s2",
            "list_item_id": "abc123",
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["three"],
        },
    ]
    store = ProgressStore(completed)

    store.update_section_status(
        section_status=CompletionStatus.IN_PROGRESS, section_id="s1"
    )
    store.update_section_status(
        section_status=CompletionStatus.IN_PROGRESS,
        section_id="s2",
        list_item_id="abc123",
    )

    assert store.get_section_status(section_id="s1") == CompletionStatus.IN_PROGRESS
    assert (
        store.get_section_status(section_id="s2", list_item_id="abc123")
        == CompletionStatus.IN_PROGRESS
    )
    assert store.is_dirty


def test_update_non_existing_section_status():
    completed = [
        {
            "section_id": "s1",
            "list_item_id": None,
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["one"],
        }
    ]
    store = ProgressStore(completed)

    store.update_section_status("s2", CompletionStatus.IN_PROGRESS)

    assert store.get_section_status("s1") == CompletionStatus.COMPLETED

    assert "s2" not in store
    assert store.get_completed_block_ids(section_id="s2") == []

    assert not store.is_dirty


def test_get_section_status():
    existing_progress = [
        {
            "section_id": "s1",
            "list_item_id": None,
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["one"],
        },
        {
            "section_id": "s2",
            "list_item_id": "abc123",
            "status": CompletionStatus.IN_PROGRESS,
            "block_ids": ["three"],
        },
    ]
    store = ProgressStore(existing_progress)

    assert store.get_section_status(section_id="s1") == CompletionStatus.COMPLETED
    assert (
        store.get_section_status(section_id="s2", list_item_id="abc123")
        == CompletionStatus.IN_PROGRESS
    )


def test_get_section_locations():
    completed = [
        {
            "section_id": "s1",
            "list_item_id": None,
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["one"],
        },
        {
            "section_id": "s2",
            "list_item_id": "abc123",
            "status": CompletionStatus.IN_PROGRESS,
            "block_ids": ["three"],
        },
    ]
    store = ProgressStore(completed)

    assert store.get_completed_block_ids(section_id="s1") == ["one"]

    assert store.get_completed_block_ids(section_id="s2", list_item_id="abc123") == [
        "three"
    ]


def test_is_section_complete():
    completed = [
        {
            "section_id": "s1",
            "list_item_id": None,
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["one", "two"],
        },
        {
            "section_id": "s2",
            "list_item_id": None,
            "status": CompletionStatus.IN_PROGRESS,
            "block_ids": ["three"],
        },
        {
            "section_id": "s3",
            "list_item_id": "abc123",
            "status": CompletionStatus.IN_PROGRESS,
            "block_ids": ["three"],
        },
        {
            "section_id": "s4",
            "list_item_id": "123abc",
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["not-three"],
        },
        {
            "section_id": "s5",
            "list_item_id": "456def",
            "status": CompletionStatus.INDIVIDUAL_RESPONSE_REQUESTED,
            "block_ids": ["not-three"],
        },
    ]

    store = ProgressStore(completed)

    assert store.is_section_complete(section_id="s1", list_item_id=None) is True
    assert store.is_section_complete(section_id="s4", list_item_id="123abc") is True
    assert store.is_section_complete(section_id="s5", list_item_id="456def") is True


def test_remove_progress_for_list_item_id():
    completed = [
        {
            "section_id": "s1",
            "list_item_id": None,
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["one", "two"],
        },
        {
            "section_id": "s2",
            "list_item_id": None,
            "status": CompletionStatus.IN_PROGRESS,
            "block_ids": ["three"],
        },
        {
            "section_id": "s3",
            "list_item_id": "abc123",
            "status": CompletionStatus.IN_PROGRESS,
            "block_ids": ["three"],
        },
        {
            "section_id": "s4",
            "list_item_id": "123abc",
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["not-three"],
        },
    ]

    store = ProgressStore(completed)

    store.remove_progress_for_list_item_id(list_item_id="abc123")

    assert ("s3", "abc123") not in store
    assert store.get_completed_block_ids(section_id="s3", list_item_id="abc123") == []

    assert ("s4", "123abc") in store

    store.remove_progress_for_list_item_id(list_item_id="123abc")

    assert ("s4", "123abc") not in store
    assert store.get_completed_block_ids(section_id="s4", list_item_id="123abc") == []


@pytest.mark.parametrize(
    "section_ids, expected_section_keys",
    [
        # No repeating sections
        ({"s1", "s2"}, [("s1", None), ("s2", None)]),
        # Repeating sections and non repeating sections
        ({"s1", "s4"}, [("s1", None), ("s4", "123abc")]),
        # Only repeating sections
        ({"s4", "s5"}, [("s4", "123abc"), ("s5", "456def")]),
        # No filter_by paramater specified
        (None, [("s1", None), ("s2", None), ("s4", "123abc"), ("s5", "456def")]),
    ],
)
def test_in_progress_and_completed_section_ids(section_ids, expected_section_keys):
    completed = [
        {
            "section_id": "s1",
            "list_item_id": None,
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["one", "two"],
        },
        {
            "section_id": "s2",
            "list_item_id": None,
            "status": CompletionStatus.IN_PROGRESS,
            "block_ids": ["three"],
        },
        {
            "section_id": "s3",
            "list_item_id": "abc123",
            "status": CompletionStatus.NOT_STARTED,
            "block_ids": ["three"],
        },
        {
            "section_id": "s4",
            "list_item_id": "123abc",
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["not-three"],
        },
        {
            "section_id": "s5",
            "list_item_id": "456def",
            "status": CompletionStatus.IN_PROGRESS,
            "block_ids": ["not-three"],
        },
    ]

    store = ProgressStore(completed)

    statuses = {CompletionStatus.COMPLETED, CompletionStatus.IN_PROGRESS}
    section_keys = store.section_keys(section_ids=section_ids, statuses=statuses)

    assert sorted(section_keys) == expected_section_keys


def test_section_keys():
    completed = [
        {
            "section_id": "s1",
            "list_item_id": None,
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["one", "two"],
        },
        {
            "section_id": "s2",
            "list_item_id": None,
            "status": CompletionStatus.IN_PROGRESS,
            "block_ids": ["three"],
        },
        {
            "section_id": "s3",
            "list_item_id": "abc123",
            "status": CompletionStatus.NOT_STARTED,
            "block_ids": ["three"],
        },
        {
            "section_id": "s4",
            "list_item_id": "123abc",
            "status": CompletionStatus.COMPLETED,
            "block_ids": ["not-three"],
        },
        {
            "section_id": "s5",
            "list_item_id": "456def",
            "status": CompletionStatus.IN_PROGRESS,
            "block_ids": ["not-three"],
        },
    ]

    store = ProgressStore(completed)
    section_keys = store.section_keys(section_ids={"s1", "s2", "s3"})
    assert sorted(section_keys) == sorted(
        [("s1", None), ("s2", None), ("s3", "abc123")]
    )
