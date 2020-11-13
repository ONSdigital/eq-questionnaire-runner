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
        list_item_ids=["abc123", "def123", "ghi123", "jkl123", "mno123", "pqr123"],
        relationships_block_id="relationships",
        unrelated_block_id="related-to-anyone-else",
        unrelated_answer_id="anyone-else-answer",
        unrelated_no_answer_values=["No", "No, they are not related"],
    )


def relationship_location(list_item_id, to_list_item_id):
    return RelationshipLocation(
        section_id="relationships-section",
        list_name="people",
        list_item_id=list_item_id,
        to_list_item_id=to_list_item_id,
        block_id="relationships",
    )


def unrelated_relationship_location(list_item_id):
    return RelationshipLocation(
        section_id="relationships-section",
        list_name="people",
        list_item_id=list_item_id,
        block_id="related-to-anyone-else",
    )


def test_can_access_location():
    relationships = [
        {
            "list_item_id": "abc123",
            "to_list_item_id": "def123",
            "relationship": "Unrelated",
        },
        {
            "list_item_id": "abc123",
            "to_list_item_id": "ghi123",
            "relationship": "Unrelated",
        },
    ]
    router = relationship_router(relationships=relationships)
    location = unrelated_relationship_location("abc123")
    can_access_location = router.can_access_location(location)
    assert can_access_location


def test_cant_access_location():
    location = unrelated_relationship_location("abc123")
    can_access_location = relationship_router().can_access_location(location)
    assert not can_access_location


def test_get_last_location():
    last_location = relationship_router().get_last_location()
    expected_location = relationship_location("mno123", "pqr123")
    assert last_location == expected_location


def test_get_next_location_is_unrelated_question():
    relationships = [
        {
            "list_item_id": "abc123",
            "to_list_item_id": "def123",
            "relationship": "Unrelated",
        },
        {
            "list_item_id": "abc123",
            "to_list_item_id": "ghi123",
            "relationship": "Unrelated",
        },
    ]
    router = relationship_router(relationships=relationships)
    location = relationship_location("abc123", "ghi123")
    next_location = router.get_next_location(location)
    expected_location = unrelated_relationship_location("abc123")
    assert next_location == expected_location


def test_get_previous_location_is_unrelated_question():
    relationships = [
        {
            "list_item_id": "abc123",
            "to_list_item_id": "def123",
            "relationship": "Unrelated",
        },
        {
            "list_item_id": "abc123",
            "to_list_item_id": "ghi123",
            "relationship": "Unrelated",
        },
    ]
    router = relationship_router(relationships=relationships)
    location = relationship_location("abc123", "jkl123")
    previous_location = router.get_previous_location(location)
    expected_location = unrelated_relationship_location("abc123")
    assert previous_location == expected_location


def test_get_next_location_is_not_unrelated_question_when_less_than_two_relationships_left():
    relationships = [
        {
            "list_item_id": "abc123",
            "to_list_item_id": "def123",
            "relationship": "Related",
        },
        {
            "list_item_id": "abc123",
            "to_list_item_id": "ghi123",
            "relationship": "Related",
        },
        {
            "list_item_id": "abc123",
            "to_list_item_id": "jkl123",
            "relationship": "Unrelated",
        },
        {
            "list_item_id": "abc123",
            "to_list_item_id": "mno123",
            "relationship": "Unrelated",
        },
    ]
    router = relationship_router(relationships=relationships)
    location = relationship_location("abc123", "jkl123")
    next_location = router.get_next_location(location)
    expected_location = relationship_location("abc123", "mno123")
    assert next_location == expected_location


@pytest.mark.parametrize(
    "unrelated_answer, expected_next_location",
    [
        (None, relationship_location("abc123", "jkl123")),
        ("Yes", relationship_location("abc123", "jkl123")),
        ("Yes, they are related", relationship_location("abc123", "jkl123")),
        ("No", relationship_location("def123", "ghi123")),
        ("No, they are not related", relationship_location("def123", "ghi123")),
    ],
)
def test_get_next_location_from_unrelated_question(
    unrelated_answer, expected_next_location
):
    if unrelated_answer:
        answers = [
            {
                "answer_id": "anyone-else-answer",
                "list_item_id": "abc123",
                "value": unrelated_answer,
            }
        ]
    else:
        answers = None

    relationships = [
        {
            "list_item_id": "abc123",
            "to_list_item_id": "def123",
            "relationship": "Unrelated",
        },
        {
            "list_item_id": "abc123",
            "to_list_item_id": "ghi123",
            "relationship": "Unrelated",
        },
    ]
    router = relationship_router(
        answers=answers,
        relationships=relationships,
    )
    location = unrelated_relationship_location("abc123")
    next_location = router.get_next_location(location)
    assert next_location == expected_next_location
