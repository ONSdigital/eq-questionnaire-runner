import pytest

from app.data_models.answer_store import AnswerStore
from app.data_models.relationship_store import RelationshipStore
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.relationship_router import RelationshipRouter


def relationship_router(answers=None, relationships=None):
    return RelationshipRouter(
        answer_store=AnswerStore(answers),
        relationship_store=RelationshipStore(relationships),
        section_id="relationships-section",
        list_name="people",
        list_item_ids=["abc123", "def123", "ghi123", "jkl123"],
        relationships_block_id="relationships",
    )


def relationship_location(list_item_id, to_list_item_id):
    return RelationshipLocation(
        section_id="relationships-section",
        list_name="people",
        list_item_id=list_item_id,
        to_list_item_id=to_list_item_id,
        block_id="relationships",
    )


def test_can_access_location():
    location = relationship_location("abc123", "def123")
    can_access_location = relationship_router().can_access_location(location)
    assert can_access_location


def test_cant_access_location():
    location = relationship_location("def123", "abc123")
    can_access_location = relationship_router().can_access_location(location)
    assert not can_access_location


def test_get_first_location():
    first_location = relationship_router().get_first_location()
    expected_location = relationship_location("abc123", "def123")
    assert first_location == expected_location


def test_get_last_location():
    last_location = relationship_router().get_last_location()
    expected_location = relationship_location("ghi123", "jkl123")
    assert last_location == expected_location


def test_get_next_location():
    location = relationship_location("abc123", "def123")
    next_location = relationship_router().get_next_location(location)
    expected_location = relationship_location("abc123", "ghi123")
    assert next_location == expected_location


def test_get_next_location_goes_to_next_person():
    location = relationship_location("abc123", "jkl123")
    next_location = relationship_router().get_next_location(location)
    expected_location = relationship_location("def123", "ghi123")
    assert next_location == expected_location


def test_get_previous_location():
    location = relationship_location("abc123", "ghi123")
    previous_location = relationship_router().get_previous_location(location)
    expected_location = relationship_location("abc123", "def123")
    assert previous_location == expected_location


def test_get_previous_location_goes_to_previous_person():
    location = relationship_location("def123", "ghi123")
    previous_location = relationship_router().get_previous_location(location)
    expected_location = relationship_location("abc123", "jkl123")
    assert previous_location == expected_location
