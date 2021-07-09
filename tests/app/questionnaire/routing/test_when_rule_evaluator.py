from datetime import datetime
from typing import Optional, Union
from unittest.mock import Mock

import pytest
from freezegun import freeze_time

from app.data_models import AnswerStore, ListStore
from app.data_models.answer import Answer
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.routing.operator import Operator
from app.questionnaire.routing.when_rule_evaluator import WhenRuleEvaluator
from tests.app.questionnaire.test_value_source_resolver import (
    answer_source,
    answer_source_dict_answer_selector,
    answer_source_list_item_selector_list_first_item,
    answer_source_list_item_selector_location,
    get_list_items,
    list_source,
    list_source_id_selector_first,
    list_source_id_selector_primary_person,
    list_source_id_selector_same_name_items,
    location_source,
    metadata_source,
)

now = datetime.utcnow()
now_as_yyyy_mm_dd = now.strftime("%Y-%m-%d")


def get_test_data_for_source(source: dict):
    """
    operator, operands, resolved_value, expected_result
    """
    return [
        (Operator.EQUAL, [source, "Maybe"], "Maybe", True),
        (Operator.EQUAL, ["Maybe", source], "Maybe", True),
        (Operator.NOT_EQUAL, [source, "Maybe"], "Yes", True),
        (Operator.NOT_EQUAL, ["Maybe", source], "Yes", True),
        (Operator.GREATER_THAN, [2, source], 1, True),
        (Operator.GREATER_THAN, [source, 1], 2, True),
        (Operator.GREATER_THAN_OR_EQUAL, [1, source], 1, True),
        (Operator.GREATER_THAN_OR_EQUAL, [source, 1], 1, True),
        (Operator.LESS_THAN, [1, source], 2, True),
        (Operator.LESS_THAN, [source, 2], 1, True),
        (Operator.LESS_THAN_OR_EQUAL, [1, source], 1, True),
        (Operator.LESS_THAN_OR_EQUAL, [source, 1], 1, True),
        (Operator.IN, [source, ["Maybe"]], "Maybe", True),
        (Operator.IN, ["Maybe", source], ["Maybe"], True),
        (Operator.ANY_IN, [source, ["Maybe"]], ["Yes", "Maybe"], True),
        (Operator.ANY_IN, [["Maybe"], source], ["Yes", "Maybe"], True),
        (Operator.ALL_IN, [source, ["Maybe"]], ["Maybe"], True),
        (Operator.ALL_IN, [["Maybe"], source], ["Maybe"], True),
        # Test inverse
        (Operator.EQUAL, [source, "Maybe"], "Yes", False),
        (Operator.EQUAL, ["Maybe", source], "Yes", False),
        (Operator.NOT_EQUAL, [source, "Maybe"], "Maybe", False),
        (Operator.NOT_EQUAL, ["Maybe", source], "Maybe", False),
        (Operator.GREATER_THAN, [1, source], 2, False),
        (Operator.GREATER_THAN, [source, 2], 1, False),
        (Operator.GREATER_THAN_OR_EQUAL, [1, source], 2, False),
        (Operator.GREATER_THAN_OR_EQUAL, [source, 1], 0, False),
        (Operator.LESS_THAN, [2, source], 1, False),
        (Operator.LESS_THAN, [source, 1], 2, False),
        (Operator.LESS_THAN_OR_EQUAL, [1, source], 0, False),
        (Operator.LESS_THAN_OR_EQUAL, [source, 1], 2, False),
        (Operator.IN, [source, ["Maybe"]], "Yes", False),
        (Operator.IN, ["Maybe", source], ["Yes"], False),
        (Operator.ANY_IN, [source, ["Maybe"]], ["Yes", "No"], False),
        (Operator.ANY_IN, [["Maybe"], source], ["Yes", "No"], False),
        (Operator.ALL_IN, [source, ["Maybe"]], ["Yes", "No"], False),
        (Operator.ALL_IN, [["Maybe"], source], ["Yes"], False),
    ]


def get_test_data_with_string_values_for_source(source: dict):
    """
    operator, operands, expected_result
    """
    return [
        (Operator.EQUAL, [source, "item-1"], True),
        (Operator.EQUAL, ["item-1", source], True),
        (Operator.NOT_EQUAL, [source, "item-2"], True),
        (Operator.NOT_EQUAL, ["item-2", source], True),
        (Operator.IN, [source, ["item-1"]], True),
        # Test inverse
        (Operator.EQUAL, [source, "item-2"], False),
        (Operator.EQUAL, ["item-2", source], False),
        (Operator.NOT_EQUAL, [source, "item-1"], False),
        (Operator.NOT_EQUAL, ["item-1", source], False),
        (Operator.IN, [source, ["item-2"]], False),
    ]


def get_test_data_comparison_operators_numeric_value_for_source(source):
    """
    operator, operands, resolved_value, expected_result
    """
    return [
        (Operator.EQUAL, [source, 1], 1, True),
        (Operator.EQUAL, [1, source], 1, True),
        (Operator.NOT_EQUAL, [source, 1], 2, True),
        (Operator.NOT_EQUAL, [1, source], 2, True),
        (Operator.GREATER_THAN, [2, source], 1, True),
        (Operator.GREATER_THAN, [source, 1], 2, True),
        (Operator.GREATER_THAN_OR_EQUAL, [1, source], 1, True),
        (Operator.GREATER_THAN_OR_EQUAL, [source, 1], 1, True),
        (Operator.LESS_THAN, [1, source], 2, True),
        (Operator.LESS_THAN, [source, 2], 1, True),
        (Operator.LESS_THAN_OR_EQUAL, [1, source], 1, True),
        (Operator.LESS_THAN_OR_EQUAL, [source, 1], 1, True),
        # Test inverse
        (Operator.EQUAL, [source, 1], 2, False),
        (Operator.EQUAL, [1, source], 2, False),
        (Operator.NOT_EQUAL, [source, 1], 1, False),
        (Operator.NOT_EQUAL, [1, source], 1, False),
        (Operator.GREATER_THAN, [1, source], 2, False),
        (Operator.GREATER_THAN, [source, 2], 1, False),
        (Operator.GREATER_THAN_OR_EQUAL, [1, source], 2, False),
        (Operator.GREATER_THAN_OR_EQUAL, [source, 1], 0, False),
        (Operator.LESS_THAN, [2, source], 1, False),
        (Operator.LESS_THAN, [source, 1], 2, False),
        (Operator.LESS_THAN_OR_EQUAL, [1, source], 0, False),
        (Operator.LESS_THAN_OR_EQUAL, [source, 1], 2, False),
    ]


def get_test_data_for_date_value_for_source(source):
    """
    rule, expected_result
    """
    return [
        (
            {
                Operator.EQUAL: [
                    {Operator.DATE: [source]},
                    {Operator.DATE: [now_as_yyyy_mm_dd]},
                ]
            },
            True,
        ),
        (
            {
                Operator.NOT_EQUAL: [
                    {Operator.DATE: [source, {"days": -1}]},
                    {Operator.DATE: [now_as_yyyy_mm_dd]},
                ]
            },
            True,
        ),
        (
            {
                Operator.LESS_THAN: [
                    {Operator.DATE: [source, {"days": -1}]},
                    {Operator.DATE: ["now"]},
                ]
            },
            True,
        ),
        (
            {
                Operator.LESS_THAN_OR_EQUAL: [
                    {Operator.DATE: [source, {"days": -1}]},
                    {Operator.DATE: ["now", {"days": -1}]},
                ]
            },
            True,
        ),
        (
            {
                Operator.GREATER_THAN: [
                    {Operator.DATE: [source]},
                    {Operator.DATE: ["now", {"months": -1}]},
                ]
            },
            True,
        ),
        (
            {
                Operator.GREATER_THAN_OR_EQUAL: [
                    {Operator.DATE: [source, {"months": -1}]},
                    {Operator.DATE: ["now", {"months": -1}]},
                ]
            },
            True,
        ),
        # Test inverse
        (
            {
                Operator.EQUAL: [
                    {Operator.DATE: [source, {"days": -1}]},
                    {Operator.DATE: [now_as_yyyy_mm_dd]},
                ]
            },
            False,
        ),
        (
            {
                Operator.NOT_EQUAL: [
                    {Operator.DATE: [source]},
                    {Operator.DATE: [now_as_yyyy_mm_dd]},
                ]
            },
            False,
        ),
        (
            {
                Operator.LESS_THAN: [
                    {Operator.DATE: [source, {"days": 1}]},
                    {Operator.DATE: ["now"]},
                ]
            },
            False,
        ),
        (
            {
                Operator.GREATER_THAN: [
                    {Operator.DATE: [source, {"months": -1}]},
                    {Operator.DATE: ["now"]},
                ]
            },
            False,
        ),
        (
            {
                Operator.EQUAL: [
                    {Operator.DATE: [source]},
                    {Operator.DATE: [None]},
                ]
            },
            False,
        ),
    ]


test_data_mixed_value_sources = (
    # operator, operands
    {Operator.EQUAL: [{"source": "answers", "identifier": "answer-1"}, "Yes, I do"]},
    {Operator.NOT_EQUAL: [{"source": "list", "identifier": "some-list"}, 0]},
    {
        Operator.GREATER_THAN_OR_EQUAL: [
            {
                "source": "answers",
                "identifier": "answer-2",
                "list_item_selector": {
                    "source": "location",
                    "id": "list_item_id",
                },
            },
            9,
        ]
    },
    {
        Operator.IN: [
            {"source": "metadata", "identifier": "region_code"},
            ["GB-ENG", "GB-WLS"],
        ]
    },
    {Operator.EQUAL: [list_source_id_selector_first, location_source]},
    {Operator.ANY_IN: [list_source_id_selector_same_name_items, ["item-1"]]},
)


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


def get_when_rule_evaluator(
    rule: dict,
    schema: QuestionnaireSchema = None,
    answer_store: AnswerStore = AnswerStore(),
    list_store: ListStore = ListStore(),
    metadata: Optional[dict] = None,
    location: Union[Location, RelationshipLocation] = Location(
        section_id="test-section", block_id="test-block"
    ),
    routing_path_block_ids: Optional[list] = None,
):
    if not schema:
        schema = get_mock_schema()
        schema.answer_should_have_list_item_id = Mock(return_value=True)
        schema.get_default_answer = Mock(return_value=None)

    return WhenRuleEvaluator(
        rule=rule,
        schema=schema,
        metadata=metadata or {},
        answer_store=answer_store,
        list_store=list_store,
        location=location,
        routing_path_block_ids=routing_path_block_ids,
    )


@pytest.mark.parametrize(
    "operator, operands, answer_value, expected_result",
    get_test_data_for_source(answer_source),
)
def test_answer_source(operator, operands, answer_value, expected_result):
    when_rule_evaluator = get_when_rule_evaluator(
        rule={operator: operands},
        answer_store=AnswerStore([{"answer_id": "some-answer", "value": answer_value}]),
    )

    assert when_rule_evaluator.evaluate() is expected_result


@pytest.mark.parametrize(
    "operator, operands, answer_value, expected_result",
    get_test_data_for_source(answer_source_list_item_selector_location),
)
def test_answer_source_with_list_item_selector_location(
    operator, operands, answer_value, expected_result
):
    when_rule_evaluator = get_when_rule_evaluator(
        rule={operator: operands},
        answer_store=AnswerStore(
            [
                {
                    "answer_id": "some-answer",
                    "list_item_id": "item-1",
                    "value": answer_value,
                }
            ]
        ),
        location=Location(
            section_id="some-section", block_id="some-block", list_item_id="item-1"
        ),
    )

    assert when_rule_evaluator.evaluate() is expected_result


@pytest.mark.parametrize(
    "operator, operands, answer_value, expected_result",
    get_test_data_for_source(answer_source_list_item_selector_list_first_item),
)
def test_answer_source_with_list_item_selector_list_first_item(
    operator, operands, answer_value, expected_result
):
    when_rule_evaluator = get_when_rule_evaluator(
        rule={operator: operands},
        answer_store=AnswerStore(
            [
                {
                    "answer_id": "some-answer",
                    "list_item_id": "item-1",
                    "value": answer_value,
                }
            ]
        ),
        list_store=ListStore([{"name": "some-list", "items": get_list_items(3)}]),
    )

    assert when_rule_evaluator.evaluate() is expected_result


@pytest.mark.parametrize(
    "operator, operands, answer_value, expected_result",
    get_test_data_comparison_operators_numeric_value_for_source(
        answer_source_dict_answer_selector
    ),
)
def test_answer_source_with_dict_answer_selector(
    operator, operands, answer_value, expected_result
):
    when_rule_evaluator = get_when_rule_evaluator(
        rule={operator: operands},
        answer_store=AnswerStore(
            [
                {
                    "answer_id": "some-answer",
                    "value": {"years": answer_value, "months": 10},
                }
            ]
        ),
    )

    assert when_rule_evaluator.evaluate() is expected_result


@pytest.mark.parametrize(
    "operator, operands, metadata_value, expected_result",
    get_test_data_for_source(metadata_source),
)
def test_metadata_source(operator, operands, metadata_value, expected_result):
    when_rule_evaluator = get_when_rule_evaluator(
        rule={operator: operands},
        metadata={"some-metadata": metadata_value},
    )

    assert when_rule_evaluator.evaluate() is expected_result


@pytest.mark.parametrize(
    "operator, operands, list_count, expected_result",
    get_test_data_comparison_operators_numeric_value_for_source(list_source),
)
def test_list_source(operator, operands, list_count, expected_result):
    when_rule_evaluator = get_when_rule_evaluator(
        rule={operator: operands},
        list_store=ListStore(
            [{"name": "some-list", "items": get_list_items(list_count)}]
        ),
    )

    assert when_rule_evaluator.evaluate() is expected_result


@pytest.mark.parametrize(
    "operator, operands, expected_result",
    get_test_data_with_string_values_for_source(list_source_id_selector_first),
)
def test_list_source_with_id_selector_first(operator, operands, expected_result):
    when_rule_evaluator = get_when_rule_evaluator(
        rule={operator: operands},
        list_store=ListStore([{"name": "some-list", "items": get_list_items(1)}]),
    )

    assert when_rule_evaluator.evaluate() is expected_result


@pytest.mark.parametrize(
    "operator, operands, expected_result",
    [
        (Operator.IN, ["item-2", list_source_id_selector_same_name_items], True),
        (
            Operator.ANY_IN,
            [list_source_id_selector_same_name_items, ["item-3", "item-5"]],
            True,
        ),
        (Operator.ANY_IN, [["item-1"], list_source_id_selector_same_name_items], True),
        (
            Operator.ALL_IN,
            [list_source_id_selector_same_name_items, ["item-1", "item-2", "item-3"]],
            True,
        ),
        (
            Operator.ALL_IN,
            [["item-1", "item-2", "item-3"], list_source_id_selector_same_name_items],
            True,
        ),
        # Test inverse
        (Operator.IN, ["item-5", list_source_id_selector_same_name_items], False),
        (
            Operator.ANY_IN,
            [list_source_id_selector_same_name_items, ["item-4", "item-5"]],
            False,
        ),
        (Operator.ANY_IN, [["item-5"], list_source_id_selector_same_name_items], False),
        (
            Operator.ALL_IN,
            [list_source_id_selector_same_name_items, ["item-1", "item-2", "item-5"]],
            False,
        ),
        (
            Operator.ALL_IN,
            [["item-1", "item-2", "item-5"], list_source_id_selector_same_name_items],
            False,
        ),
    ],
)
def test_list_source_with_id_selector_same_name_items(
    operator, operands, expected_result
):
    when_rule_evaluator = get_when_rule_evaluator(
        rule={operator: operands},
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

    assert when_rule_evaluator.evaluate() is expected_result


@pytest.mark.parametrize(
    "primary_person_list_item_id, expected_result",
    [("item-1", True), ("item-2", False)],
)
def test_list_source_id_selector_primary_person(
    primary_person_list_item_id, expected_result
):
    location = RelationshipLocation(
        section_id="some-section",
        block_id="some-block",
        list_item_id="item-1",
        to_list_item_id="item-2",
        list_name="household",
    )

    when_rule_evaluator = get_when_rule_evaluator(
        rule={
            Operator.EQUAL: [
                list_source_id_selector_primary_person,
                location_source,
            ]
        },
        list_store=ListStore(
            [
                {
                    "name": "some-list",
                    "primary_person": primary_person_list_item_id,
                    "items": get_list_items(3),
                }
            ]
        ),
        location=location,
    )

    assert when_rule_evaluator.evaluate() is expected_result


@pytest.mark.parametrize(
    "operator, operands, expected_result",
    get_test_data_with_string_values_for_source(location_source),
)
def test_current_location_source(operator, operands, expected_result):
    when_rule_evaluator = get_when_rule_evaluator(
        rule={operator: operands},
        location=Location(
            section_id="some-section", block_id="some-block", list_item_id="item-1"
        ),
    )

    assert when_rule_evaluator.evaluate() is expected_result


@pytest.mark.parametrize(
    "operator, operands, expected_result",
    [
        (
            Operator.AND,
            [
                *test_data_mixed_value_sources,
                {
                    Operator.ANY_IN: [
                        list_source_id_selector_same_name_items,
                        ["item-1"],
                    ]
                },
            ],
            True,
        ),
        # Test inverse
        (
            Operator.AND,
            [
                *test_data_mixed_value_sources,
                {
                    Operator.ANY_IN: [
                        list_source_id_selector_same_name_items,
                        ["item-5"],
                    ]
                },
            ],
            False,
        ),
        (
            Operator.OR,
            [
                *test_data_mixed_value_sources,
                {
                    Operator.ALL_IN: [
                        list_source_id_selector_same_name_items,
                        ["item-1"],
                    ]
                },
            ],
            True,
        ),
        # Test inverse
        (
            Operator.OR,
            [
                {
                    Operator.EQUAL: [
                        {"source": "answers", "identifier": "answer-1"},
                        "No",
                    ]
                },
                {
                    Operator.NOT_EQUAL: [
                        {"source": "list", "identifier": "some-list"},
                        5,
                    ]
                },
                {
                    Operator.GREATER_THAN_OR_EQUAL: [
                        {
                            "source": "answers",
                            "identifier": "answer-2",
                            "list_item_selector": {
                                "source": "location",
                                "id": "list_item_id",
                            },
                        },
                        15,
                    ]
                },
                {
                    Operator.IN: [
                        {"source": "metadata", "identifier": "region_code"},
                        ["GB-NIR"],
                    ]
                },
                {
                    Operator.NOT_EQUAL: [
                        list_source_id_selector_first,
                        location_source,
                    ]
                },
                {
                    Operator.ANY_IN: [
                        list_source_id_selector_same_name_items,
                        ["item-5"],
                    ]
                },
            ],
            False,
        ),
    ],
)
def test_logic_and_or(operator, operands, expected_result):
    when_rule_evaluator = get_when_rule_evaluator(
        rule={operator: operands},
        answer_store=AnswerStore(
            [
                {
                    "answer_id": "answer-1",
                    "list_item_id": "item-1",
                    "value": "Yes, I do",
                },
                {
                    "answer_id": "answer-2",
                    "list_item_id": "item-1",
                    "value": 10,
                },
            ]
        ),
        metadata={"region_code": "GB-ENG", "language_code": "en"},
        list_store=ListStore(
            [
                {
                    "name": "some-list",
                    "items": get_list_items(5),
                    "same_name_items": get_list_items(3),
                }
            ],
        ),
        location=Location(
            section_id="some-section", block_id="some-block", list_item_id="item-1"
        ),
    )

    assert when_rule_evaluator.evaluate() is expected_result


@pytest.mark.parametrize(
    "operator, operands, answer_value, expected_result",
    get_test_data_for_source(answer_source),
)
def test_logic_not(operator, operands, answer_value, expected_result):
    when_rule_evaluator = get_when_rule_evaluator(
        rule={Operator.NOT: [{operator: operands}]},
        answer_store=AnswerStore([{"answer_id": "some-answer", "value": answer_value}]),
    )

    assert when_rule_evaluator.evaluate() is not expected_result


@pytest.mark.parametrize(
    "operator, operands, expected_result",
    [
        (
            Operator.AND,
            [
                {
                    Operator.EQUAL: [
                        {"source": "answers", "identifier": "answer-1"},
                        "Yes, I do",
                    ]
                },
                {
                    Operator.GREATER_THAN_OR_EQUAL: [
                        {
                            "source": "answers",
                            "identifier": "answer-2",
                            "list_item_selector": {
                                "source": "location",
                                "id": "list_item_id",
                            },
                        },
                        9,
                    ]
                },
                {
                    Operator.OR: [
                        {Operator.EQUAL: [list_source, 0]},
                        {
                            Operator.AND: [
                                {
                                    Operator.NOT: [
                                        {
                                            Operator.IN: [
                                                {
                                                    "source": "metadata",
                                                    "identifier": "region_code",
                                                },
                                                ["GB-ENG", "GB-WLS"],
                                            ]
                                        }
                                    ]
                                },
                                {
                                    Operator.IN: [
                                        list_source_id_selector_first,
                                        list_source_id_selector_same_name_items,
                                    ]
                                },
                            ]
                        },
                    ]
                },
            ],
            True,
        ),
        (
            Operator.OR,
            [
                {
                    Operator.NOT_EQUAL: [
                        {"source": "answers", "identifier": "answer-1"},
                        "Yes, I do",
                    ]
                },
                {
                    Operator.OR: [
                        {Operator.EQUAL: [list_source, 0]},
                        {
                            Operator.AND: [
                                {
                                    Operator.NOT: [
                                        {
                                            Operator.IN: [
                                                {
                                                    "source": "metadata",
                                                    "identifier": "region_code",
                                                },
                                                ["GB-ENG", "GB-WLS"],
                                            ]
                                        }
                                    ]
                                },
                                {
                                    Operator.IN: [
                                        list_source_id_selector_first,
                                        list_source_id_selector_same_name_items,
                                    ]
                                },
                            ]
                        },
                    ]
                },
            ],
            True,
        ),
    ],
)
def test_nested_rules(operator, operands, expected_result):
    when_rule_evaluator = get_when_rule_evaluator(
        rule={operator: operands},
        answer_store=AnswerStore(
            [
                {
                    "answer_id": "answer-1",
                    "list_item_id": "item-1",
                    "value": "Yes, I do",
                },
                {
                    "answer_id": "answer-2",
                    "list_item_id": "item-1",
                    "value": 10,
                },
            ]
        ),
        metadata={"region_code": "GB-NIR", "language_code": "en"},
        list_store=ListStore(
            [
                {
                    "name": "some-list",
                    "items": get_list_items(5),
                    "same_name_items": get_list_items(3),
                }
            ],
        ),
        location=Location(
            section_id="some-section", block_id="some-block", list_item_id="item-1"
        ),
    )

    assert when_rule_evaluator.evaluate() is expected_result


@pytest.mark.parametrize(
    "operands",
    [
        [None, 10],
        [10, None],
        [None, None],
        # Value for value sources does not exist
        [10, answer_source],
        [10, metadata_source],
    ],
)
@pytest.mark.parametrize(
    "operator_name",
    [
        Operator.GREATER_THAN,
        Operator.GREATER_THAN_OR_EQUAL,
        Operator.LESS_THAN,
        Operator.LESS_THAN_OR_EQUAL,
    ],
)
def test_comparison_operator_rule_with_nonetype_operands(operator_name, operands):
    when_rule_evaluator = get_when_rule_evaluator(
        rule={operator_name: operands},
    )
    assert when_rule_evaluator.evaluate() is False


@pytest.mark.parametrize(
    "operands",
    [
        [None, ["Yes"]],
        [["Yes"], None],
        [None, None],
        # Value for value sources does not exist
        [["Yes"], answer_source],
        [["Yes"], metadata_source],
    ],
)
@pytest.mark.parametrize(
    "operator_name", [Operator.ALL_IN, Operator.ANY_IN, Operator.IN]
)
def test_array_operator_rule_with_nonetype_operands(operator_name, operands):
    when_rule_evaluator = get_when_rule_evaluator(
        rule={operator_name: operands},
    )
    assert when_rule_evaluator.evaluate() is False


@freeze_time(now)
@pytest.mark.parametrize(
    "rule, expected_result",
    [
        *get_test_data_for_date_value_for_source(answer_source),
        *get_test_data_for_date_value_for_source(metadata_source),
    ],
)
def test_date_value(rule, expected_result):
    when_rule_evaluator = get_when_rule_evaluator(
        rule=rule,
        answer_store=AnswerStore(
            [
                {
                    "answer_id": "some-answer",
                    "value": now_as_yyyy_mm_dd,
                }
            ]
        ),
        metadata={"some-metadata": now_as_yyyy_mm_dd},
    )

    assert when_rule_evaluator.evaluate() is expected_result


@pytest.mark.parametrize(
    "answer_should_have_list_item_id, list_item_id_for_answer, expected_result",
    [
        (True, None, False),
        (True, "item-2", False),
        (True, "item-1", True),
        (False, None, True),
        (False, "item-2", False),
        (False, "item-1", False),
    ],
)
def test_rule_uses_list_item_id_when_evaluating_answer_value(
    answer_should_have_list_item_id, list_item_id_for_answer, expected_result
):
    schema = get_mock_schema()

    # We are fetching an answer that is outside of a repeat or one not in a list collector.
    schema.answer_should_have_list_item_id = Mock(
        return_value=answer_should_have_list_item_id
    )

    when_rule_evaluator = get_when_rule_evaluator(
        rule={Operator.EQUAL: [answer_source, "Yes"]},
        schema=schema,
        answer_store=AnswerStore(
            [
                {
                    "answer_id": "some-answer",
                    "list_item_id": list_item_id_for_answer,
                    "value": "Yes",
                }
            ]
        ),
        location=Location(
            section_id="some-section", block_id="some-block", list_item_id="item-1"
        ),
    )

    assert when_rule_evaluator.evaluate() is expected_result


@pytest.mark.parametrize("is_answer_on_path", [True, False])
@pytest.mark.parametrize("is_inside_repeat", [True, False])
def test_answer_with_routing_path_block_ids(is_answer_on_path, is_inside_repeat):
    schema = get_mock_schema()
    schema.get_block_for_answer_id = Mock(return_value={"id": f"some-block"})

    location = Location(section_id="test-section", block_id="test-block")
    id_prefix = "some" if is_answer_on_path else "some-other"
    answer = Answer(answer_id=f"{id_prefix}-answer", value="Yes")

    if is_inside_repeat:
        location.list_item_id = answer.list_item_id = "item-1"
        schema.answer_should_have_list_item_id = Mock(return_value=True)
    else:
        schema.answer_should_have_list_item_id = Mock(return_value=False)

    when_rule_evaluator = get_when_rule_evaluator(
        rule={Operator.EQUAL: ["Yes", answer_source]},
        schema=schema,
        answer_store=AnswerStore([answer.to_dict()]),
        location=location,
        routing_path_block_ids=[f"{id_prefix}-block"],
    )

    expected_result = True if is_answer_on_path else False
    assert when_rule_evaluator.evaluate() is expected_result


@pytest.mark.parametrize(
    "operator, operands, answer_value, expected_result",
    get_test_data_for_source(answer_source),
)
def test_answer_source_default_answer_used_when_no_answer(
    operator, operands, answer_value, expected_result
):
    schema = get_mock_schema()
    schema.get_default_answer = Mock(
        return_value=Answer(answer_id="some-answer", value=answer_value)
    )

    when_rule_evaluator = get_when_rule_evaluator(
        rule={operator: operands},
        schema=schema,
        answer_store=AnswerStore([{"answer_id": f"some-other-answer", "value": "No"}]),
    )

    assert when_rule_evaluator.evaluate() is expected_result


def test_raises_exception_when_bad_operands():
    with pytest.raises(TypeError):
        when_rule_evaluator = get_when_rule_evaluator(
            rule={Operator.EQUAL: {1, 1}},
            answer_store=AnswerStore(
                [{"answer_id": f"some-other-answer", "value": "No"}]
            ),
        )

        when_rule_evaluator.evaluate()
