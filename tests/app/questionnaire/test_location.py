import pytest

from app.questionnaire.location import Location


@pytest.mark.usefixtures("app")
def test_location_url():
    location = Location(section_id="some-section", block_id="some-block")
    assert (
        location.url(_external=True)
        == "http://test.localdomain/questionnaire/some-block/"
    )


@pytest.mark.usefixtures("app")
def test_location_url_with_list():
    location = Location(
        section_id="some-section", block_id="add-block", list_name="people"
    )
    assert (
        location.url(_external=True)
        == "http://test.localdomain/questionnaire/people/add-block/"
    )


@pytest.mark.usefixtures("app")
def test_location_url_with_list_item_id():
    location = Location(
        section_id="some-section",
        block_id="add-block",
        list_name="people",
        list_item_id="abc123",
    )
    assert (
        location.url(_external=True)
        == "http://test.localdomain/questionnaire/people/abc123/add-block/"
    )


def test_location_hash():
    location = Location(section_id="some-section", block_id="some-block")

    assert hash(location) == hash(frozenset(location.__dict__.values()))


def test_load_location_from_dict():
    location_dict = {
        "section_id": "some-section",
        "block_id": "some-block",
        "list_name": "people",
        "list_item_id": "adhjiiw",
    }

    location = Location.from_dict(location_dict)

    assert location.section_id == "some-section"
    assert location.block_id == "some-block"
    assert location.list_item_id == "adhjiiw"
    assert location.list_name == "people"


def test_load_location_from_dict_without_list_item_id():
    location_dict = {"section_id": "some-section", "block_id": "some-block"}

    location = Location.from_dict(location_dict)

    assert location.section_id == "some-section"
    assert location.block_id == "some-block"
    assert location.list_item_id is None
    assert location.list_name is None
