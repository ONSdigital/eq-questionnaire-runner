# pylint: disable=too-many-lines
from typing import Optional, Union

import pytest
from mock import MagicMock, Mock

from app.authentication.auth_payload_versions import AuthPayloadVersion
from app.data_models import AnswerStore, ListStore, ProgressStore
from app.data_models.answer import Answer, AnswerDict
from app.data_models.data_stores import DataStores
from app.data_models.metadata_proxy import NoMetadataException
from app.data_models.supplementary_data_store import InvalidSupplementaryDataSelector
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.location import InvalidLocationException
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.value_source_resolver import ValueSourceResolver
from tests.app.data_model.test_answer import ESCAPED_CONTENT, HTML_CONTENT
from tests.app.questionnaire.conftest import get_metadata


def get_list_items(num: int):
    return [f"item-{i}" for i in range(1, num + 1)]


def get_mock_schema():
    schema = MagicMock(
        QuestionnaireSchema(
            {
                "questionnaire_flow": {
                    "type": "Linear",
                    "options": {"summary": {"collapsible": False}},
                }
            }
        )
    )
    schema.is_answer_dynamic = Mock(return_value=False)
    schema.is_answer_in_list_collector_repeating_block = Mock(return_value=False)
    return schema


def get_calculation_block(
    block_id: str, summary_type: str, source_type: str, identifiers: list[str]
) -> dict:
    return {
        "id": block_id,
        "type": summary_type,
        "calculation": {
            "operation": {
                "+": [
                    {
                        "source": source_type,
                        "identifier": identifier,
                    }
                    for identifier in identifiers
                ]
            }
        },
    }


def get_value_source_resolver(
    schema: QuestionnaireSchema = None,
    data_stores: DataStores = None,
    location: Union[Location, RelationshipLocation] = Location(
        section_id="test-section", block_id="test-block"
    ),
    list_item_id: Optional[str] = None,
    routing_path_block_ids: Optional[list] = None,
    use_default_answer=False,
    escape_answer_values=False,
):
    data_stores = data_stores or DataStores()
    if not schema:
        schema = get_mock_schema()
        schema.is_repeating_answer = Mock(return_value=bool(list_item_id))
        schema.get_list_name_for_answer_id = Mock(
            return_value="list" if list_item_id else None
        )
        schema.is_answer_dynamic = Mock(return_value=False)
        schema.is_answer_in_list_collector_repeating_block = Mock(return_value=False)

    if not use_default_answer:
        schema.get_default_answer = Mock(return_value=None)

    return ValueSourceResolver(
        data_stores=data_stores,
        schema=schema,
        location=location,
        list_item_id=list_item_id,
        routing_path_block_ids=routing_path_block_ids,
        use_default_answer=use_default_answer,
        escape_answer_values=escape_answer_values,
    )


def test_answer_source():
    value_source_resolver = get_value_source_resolver(
        data_stores=DataStores(
            answer_store=AnswerStore([{"answer_id": "some-answer", "value": "Yes"}])
        ),
    )

    assert (
        value_source_resolver.resolve(
            {"source": "answers", "identifier": "some-answer"}
        )
        == "Yes"
    )


def test_answer_source_with_dict_answer_selector():
    value_source_resolver = get_value_source_resolver(
        data_stores=DataStores(
            answer_store=AnswerStore(
                [
                    {
                        "answer_id": "some-answer",
                        "value": {"years": 1, "months": 10},
                    }
                ]
            ),
        )
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
        data_stores=DataStores(
            answer_store=AnswerStore(
                [{"answer_id": "some-answer", "list_item_id": "item-1", "value": "Yes"}]
            )
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
    schema.get_list_name_for_answer_id = Mock(return_value=None)

    value_source_resolver = get_value_source_resolver(
        schema=schema,
        data_stores=DataStores(
            answer_store=AnswerStore([{"answer_id": "some-answer", "value": "Yes"}])
        ),
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
        data_stores=DataStores(
            answer_store=AnswerStore(
                [
                    {
                        "answer_id": "some-answer",
                        "list_item_id": "item-1",
                        "value": "Yes",
                    }
                ]
            )
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
        data_stores=DataStores(
            answer_store=AnswerStore(
                [
                    {
                        "answer_id": "some-answer",
                        "list_item_id": "item-1",
                        "value": "Yes",
                    }
                ]
            )
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
        data_stores=DataStores(
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
        ),
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

    schema.get_list_name_for_answer_id = Mock(return_value=None)
    answer_store = AnswerStore([{"answer_id": "some-answer", "value": "Yes"}])

    value_source_resolver = get_value_source_resolver(
        schema=schema,
        data_stores=DataStores(
            answer_store=answer_store,
            list_store=ListStore([{"name": "some-list", "items": get_list_items(3)}]),
        ),
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
        data_stores=DataStores(
            answer_store=AnswerStore([answer.to_dict()]),
            list_store=ListStore([{"name": "some-list", "items": get_list_items(3)}]),
        ),
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
    schema.get_list_name_for_answer_id = Mock(return_value="some-list")
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
        data_stores=DataStores(
            answer_store=AnswerStore([answer.to_dict()]),
            list_store=ListStore([{"name": "some-list", "items": get_list_items(3)}]),
        ),
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
    "answer_values,escape_answer_values",
    (([], False), ([10, 5], False), ([100, 200, 300], False), ([HTML_CONTENT], True)),
)
def test_answer_source_dynamic_answer(
    mocker,
    placeholder_transform_question_dynamic_answers_json,
    answer_values,
    escape_answer_values,
):
    """
    Tests that a dynamic answer id as a value source resolves to the list of answers for that list and question
    """
    schema = mocker.MagicMock()
    schema.is_answer_dynamic = Mock(return_value=True)
    schema.get_block_for_answer_id = Mock(
        return_value={"question": placeholder_transform_question_dynamic_answers_json}
    )
    list_item_ids = get_list_items(len(answer_values))
    value_source_resolver = get_value_source_resolver(
        data_stores=DataStores(
            answer_store=AnswerStore(
                [
                    AnswerDict(
                        answer_id="percentage-of-shopping",
                        value=value,
                        list_item_id=list_item_id,
                    )
                    for list_item_id, value in zip(list_item_ids, answer_values)
                ]
            ),
            list_store=ListStore([{"name": "supermarkets", "items": list_item_ids}]),
        ),
        schema=schema,
        escape_answer_values=escape_answer_values,
    )
    expected_result = [ESCAPED_CONTENT] if escape_answer_values else answer_values
    assert (
        value_source_resolver.resolve(
            {"source": "answers", "identifier": "percentage-of-shopping"}
        )
        == expected_result
    )


@pytest.mark.parametrize(
    "answer_values, list_name, list_item_id, expected",
    (
        ([10, 5], "supermarkets", "item-1", 10),
        ([10, 5], "cars", "item-1", [10, 5]),
        ([10, 5], None, None, [10, 5]),
    ),
)
def test_answer_source_dynamic_answer_in_different_repeat(
    placeholder_transform_question_dynamic_answers_json,
    answer_values,
    list_name,
    list_item_id,
    expected,
):
    """
    Tests that a dynamic answer id as a value source resolves to the specific instance in the context of a repeat
    and the list of all answers when outside a repeat or in a repeat for a different list.
    """
    schema = MagicMock()
    schema.is_answer_dynamic = Mock(return_value=True)
    schema.get_block_for_answer_id = Mock(
        return_value={"question": placeholder_transform_question_dynamic_answers_json}
    )
    schema.get_list_name_for_answer_id = Mock(return_value="supermarkets")
    list_item_ids = get_list_items(len(answer_values))
    value_source_resolver = get_value_source_resolver(
        data_stores=DataStores(
            answer_store=AnswerStore(
                [
                    AnswerDict(
                        answer_id="percentage-of-shopping",
                        value=value,
                        list_item_id=list_item_id,
                    )
                    for list_item_id, value in zip(list_item_ids, answer_values)
                ]
            ),
            list_store=ListStore([{"name": "supermarkets", "items": list_item_ids}]),
        ),
        location=Location(
            section_id="section-1", list_name=list_name, list_item_id=list_item_id
        ),
        list_item_id=list_item_id,
        schema=schema,
    )
    assert (
        value_source_resolver.resolve(
            {"source": "answers", "identifier": "percentage-of-shopping"}
        )
        == expected
    )


@pytest.mark.parametrize(
    "answer_values, list_name, list_item_id, expected",
    (
        ([], None, None, []),
        ([10, 5], None, None, [10, 5]),
        ([100, 200, 300], None, None, [100, 200, 300]),
        ([10, 5], "transport", "item-1", 10),
        ([100, 200, 300], "transport", "item-2", 200),
        ([10, 5], "shopping", "item-1", [10, 5]),
        ([100, 200, 300], "shopping", "item-2", [100, 200, 300]),
    ),
)
def test_answer_source_repeating_block_answers_in_repeat(
    placeholder_transform_question_repeating_block,
    answer_values,
    list_name,
    list_item_id,
    expected,
):
    """
    Tests that an answer id from a repeating block resolves to the specific answer in the context of a repeat.
    And the list of answers for that list and repeating block question outside a repeat or in a repeat for another list.
    """
    schema = MagicMock()
    schema.list_names_by_list_repeating_block_id = {"repeating-block-1": "transport"}
    schema.is_answer_dynamic = Mock(return_value=False)
    schema.get_list_name_for_answer_id = Mock(return_value="transport")
    schema.get_block_for_answer_id = Mock(
        return_value=placeholder_transform_question_repeating_block
    )
    list_item_ids = get_list_items(len(answer_values))
    value_source_resolver = get_value_source_resolver(
        data_stores=DataStores(
            answer_store=AnswerStore(
                [
                    AnswerDict(
                        answer_id="transport-cost",
                        value=value,
                        list_item_id=list_item_id,
                    )
                    for list_item_id, value in zip(list_item_ids, answer_values)
                ]
            ),
            list_store=ListStore([{"name": "transport", "items": list_item_ids}]),
        ),
        schema=schema,
        location=Location(
            section_id="section-1", list_name=list_name, list_item_id=list_item_id
        ),
        list_item_id=list_item_id,
    )
    assert (
        value_source_resolver.resolve(
            {"source": "answers", "identifier": "transport-cost"}
        )
        == expected
    )


@pytest.mark.parametrize(
    "metadata_identifier, expected_result",
    [("region_code", "GB-ENG"), ("language_code", None)],
)
def test_metadata_source(metadata_identifier, expected_result):
    value_source_resolver = get_value_source_resolver(
        data_stores=DataStores(metadata=get_metadata({"region_code": "GB-ENG"}))
    )

    source = {"source": "metadata", "identifier": metadata_identifier}
    assert value_source_resolver.resolve(source) == expected_result


def test_resolve_metadata_source_with_no_metadata_raises_exception():
    value_source_resolver = get_value_source_resolver()

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

    value_source_resolver = get_value_source_resolver(
        data_stores=DataStores(metadata=metadata)
    )

    source = {"source": "metadata", "identifier": metadata_identifier}
    assert value_source_resolver.resolve(source) == expected_result


@pytest.mark.parametrize(
    "list_count",
    [0, 1, 5, 10],
)
def test_list_source(list_count):
    value_source_resolver = get_value_source_resolver(
        data_stores=DataStores(
            list_store=ListStore(
                [{"name": "some-list", "items": get_list_items(list_count)}]
            )
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
        data_stores=DataStores(
            list_store=ListStore([{"name": "some-list", "items": get_list_items(3)}])
        ),
    )

    assert (
        value_source_resolver.resolve(
            {"source": "list", "identifier": "some-list", "selector": "first"}
        )
        == "item-1"
    )


def test_list_source_with_id_selector_same_name_items():
    value_source_resolver = get_value_source_resolver(
        data_stores=DataStores(
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
        data_stores=DataStores(
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
        data_stores=DataStores(
            response_metadata={"started_at": "2021-10-11T09:40:11.220038+00:00"}
        )
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
        data_stores=DataStores(
            answer_store=AnswerStore(
                [
                    AnswerDict(
                        answer_id="number-answer-1", value=10, list_item_id=list_item_id
                    ),
                    AnswerDict(
                        answer_id="number-answer-2", value=5, list_item_id=list_item_id
                    ),
                ]
            )
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
    schema.is_answer_dynamic = Mock(return_value=False)
    schema.is_answer_in_list_collector_repeating_block = Mock(return_value=False)

    location = Location(
        section_id="test-section", block_id="test-block", list_item_id=list_item_id
    )

    value_source_resolver = get_value_source_resolver(
        data_stores=DataStores(
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
            )
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
    schema.is_answer_dynamic = Mock(return_value=False)
    schema.is_answer_in_list_collector_repeating_block = Mock(return_value=False)

    location = Location(
        section_id="test-section", block_id="test-block", list_item_id=list_item_id
    )

    value_source_resolver = get_value_source_resolver(
        data_stores=DataStores(
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
            )
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
    "gcs_list_item_id, cs_list_item_id_1, cs_list_item_id_2",
    [
        (None, None, None),
        ("item-1", "item-1", "item-1"),
        ("item-1", "item-1", None),
        ("item-1", None, None),
    ],
)
def test_grand_calculated_summary_value_source(
    mocker, gcs_list_item_id, cs_list_item_id_1, cs_list_item_id_2
):
    """
    Mocks out the grand calculated summary block and its child calculated summary blocks and tests
    that the value source resolver correctly sums up all child answers when
    1) The GCS is in a repeat alongside both CS
    2) The GCS is in a repeat alongside one CS
    3) The GCS is in a repeat but neither CS is
    3) The GCS is not in a repeat and neither CS is
    """
    schema = mocker.MagicMock()

    def mock_get_block(block_id: str) -> dict:
        blocks = {
            "number-total": get_calculation_block(
                "number-total",
                "GrandCalculatedSummary",
                "calculated_summary",
                ["calculated-summary-1", "calculated-summary-2"],
            ),
            "calculated-summary-1": get_calculation_block(
                "calculated-summary-1",
                "CalculatedSummary",
                "answers",
                ["answer-1", "answer-2"],
            ),
            "calculated-summary-2": get_calculation_block(
                "calculated-summary-2",
                "CalculatedSummary",
                "answers",
                ["answer-3", "answer-4"],
            ),
        }
        return blocks[block_id]

    def mock_get_list_name_for_answer_id(answer_id: str) -> str | None:
        return (
            "mock-list"
            if (answer_id in {"answer-1", "answer-2"} and cs_list_item_id_1)
            or (answer_id in {"answer-3", "answer-4"} and cs_list_item_id_2)
            else None
        )

    schema.get_block = Mock(side_effect=mock_get_block)
    schema.get_list_name_for_answer_id = Mock(
        side_effect=mock_get_list_name_for_answer_id
    )
    schema.is_answer_dynamic = Mock(return_value=False)
    schema.is_answer_in_list_collector_repeating_block = Mock(return_value=False)

    location = Location(
        section_id="test-section",
        block_id="test-block",
        list_item_id=gcs_list_item_id,
    )

    value_source_resolver = get_value_source_resolver(
        data_stores=DataStores(
            answer_store=AnswerStore(
                [
                    AnswerDict(
                        answer_id="answer-1", value=10, list_item_id=cs_list_item_id_1
                    ),
                    AnswerDict(
                        answer_id="answer-2", value=5, list_item_id=cs_list_item_id_1
                    ),
                    AnswerDict(
                        answer_id="answer-3", value=20, list_item_id=cs_list_item_id_2
                    ),
                    AnswerDict(
                        answer_id="answer-4", value=30, list_item_id=cs_list_item_id_2
                    ),
                ]
            )
        ),
        schema=schema,
        list_item_id=gcs_list_item_id,
        location=location,
    )
    assert (
        value_source_resolver.resolve(
            {"source": "grand_calculated_summary", "identifier": "number-total"}
        )
        == 65
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
        data_stores=DataStores(
            answer_store=AnswerStore(
                [
                    {
                        "answer_id": "some-answer",
                        "value": answer_value,
                    }
                ]
            )
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
        data_stores=DataStores(
            answer_store=AnswerStore(
                [
                    {
                        "answer_id": "some-answer",
                        "value": {"key_1": HTML_CONTENT, "key_2": 1},
                    }
                ]
            )
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
        data_stores=DataStores(progress_store=ProgressStore()), location=None
    )
    with pytest.raises(ValueError):
        value_source_resolver.resolve(
            {"source": "progress", "selector": "block", "identifier": "a-block"}
        )


@pytest.mark.parametrize("in_repeating_section", [True, False])
@pytest.mark.parametrize(
    "value_source,expected_result",
    [
        (
            {"identifier": "guidance"},
            "Some supplementary guidance about the survey",
        ),
        (
            {"identifier": "note", "selectors": ["title"]},
            "Volume of total production",
        ),
        (
            {"identifier": "note", "selectors": ["example", "title"]},
            "Including",
        ),
        (
            {"identifier": "note", "selectors": ["example", "description"]},
            "Sales across all UK stores",
        ),
        (
            {"identifier": "note", "selectors": ["invalid", "description"]},
            None,
        ),
        (
            {"identifier": "INVALID"},
            None,
        ),
    ],
)
def test_supplementary_data_value_source_non_list_items(
    supplementary_data_store_with_data,
    value_source,
    expected_result,
    in_repeating_section,
):
    list_store = ListStore([{"name": "some-list", "items": get_list_items(3)}])
    location = (
        Location(
            section_id="section",
            block_id="block-id",
            list_name="some-list",
            list_item_id="item-1",
        )
        if in_repeating_section
        else Location(section_id="section", block_id="block-id")
    )
    value_source_resolver = get_value_source_resolver(
        data_stores=DataStores(
            supplementary_data_store=supplementary_data_store_with_data,
            list_store=list_store,
        ),
        location=location,
        list_item_id=location.list_item_id,
    )
    assert (
        value_source_resolver.resolve(
            {
                "source": "supplementary_data",
                **value_source,
            }
        )
        == expected_result
    )


@pytest.mark.parametrize(
    "list_item_id, value_source ,expected_result",
    [
        (
            "item-1",
            {"identifier": "products", "selectors": ["name"]},
            "Articles and equipment for sports or outdoor games",
        ),
        (
            "item-1",
            {"identifier": "products", "selectors": ["value_sales", "answer_code"]},
            "89929001",
        ),
        (
            "item-1",
            {"identifier": "products", "selectors": ["value_sales", "label"]},
            "Value of sales",
        ),
        (
            "item-1",
            {"identifier": "products", "selectors": ["guidance", "description"]},
            "sportswear",
        ),
        (
            "item-2",
            {"identifier": "products", "selectors": ["guidance", "description"]},
            None,
        ),
        (
            "item-2",
            {"identifier": "products", "selectors": ["non_existing_optional_key"]},
            None,
        ),
        (
            "item-2",
            {"identifier": "products", "selectors": ["name"]},
            "Other Minerals",
        ),
        (
            "item-2",
            {"identifier": "products", "selectors": ["value_sales", "answer_code"]},
            "201630601",
        ),
        (
            None,
            {"identifier": "products", "selectors": ["name"]},
            ["Articles and equipment for sports or outdoor games", "Other Minerals"],
        ),
        (
            None,
            {"identifier": "products", "selectors": ["value_sales", "answer_code"]},
            ["89929001", "201630601"],
        ),
        (
            None,
            {"identifier": "products", "selectors": ["non_existing_optional_key"]},
            [],
        ),
    ],
)
def test_supplementary_data_value_source_list_items(
    supplementary_data_store_with_data,
    list_item_id,
    value_source,
    expected_result,
):
    list_store = ListStore([{"name": "products", "items": get_list_items(2)}])
    location = Location(
        section_id="section",
        block_id="block-id",
        list_name="products",
        list_item_id=list_item_id,
    )
    value_source_resolver = get_value_source_resolver(
        data_stores=DataStores(
            supplementary_data_store=supplementary_data_store_with_data,
            list_store=list_store,
        ),
        location=location,
        list_item_id=list_item_id,
    )
    assert (
        value_source_resolver.resolve(
            {
                "source": "supplementary_data",
                **value_source,
            }
        )
        == expected_result
    )


def test_supplementary_data_value_source_list_items_value_missing_excluded(
    supplementary_data_store_with_data_extra_item,
):
    list_store = ListStore([{"name": "products", "items": get_list_items(3)}])
    location = Location(
        section_id="section",
        block_id="block-id",
        list_name="products",
        list_item_id=None,
    )
    value_source_resolver = get_value_source_resolver(
        data_stores=DataStores(
            supplementary_data_store=supplementary_data_store_with_data_extra_item,
            list_store=list_store,
        ),
        location=location,
        list_item_id=None,
    )
    assert value_source_resolver.resolve(
        {
            "source": "supplementary_data",
            **{"identifier": "products", "selectors": ["name"]},
        }
    ) == ["Articles and equipment for sports or outdoor games", "Other Minerals"]


def test_supplementary_data_invalid_selector_raises_exception(
    supplementary_data_store_with_data,
):
    location = Location(
        section_id="section",
        block_id="block-id",
    )
    value_source_resolver = get_value_source_resolver(
        data_stores=DataStores(
            supplementary_data_store=supplementary_data_store_with_data
        ),
        location=location,
    )
    with pytest.raises(InvalidSupplementaryDataSelector) as e:
        value_source_resolver.resolve(
            {
                "source": "supplementary_data",
                "identifier": "guidance",
                "selectors": ["invalid"],
            }
        )

    assert e.value.args[0] == "Cannot use the selector `invalid` on non-nested data"
