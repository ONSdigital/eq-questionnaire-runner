from app.questionnaire.routing_path import RoutingPath
from app.utilities.types import SectionKey


def test_eq_to_routing_path(block_ids, routing_path):
    assert routing_path == RoutingPath(
        block_ids=block_ids,
        section_id="section-1",
        list_item_id="list_item_id",
        list_name="list_name",
    )


def test_eq_to_tuple(block_ids, routing_path):
    assert tuple(block_ids) == routing_path


def test_len(block_ids, routing_path):
    assert len(routing_path) == len(block_ids)


def test_reversed(block_ids, routing_path):
    assert list(reversed(block_ids)) == list(reversed(routing_path))


def test_contains_true(block_ids, routing_path):
    assert block_ids[0] in routing_path
    assert "block-z" not in routing_path


def test_iter(block_ids, routing_path):
    assert block_ids[0] == next(iter(routing_path))


def test_getitem(block_ids, routing_path):
    assert block_ids[0] == routing_path[0]


def test_properties(block_ids, routing_path):
    assert block_ids == routing_path
    assert "section-1" == routing_path.section_id
    assert "list_item_id" == routing_path.list_item_id
    assert "list_name" == routing_path.list_name
    assert SectionKey("section-1", "list_item_id") == routing_path.section_key
