import pytest

from app.questionnaire.location import SectionKey
from app.questionnaire.relationship_location import RelationshipLocation


@pytest.mark.usefixtures("app")
def test_location_url():
    location = RelationshipLocation(
        section_id="household",
        block_id="relationships",
        list_item_id="id1",
        to_list_item_id="id2",
        list_name="household",
    )
    location_url = location.url()

    assert location_url == "/questionnaire/relationships/household/id1/to/id2/"

    assert location.for_json() == {
        "section_id": "household",
        "block_id": "relationships",
        "list_item_id": "id1",
        "to_list_item_id": "id2",
        "list_name": "household",
    }


def test_create_location_from_dict():
    location_dict = {
        "section_id": "household",
        "block_id": "relationships",
        "list_item_id": "id1",
        "to_list_item_id": "id2",
        "list_name": "household",
    }

    location = RelationshipLocation(**location_dict)

    assert location.section_id == "household"
    assert location.block_id == "relationships"
    assert location.list_item_id == "id1"
    assert location.to_list_item_id == "id2"
    assert location.section_key == SectionKey(
        section_id=location.section_id, list_item_id=location.list_item_id
    )
