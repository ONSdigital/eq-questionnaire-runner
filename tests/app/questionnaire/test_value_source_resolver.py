from typing import Mapping, Optional, Union

import pytest
from mock import Mock

from app.authentication.auth_payload_version import AuthPayloadVersion
from app.data_models import AnswerStore, ListStore, ProgressStore
from app.data_models.answer import Answer, AnswerDict
from app.data_models.metadata_proxy import MetadataProxy, NoMetadataException
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.location import InvalidLocationException
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.value_source_resolver import ValueSourceResolver
from tests.app.data_model.test_answer import ESCAPED_CONTENT, HTML_CONTENT
from tests.app.questionnaire.conftest import get_metadata


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
    metadata: MetadataProxy = None,
    response_metadata: Mapping = None,
    location: Union[Location, RelationshipLocation] = Location(
        section_id="test-section", block_id="test-block"
    ),
    list_item_id: Optional[str] = None,
    routing_path_block_ids: Optional[list] = None,
    use_default_answer=False,
    escape_answer_values=False,
    progress_store: ProgressStore | None = None,
):
    if not schema:
        schema = get_mock_schema()
        schema.is_repeating_answer = Mock(return_value=bool(list_item_id))

    if not use_default_answer:
        schema.get_default_answer = Mock(return_value=None)

    return ValueSourceResolver(
        answer_store=answer_store,
        list_store=list_store,
        metadata=metadata,
        response_metadata=response_metadata,
        schema=schema,
        location=location,
        list_item_id=list_item_id,
        routing_path_block_ids=routing_path_block_ids,
        use_default_answer=use_default_answer,
        escape_answer_values=escape_answer_values,
        progress_store=progress_store,
    )


def test_answer_source():
    value_source_resolver = get_value_source_resolver(
        answer_store=AnswerStore([{"answer_id": "some-answer", "value": "Yes"}]),
    )

    assert (
        value_source_resolver.resolve(
            {"source": "answers", "identifier": "some-answer"}
        )
        == "Yes"
    )


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

    assert (
        value_source_resolver.resolve(
            {
                "source": "answers",
                "identifier": "some-answer",
                "selector": "years",
            }
        )
        == 1
    )


def test_answer_source_with_list_item_id_no_list_item_selector():
    value_source_resolver = get_value_source_resolver(
        answer_store=AnswerStore(
            [{"answer_id": "some-answer", "list_item_id": "item-1", "value": "Yes"}]
        ),
        list_item_id="item-1",
    )

    assert (
        value_source_resolver.resolve(
            {"source": "answers", "identifier": "some-answer"}
        )
        == "Yes"
    )


def test_list_item_id_ignored_if_answer_not_in_list_collector_or_repeat():
    schema = get_mock_schema()
    schema.is_repeating_answer = Mock(return_value=False)

    value_source_resolver = get_value_source_resolver(
        schema=schema,
        answer_store=AnswerStore([{"answer_id": "some-answer", "value": "Yes"}]),
        list_item_id="item-1",
    )

    assert (
        value_source_resolver.resolve(
            {"source": "answers", "identifier": "some-answer"}
        )
        == "Yes"
    )


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
        value_source_resolver.resolve(
            {
                "source": "answers",
                "identifier": "some-answer",
                "list_item_selector": {
                    "source": "location",
                    "identifier": "list_item_id",
                },
            }
        )
        == "Yes"
    )


def test_answer_source_with_list_item_selector_location_none():
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
        location=None,
    )
    with pytest.raises(InvalidLocationException):
        value_source_resolver.resolve(
            {
                "source": "answers",
                "identifier": "some-answer",
                "list_item_selector": {"source": "location", "id": "list_item_id"},
            }
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
        value_source_resolver.resolve(
            {
                "source": "answers",
                "identifier": "some-answer",
                "list_item_selector": {
                    "source": "list",
                    "identifier": "some-list",
                    "selector": "first",
                },
            }
        )
        == "Yes"
    )


def test_answer_source_outside_of_repeating_section():
    schema = get_mock_schema()

    schema.is_repeating_answer = Mock(return_value=False)
    answer_store = AnswerStore([{"answer_id": "some-answer", "value": "Yes"}])

    value_source_resolver = get_value_source_resolver(
        schema=schema,
        answer_store=answer_store,
        list_store=ListStore([{"name": "some-list", "items": get_list_items(3)}]),
        location=Location(
            section_id="some-section", block_id="some-block", list_item_id="item-1"
        ),
    )

    assert (
        value_source_resolver.resolve(
            {"source": "answers", "identifier": "some-answer"}
        )
        == "Yes"
    )


@pytest.mark.parametrize("is_answer_on_path", [True, False])
def test_answer_source_not_on_path_non_repeating_section(is_answer_on_path):
    schema = get_mock_schema()

    location = Location(section_id="test-section", block_id="test-block")

    if is_answer_on_path:
        schema.get_block_for_answer_id = Mock(return_value={"id": "block-on-path"})
        answer_id = "answer-on-path"
        expected_result = "Yes"
    else:
        schema.get_block_for_answer_id = Mock(return_value={"id": "block-not-on-path"})
        answer_id = "answer-not-on-path"
        expected_result = None

    answer = Answer(answer_id=answer_id, value="Yes")

    value_source_resolver = get_value_source_resolver(
        schema=schema,
        answer_store=AnswerStore([answer.to_dict()]),
        list_store=ListStore([{"name": "some-list", "items": get_list_items(3)}]),
        location=location,
        list_item_id=location.list_item_id,
        routing_path_block_ids=["block-on-path"],
    )

    assert (
        value_source_resolver.resolve(
            {"source": "answers", "identifier": "answer-on-path"}
        )
        == expected_result
    )


@pytest.mark.parametrize("is_answer_on_path", [True, False])
def test_answer_source_not_on_path_repeating_section(is_answer_on_path):
    schema = get_mock_schema()
    schema.is_repeating_answer = Mock(return_value=True)
    location = Location(
        section_id="test-section", block_id="test-block", list_item_id="item-1"
    )

    if is_answer_on_path:
        schema.get_block_for_answer_id = Mock(return_value={"id": "block-on-path"})
        answer_id = "answer-on-path"
        expected_result = "Yes"
    else:
        schema.get_block_for_answer_id = Mock(return_value={"id": "block-not-on-path"})
        answer_id = "answer-not-on-path"
        expected_result = None

    answer = Answer(answer_id=answer_id, list_item_id="item-1", value="Yes")

    value_source_resolver = get_value_source_resolver(
        schema=schema,
        answer_store=AnswerStore([answer.to_dict()]),
        list_store=ListStore([{"name": "some-list", "items": get_list_items(3)}]),
        location=location,
        list_item_id=location.list_item_id,
        routing_path_block_ids=["block-on-path"],
    )

    assert (
        value_source_resolver.resolve(
            {"source": "answers", "identifier": "answer-on-path"}
        )
        == expected_result
    )


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
        use_default_answer=use_default_answer,
    )

    expected_result = "Yes" if use_default_answer else None
    assert (
        value_source_resolver.resolve(
            {"source": "answers", "identifier": "some-answer"}
        )
        == expected_result
    )


@pytest.mark.parametrize(
    "metadata_identifier, expected_result",
    [("region_code", "GB-ENG"), ("language_code", None)],
)
def test_metadata_source(metadata_identifier, expected_result):
    value_source_resolver = get_value_source_resolver(
        metadata=get_metadata({"region_code": "GB-ENG"})
    )

    source = {"source": "metadata", "identifier": metadata_identifier}
    assert value_source_resolver.resolve(source) == expected_result


def test_resolve_metadata_source_with_no_metadata_raises_exception():
    value_source_resolver = get_value_source_resolver(metadata=None)

    source = {"source": "metadata", "identifier": "identifier"}

    with pytest.raises(NoMetadataException):
        value_source_resolver.resolve(source)


@pytest.mark.parametrize(
    "metadata_identifier, expected_result",
    [
        ("region_code", "GB-ENG"),
        ("display_address", "68 Abingdon Road, Goathill"),
        ("language_code", None),
    ],
)
def test_metadata_source_v2_metadata_structure(metadata_identifier, expected_result):
    metadata = get_metadata(
        {
            "version": AuthPayloadVersion.V2,
            "region_code": "GB-ENG",
            "survey_metadata": {
                "data": {"display_address": "68 Abingdon Road, Goathill"}
            },
        }
    )

    value_source_resolver = get_value_source_resolver(metadata=metadata)

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

    assert (
        value_source_resolver.resolve(
            {"source": "list", "identifier": "some-list", "selector": "count"}
        )
        == list_count
    )


def test_list_source_with_id_selector_first():
    value_source_resolver = get_value_source_resolver(
        list_store=ListStore([{"name": "some-list", "items": get_list_items(3)}]),
    )

    assert (
        value_source_resolver.resolve(
            {"source": "list", "identifier": "some-list", "selector": "first"}
        )
        == "item-1"
    )


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
        {
            "source": "list",
            "identifier": "some-list",
            "selector": "same_name_items",
        }
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
        value_source_resolver.resolve(
            {
                "source": "list",
                "identifier": "some-list",
                "selector": "primary_person",
            }
        )
        == primary_person_list_item_id
    )


def test_location_source():
    value_source_resolver = get_value_source_resolver(list_item_id="item-1")
    assert (
        value_source_resolver.resolve(
            {"source": "location", "identifier": "list_item_id"}
        )
        == "item-1"
    )


def test_response_metadata_source():
    value_source_resolver = get_value_source_resolver(
        response_metadata={"started_at": "2021-10-11T09:40:11.220038+00:00"}
    )
    assert (
        value_source_resolver.resolve(
            {"source": "response_metadata", "identifier": "started_at"}
        )
        == "2021-10-11T09:40:11.220038+00:00"
    )


@pytest.mark.parametrize(
    "list_item_id",
    [None, "item-1"],
)
def test_calculated_summary_value_source(mocker, list_item_id):
    schema = mocker.MagicMock()
    schema.get_block = Mock(
        return_value={
            "id": "number-total",
            "type": "CalculatedSummary",
            "calculation": {
                "calculation_type": "sum",
                "answers_to_calculate": ["number-answer-1", "number-answer-2"],
            },
        },
    )

    value_source_resolver = get_value_source_resolver(
        answer_store=AnswerStore(
            [
                AnswerDict(
                    answer_id="number-answer-1", value=10, list_item_id=list_item_id
                ),
                AnswerDict(
                    answer_id="number-answer-2", value=5, list_item_id=list_item_id
                ),
            ]
        ),
        schema=schema,
        list_item_id=list_item_id,
    )
    assert (
        value_source_resolver.resolve(
            {"source": "calculated_summary", "identifier": "number-total"}
        )
        == 15
    )


@pytest.mark.parametrize(
    "list_item_id",
    [None, "item-1"],
)
def test_new_calculated_summary_value_source(mocker, list_item_id):
    schema = mocker.MagicMock()
    schema.get_block = Mock(
        return_value={
            "id": "number-total",
            "type": "CalculatedSummary",
            "calculation": {
                "operation": {
                    "+": [
                        {"source": "answers", "identifier": "number-answer-1"},
                        {"source": "answers", "identifier": "number-answer-2"},
                    ]
                }
            },
        },
    )

    location = Location(
        section_id="test-section", block_id="test-block", list_item_id=list_item_id
    )

    value_source_resolver = get_value_source_resolver(
        answer_store=AnswerStore(
            [
                AnswerDict(
                    answer_id="number-answer-1",
                    value=10,
                    list_item_id=location.list_item_id,
                ),
                AnswerDict(
                    answer_id="number-answer-2", value=5, list_item_id=list_item_id
                ),
            ]
        ),
        schema=schema,
        list_item_id=list_item_id,
        location=location,
    )
    assert (
        value_source_resolver.resolve(
            {"source": "calculated_summary", "identifier": "number-total"}
        )
        == 15
    )


@pytest.mark.parametrize(
    "list_item_id",
    [None, "item-1"],
)
def test_new_calculated_summary_nested_value_source(mocker, list_item_id):
    schema = mocker.MagicMock()
    schema.get_block = Mock(
        return_value={
            "id": "number-total",
            "type": "CalculatedSummary",
            "calculation": {
                "operation": {
                    "+": [
                        {
                            "+": [
                                {"source": "answers", "identifier": "number-answer-1"},
                                {"source": "answers", "identifier": "number-answer-2"},
                            ]
                        },
                        {"source": "answers", "identifier": "number-answer-3"},
                    ]
                }
            },
        },
    )

    location = Location(
        section_id="test-section", block_id="test-block", list_item_id=list_item_id
    )

    value_source_resolver = get_value_source_resolver(
        answer_store=AnswerStore(
            [
                AnswerDict(
                    answer_id="number-answer-1", value=10, list_item_id=list_item_id
                ),
                AnswerDict(
                    answer_id="number-answer-2", value=5, list_item_id=list_item_id
                ),
                AnswerDict(
                    answer_id="number-answer-3", value=5, list_item_id=list_item_id
                ),
            ]
        ),
        schema=schema,
        list_item_id=list_item_id,
        location=location,
    )
    assert (
        value_source_resolver.resolve(
            {"source": "calculated_summary", "identifier": "number-total"}
        )
        == 20
    )


@pytest.mark.parametrize(
    "answer_value, escaped_value",
    [
        (HTML_CONTENT, ESCAPED_CONTENT),
        ([HTML_CONTENT, "some value"], [ESCAPED_CONTENT, "some value"]),
        (1, 1),
        (None, None),
    ],
)
def test_answer_value_can_be_escaped(answer_value, escaped_value):
    value_source_resolver = get_value_source_resolver(
        answer_store=AnswerStore(
            [
                {
                    "answer_id": "some-answer",
                    "value": answer_value,
                }
            ]
        ),
        escape_answer_values=True,
    )
    assert (
        value_source_resolver.resolve(
            {"source": "answers", "identifier": "some-answer"}
        )
        == escaped_value
    )


def test_answer_value_with_selector_can_be_escaped():
    value_source_resolver = get_value_source_resolver(
        answer_store=AnswerStore(
            [
                {
                    "answer_id": "some-answer",
                    "value": {"key_1": HTML_CONTENT, "key_2": 1},
                }
            ]
        ),
        escape_answer_values=True,
    )
    assert (
        value_source_resolver.resolve(
            {"source": "answers", "identifier": "some-answer", "selector": "key_1"}
        )
        == ESCAPED_CONTENT
    )


def test_progress_values_source_throws_if_no_location_given():
    value_source_resolver = get_value_source_resolver(
        progress_store=ProgressStore(), location=None
    )
    with pytest.raises(ValueError):
        value_source_resolver.resolve(
            {"source": "progress", "selector": "block", "identifier": "a-block"}
        )
