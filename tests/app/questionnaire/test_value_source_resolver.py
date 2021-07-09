from typing import Optional, Union
from unittest.mock import Mock

import pytest

from app.data_models import AnswerStore, ListStore
from app.data_models.answer import Answer
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.value_source_resolver import ValueSourceResolver

answer_source = {"source": "answers", "identifier": "some-answer"}
answer_source_dict_answer_selector = {
    **answer_source,
    "selector": "years",
}
answer_source_list_item_selector_location = {
    **answer_source,
    "list_item_selector": {"source": "location", "id": "list_item_id"},
}
answer_source_list_item_selector_list_first_item = {
    **answer_source,
    "list_item_selector": {"source": "list", "id": "some-list", "id_selector": "first"},
}

metadata_source = {"source": "metadata", "identifier": "some-metadata"}

list_source = {"source": "list", "identifier": "some-list"}
list_source_id_selector_first = {**list_source, "id_selector": "first"}
list_source_id_selector_primary_person = {
    **list_source,
    "id_selector": "primary_person",
}
list_source_id_selector_same_name_items = {
    **list_source,
    "id_selector": "same_name_items",
}

location_source = {"source": "location", "identifier": "list_item_id"}


def get_list_items(num: int):
    return [f"item-{i}" for i in range(1, num + 1)]


def get_mock_schema():
    schema = Mock(
        QuestionnaireSchema(
            {
                "questionnaire_flow": {
                    "type": "Linear",
                    "options": {"summary": {"collapsible": False}},
                }
            }
        )
    )
    return schema


def get_value_source_resolver(
    schema: QuestionnaireSchema = None,
    answer_store: AnswerStore = AnswerStore(),
    list_store: ListStore = ListStore(),
    metadata: Optional[dict] = None,
    location: Union[Location, RelationshipLocation] = Location(
        section_id="test-section", block_id="test-block"
    ),
    list_item_id: Optional[str] = None,
    routing_path_block_ids: Optional[list] = None,
    use_default_answer=False,
):
    if not schema:
        schema = get_mock_schema()
        schema.answer_should_have_list_item_id = Mock(return_value=bool(list_item_id))

    if not use_default_answer:
        schema.get_default_answer = Mock(return_value=None)

    return ValueSourceResolver(
        answer_store=answer_store,
        list_store=list_store,
        metadata=metadata,
        schema=schema,
        location=location,
        list_item_id=list_item_id,
        routing_path_block_ids=routing_path_block_ids,
        use_default_answer=use_default_answer,
    )


def test_answer_source():
    value_source_resolver = get_value_source_resolver(
        answer_store=AnswerStore([{"answer_id": "some-answer", "value": "Yes"}]),
    )

    assert value_source_resolver.resolve(answer_source) == "Yes"


def test_answer_source_with_dict_answer_selector():
    value_source_resolver = get_value_source_resolver(
        answer_store=AnswerStore(
            [
                {
                    "answer_id": "some-answer",
                    "value": {"years": 1, "months": 10},
                }
            ]
        ),
    )

    assert value_source_resolver.resolve(answer_source_dict_answer_selector) == 1


def test_answer_source_with_list_item_id_no_list_item_selector():
    value_source_resolver = get_value_source_resolver(
        answer_store=AnswerStore(
            [{"answer_id": "some-answer", "list_item_id": "item-1", "value": "Yes"}]
        ),
        list_item_id="item-1",
    )

    assert value_source_resolver.resolve(answer_source) == "Yes"


def test_answer_source_with_list_item_id_but_answer_not_in_list_collector_or_repeat():
    schema = get_mock_schema()
    schema.answer_should_have_list_item_id = Mock(return_value=False)

    value_source_resolver = get_value_source_resolver(
        schema=schema,
        answer_store=AnswerStore(
            [{"answer_id": "some-answer", "list_item_id": "item-1", "value": "Yes"}]
        ),
        list_item_id="item-1",
    )

    assert value_source_resolver.resolve(answer_source) is None

    value_source_resolver = get_value_source_resolver(
        schema=schema,
        answer_store=AnswerStore([{"answer_id": "some-answer", "value": "Yes"}]),
        list_item_id="item-1",
    )

    assert value_source_resolver.resolve(answer_source) == "Yes"


def test_answer_source_with_list_item_selector_location():
    value_source_resolver = get_value_source_resolver(
        answer_store=AnswerStore(
            [
                {
                    "answer_id": "some-answer",
                    "list_item_id": "item-1",
                    "value": "Yes",
                }
            ]
        ),
        location=Location(
            section_id="some-section", block_id="some-block", list_item_id="item-1"
        ),
    )

    assert (
        value_source_resolver.resolve(answer_source_list_item_selector_location)
        == "Yes"
    )


def test_answer_source_with_list_item_selector_list_first_item():
    value_source_resolver = get_value_source_resolver(
        answer_store=AnswerStore(
            [
                {
                    "answer_id": "some-answer",
                    "list_item_id": "item-1",
                    "value": "Yes",
                }
            ]
        ),
        list_store=ListStore([{"name": "some-list", "items": get_list_items(3)}]),
    )

    assert (
        value_source_resolver.resolve(answer_source_list_item_selector_list_first_item)
        == "Yes"
    )


@pytest.mark.parametrize("is_answer_on_path", [True, False])
@pytest.mark.parametrize("is_inside_repeat", [True, False])
def test_answer_source_with_routing_path_block_ids(is_answer_on_path, is_inside_repeat):
    schema = get_mock_schema()
    schema.get_block_for_answer_id = Mock(return_value={"id": f"some-block"})

    location = Location(section_id="test-section", block_id="test-block")
    id_prefix = "some" if is_answer_on_path else "some-other"
    answer = Answer(answer_id=f"{id_prefix}-answer", value="Yes")

    if is_inside_repeat:
        location.list_item_id = answer.list_item_id = "item-1"
        schema.answer_should_have_list_item_id = Mock(return_value=True)
    else:
        schema.answer_should_have_list_item_id = Mock(return_value=True)

    value_source_resolver = get_value_source_resolver(
        schema=schema,
        answer_store=AnswerStore([answer.to_dict()]),
        list_store=ListStore([{"name": "some-list", "items": get_list_items(3)}]),
        location=location,
        list_item_id=location.list_item_id,
        routing_path_block_ids=[f"{id_prefix}-block"],
    )

    expected_result = "Yes" if is_answer_on_path else None
    assert value_source_resolver.resolve(answer_source) == expected_result


@pytest.mark.parametrize("use_default_answer", [True, False])
def test_answer_source_default_answer(use_default_answer):
    schema = get_mock_schema()
    if use_default_answer:
        schema.get_default_answer = Mock(
            return_value=Answer(answer_id="some-answer", value="Yes")
        )
    else:
        schema.get_default_answer = Mock(return_value=None)

    value_source_resolver = get_value_source_resolver(
        schema=schema,
        answer_store=AnswerStore([{"answer_id": f"some-other-answer", "value": "No"}]),
        use_default_answer=use_default_answer,
    )

    expected_result = "Yes" if use_default_answer else None
    assert value_source_resolver.resolve(answer_source) == expected_result


@pytest.mark.parametrize(
    "metadata_identifier, expected_result",
    [("region_code", "GB-ENG"), ("language_code", None)],
)
def test_metadata_source(metadata_identifier, expected_result):
    value_source_resolver = get_value_source_resolver(
        metadata={"region_code": "GB-ENG"},
    )

    source = {"source": "metadata", "identifier": metadata_identifier}
    assert value_source_resolver.resolve(source) == expected_result


@pytest.mark.parametrize(
    "list_count",
    [0, 1, 5, 10],
)
def test_list_source(list_count):
    value_source_resolver = get_value_source_resolver(
        list_store=ListStore(
            [{"name": "some-list", "items": get_list_items(list_count)}]
        ),
    )

    assert value_source_resolver.resolve(list_source) == list_count


def test_list_source_with_id_selector_first():
    value_source_resolver = get_value_source_resolver(
        list_store=ListStore([{"name": "some-list", "items": get_list_items(3)}]),
    )

    assert value_source_resolver.resolve(list_source_id_selector_first) == "item-1"


def test_list_source_with_id_selector_same_name_items():
    value_source_resolver = get_value_source_resolver(
        list_store=ListStore(
            [
                {
                    "name": "some-list",
                    "items": get_list_items(5),
                    "same_name_items": get_list_items(3),
                }
            ]
        ),
    )

    assert value_source_resolver.resolve(
        list_source_id_selector_same_name_items
    ) == get_list_items(3)


@pytest.mark.parametrize(
    "primary_person_list_item_id",
    ["item-1", "item-2"],
)
def test_list_source_id_selector_primary_person(primary_person_list_item_id):
    value_source_resolver = get_value_source_resolver(
        list_store=ListStore(
            [
                {
                    "name": "some-list",
                    "primary_person": primary_person_list_item_id,
                    "items": get_list_items(3),
                }
            ]
        ),
    )

    assert (
        value_source_resolver.resolve(list_source_id_selector_primary_person)
        == primary_person_list_item_id
    )


def test_location_source():
    value_source_resolver = get_value_source_resolver(list_item_id="item-1")
    assert value_source_resolver.resolve(location_source) == "item-1"


def test_list_of_sources():
    value_source_resolver = get_value_source_resolver(
        answer_store=AnswerStore(
            [
                {
                    "answer_id": "first-name",
                    "list_item_id": "item-1",
                    "value": "John",
                },
                {
                    "answer_id": "second-name",
                    "list_item_id": "item-1",
                    "value": "Doe",
                },
            ]
        ),
        list_item_id="item-1",
    )
    list_of_sources = [
        {"source": "answers", "identifier": "first-name"},
        {"source": "answers", "identifier": "second-name"},
    ]
    assert value_source_resolver.resolve(list_of_sources) == ["John", "Doe"]


def test_list_of_sources_with_list_values_are_flattened():
    value_source_resolver = get_value_source_resolver(
        answer_store=AnswerStore(
            [
                {
                    "answer_id": "primary-hobby",
                    "list_item_id": "item-1",
                    "value": "Cricket",
                },
                {
                    "answer_id": "other-hobbies",
                    "list_item_id": "item-1",
                    "value": ["Football", "Basketball"],
                },
            ]
        ),
        list_item_id="item-1",
    )
    list_of_sources = [
        {"source": "answers", "identifier": "primary-hobby"},
        {"source": "answers", "identifier": "other-hobbies"},
    ]
    assert value_source_resolver.resolve(list_of_sources) == [
        "Cricket",
        "Football",
        "Basketball",
    ]
