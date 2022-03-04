# pylint: disable=too-many-lines
import pytest

from app.data_models.answer_store import Answer
from app.data_models.list_store import ListStore
from app.questionnaire.location import Location
from app.questionnaire.path_finder import PathFinder
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.routing_path import RoutingPath
from app.questionnaire.when_rules import (
    evaluate_goto,
    evaluate_rule,
    evaluate_when_rules,
)


@pytest.mark.parametrize(
    "when_rule,answers,expected",
    (
        ({"value": "singleAnswer", "condition": "contains"}, ["singleAnswer"], True),
        (
            {"value": "firstAnswer", "condition": "equals"},
            ["firstAnswer", "secondAnswer"],
            False,
        ),
        ({"value": False, "condition": "equals"}, False, True),
        ({"value": True, "condition": "not equals"}, False, True),
        ({"condition": "set"}, "", True),
        ({"condition": "set"}, "0", True),
        ({"condition": "set"}, "Yes", True),
        ({"condition": "set"}, "No", True),
        ({"condition": "set"}, 0, True),
        ({"condition": "set"}, 1, True),
        ({"condition": "set"}, None, False),
        ({"condition": "not set"}, None, True),
        ({"condition": "not set"}, "", False),
        ({"condition": "not set"}, "some text", False),
        ({"condition": "not set"}, [], True),
        ({"condition": "not set"}, ["123"], False),
        ({"condition": "set"}, ["123"], True),
        ({"condition": "set"}, [], False),
        ({"value": 0, "condition": "equals"}, 2, False),
        ({"value": 0, "condition": "equals"}, 0, True),
        ({"value": "answervalue", "condition": "equals"}, "answerValue", True),
        ({"value": "answervalue", "condition": "equals"}, "answervalue", True),
        ({"value": "answervalue", "condition": "equals"}, "answer-value", False),
        ({"value": "answervalue", "condition": "not equals"}, "answerValue", False),
        ({"value": "answervalue", "condition": "not equals"}, "answervalue", False),
        ({"value": "answervalue", "condition": "not equals"}, "answer-value", True),
        (
            {"value": ["answerValue", "notAnswerValue"], "condition": "equals any"},
            "answerValue",
            True,
        ),
        (
            {"value": ["answerValue", "notAnswerValue"], "condition": "equals any"},
            "answervalue",
            True,
        ),
        (
            {"value": ["answerValue", "notAnswerValue"], "condition": "equals any"},
            "answer-value",
            False,
        ),
        (
            {"value": ["answerValue", "notAnswerValue"], "condition": "not equals any"},
            "answerValue",
            False,
        ),
        (
            {"value": ["answerValue", "notAnswerValue"], "condition": "not equals any"},
            "answervalue",
            False,
        ),
        (
            {"value": ["answerValue", "notAnswerValue"], "condition": "not equals any"},
            "answer-value",
            True,
        ),
        ({"value": 0, "condition": "not equals"}, 2, True),
        ({"value": 0, "condition": "not equals"}, 0, False),
        ({"value": 4, "condition": "greater than or equal to"}, 4, True),
        ({"value": 4, "condition": "greater than or equal to"}, 5, True),
        ({"value": 4, "condition": "greater than or equal to"}, 3, False),
        ({"value": 4, "condition": "greater than or equal to"}, None, False),
        ({"value": 4, "condition": "less than or equal to"}, 4, True),
        ({"value": 4, "condition": "less than or equal to"}, 3, True),
        ({"value": 4, "condition": "less than or equal to"}, 5, False),
        ({"value": 4, "condition": "less than or equal to"}, None, False),
        ({"value": 5, "condition": "greater than"}, 7, True),
        ({"value": 5, "condition": "greater than"}, 5, False),
        ({"value": 5, "condition": "greater than"}, 3, False),
        ({"value": 5, "condition": "less than"}, 3, True),
        ({"value": 5, "condition": "less than"}, 5, False),
        ({"value": 5, "condition": "less than"}, 7, False),
    ),
)
def test_evaluate_rule(when_rule, answers, expected):
    assert evaluate_rule(when_rule, answers) is expected


@pytest.mark.parametrize(
    "goto,answers,metadata,expected",
    (
        (
            {
                "id": "next-question",
                "when": [{"id": "my_answer", "condition": "equals", "value": "Yes"}],
            },
            [{"answer_id": "my_answer", "value": "Yes"}],
            None,
            True,
        ),
        (
            {
                "id": "next-question",
                "when": [{"id": "my_answer", "condition": "equals", "value": "Yes"}],
            },
            [{"answer_id": "my_answer", "value": "No"}],
            None,
            False,
        ),
        (
            {
                "id": "next-question",
                "when": [
                    {"id": "my_answers", "condition": "contains", "value": "answer1"}
                ],
            },
            [{"answer_id": "my_answer", "value": "No"}],
            None,
            False,
        ),
        (
            {
                "id": "next-question",
                "when": [
                    {
                        "id": "my_answers",
                        "condition": "not contains",
                        "value": "answer1",
                    }
                ],
            },
            [{"answer_id": "my_answer", "value": "No"}],
            None,
            False,
        ),
        (
            {
                "id": "next-question",
                "when": [
                    {"id": "my_answers", "condition": "contains", "value": "answer1"}
                ],
            },
            [{"answer_id": "my_answers", "value": ["answer1", "answer2", "answer3"]}],
            None,
            True,
        ),
        (
            {
                "id": "next-question",
                "when": [
                    {
                        "id": "my_answers",
                        "condition": "not contains",
                        "value": "answer1",
                    }
                ],
            },
            [{"answer_id": "my_answers", "value": ["answer2", "answer3"]}],
            None,
            True,
        ),
        (
            {
                "id": "next-question",
                "when": [
                    {
                        "id": "my_answers",
                        "condition": "contains any",
                        "value": ["answer1", "answer2"],
                    }
                ],
            },
            [{"answer_id": "my_answers", "value": ["answer1", "answer4"]}],
            None,
            True,
        ),
        (
            {
                "id": "next-question",
                "when": [
                    {
                        "id": "my_answers",
                        "condition": "contains all",
                        "value": ["answer1", "answer2"],
                    }
                ],
            },
            [{"answer_id": "my_answers", "value": ["answer1", "answer2", "answer3"]}],
            None,
            True,
        ),
        (
            {
                "id": "next-question",
                "when": [
                    {
                        "id": "my_answers",
                        "condition": "equals any",
                        "values": ["answer1", "answer2"],
                    }
                ],
            },
            [{"answer_id": "my_answers", "value": "answer2"}],
            None,
            True,
        ),
        (
            {
                "id": "next-question",
                "when": [
                    {
                        "id": "my_answers",
                        "condition": "not equals any",
                        "values": ["answer1", "answer2"],
                    }
                ],
            },
            [{"answer_id": "my_answers", "value": "answer3"}],
            None,
            True,
        ),
        (
            {
                "id": "next-question",
                "when": [
                    {
                        "id": "my_answers",
                        "condition": "not equals any",
                        "values": ["answer1", "answer2"],
                    }
                ],
            },
            [
                {"answer_id": "my_answer", "value": "Yes"},
                {"answer_id": "my_other_answer", "value": "2"},
            ],
            None,
            True,
        ),
        (
            {
                "id": "next-question",
                "when": [
                    {"id": "my_answer", "condition": "equals", "value": "Yes"},
                    {"id": "my_other_answer", "condition": "equals", "value": "2"},
                ],
            },
            [
                {"answer_id": "my_answer", "value": "No"},
            ],
            None,
            False,
        ),
        (
            {
                "id": "next-question",
                "when": [
                    {"id": "my_answer", "condition": "equals", "value": "Yes"},
                    {"condition": "equals", "meta": "sexual_identity", "value": True},
                ],
            },
            [
                {"answer_id": "my_answer", "value": "Yes"},
            ],
            {"sexual_identity": True},
            True,
        ),
        (
            {
                "id": "next-question",
                "when": [
                    {"id": "my_answer", "condition": "equals", "value": "Yes"},
                    {"condition": "equals", "meta": "sexual_identity", "value": False},
                ],
            },
            [
                {"answer_id": "my_answer", "value": "Yes"},
            ],
            {"varient_flags": {"sexual_identity": True}},
            False,
        ),
        (
            {
                "id": "next-question",
                "when": [
                    {
                        "condition": "equals",
                        "meta": "variant_flags.does_not_exist.does_not_exist",
                        "value": True,
                    }
                ],
            },
            [
                {"answer_id": "my_answer", "value": "Yes"},
            ],
            {"sexual_identity": True},
            False,
        ),
    ),
)
def test_go_to(
    goto,
    answers,
    metadata,
    expected,
    answer_store,
    list_store,
    current_location,
    questionnaire_schema,
):
    for answer in answers:
        answer_store.add_or_update(Answer(**answer))

    assert (
        evaluate_goto(
            goto_rule=goto,
            schema=questionnaire_schema,
            metadata=metadata or {},
            answer_store=answer_store,
            list_store=list_store,
            current_location=current_location,
        )
        is expected
    )


@pytest.mark.parametrize(
    "skip_conditions,answers,expected",
    (
        (
            [
                {"when": [{"id": "this", "condition": "equals", "value": "value"}]},
                {
                    "when": [
                        {"id": "that", "condition": "equals", "value": "other value"}
                    ]
                },
            ],
            [{"answer_id": "this", "value": "value"}],
            True,
        ),
        (
            [
                {"when": [{"id": "this", "condition": "equals", "value": "value"}]},
                {
                    "when": [
                        {"id": "that", "condition": "equals", "value": "other value"}
                    ]
                },
            ],
            [{"answer_id": "that", "value": "other value"}],
            True,
        ),
        (
            [
                {"when": [{"id": "this", "condition": "equals", "value": "value"}]},
                {
                    "when": [
                        {"id": "that", "condition": "equals", "value": "other value"}
                    ]
                },
            ],
            [
                {"answer_id": "that", "value": "other value"},
                {"answer_id": "this", "value": "value"},
            ],
            True,
        ),
        (
            [
                {"when": [{"id": "this", "condition": "equals", "value": "value"}]},
                {
                    "when": [
                        {"id": "that", "condition": "equals", "value": "other value"}
                    ]
                },
            ],
            [
                {"answer_id": "that", "value": "not correct"},
                {"answer_id": "this", "value": "not correct"},
            ],
            False,
        ),
        (
            None,
            [],
            False,
        ),
    ),
)
def test_skip_conditions(
    skip_conditions,
    answers,
    expected,
    answer_store,
    list_store,
    current_location,
    questionnaire_schema,
    progress_store,
):
    for answer in answers:
        answer_store.add_or_update(Answer(**answer))

    path_finder = PathFinder(
        questionnaire_schema,
        answer_store,
        list_store=list_store,
        metadata={},
        progress_store=progress_store,
        response_metadata={},
    )

    routing_path_block_ids = []

    condition = path_finder.evaluate_skip_conditions(
        current_location, routing_path_block_ids, skip_conditions
    )

    assert condition is expected


@pytest.mark.parametrize(
    "when_rules,answers,expected",
    (([{"id": "my_answers", "condition": "not set"}], {}, True),),
)
def test_evaluate_not_set_when_rules_should_return_true(
    when_rules,
    answers,
    expected,
    answer_store,
    list_store,
    current_location,
    questionnaire_schema,
):
    for answer in answers.values():
        answer_store.add_or_update(answer)

    assert (
        evaluate_when_rules(
            when_rules=when_rules,
            schema=questionnaire_schema,
            metadata={},
            answer_store=answer_store,
            list_store=list_store,
            current_location=current_location,
        )
        is expected
    )


@pytest.mark.parametrize(
    "lhs_answer,comparison,rhs_answer,expected",
    (
        ("medium", "equals", "medium", True),
        ("medium", "equals", "low", False),
        ("medium", "greater than", "low", True),
        ("medium", "greater than", "high", False),
        ("medium", "less than", "high", True),
        ("medium", "less than", "low", False),
        ("medium", "equals", "missing_answer", False),
        ("list_answer", "contains", "text_answer", True),
        ("list_answer", "contains", "other_text_answer", False),
        ("list_answer", "not contains", "other_text_answer", True),
        ("list_answer", "not contains", "text_answer", False),
        ("list_answer", "contains any", "other_list_answer_2", True),
        ("list_answer", "contains any", "other_list_answer", False),
        ("list_answer", "contains all", "other_list_answer", False),
        ("list_answer", "contains all", "other_list_answer_2", True),
        ("text_answer", "equals any", "list_answer", True),
        ("text_answer", "equals any", "other_list_answer", False),
        ("text_answer", "not equals any", "other_list_answer", True),
        ("text_answer", "not equals any", "list_answer", False),
    ),
)
def test_when_rule_comparing_answer_values(
    lhs_answer,
    comparison,
    rhs_answer,
    expected,
    answers,
    answer_store,
    list_store,
    questionnaire_schema,
    current_location,
):

    for answer in answers.values():
        answer_store.add_or_update(answer)

    when = [
        {
            "id": answers[lhs_answer].answer_id,
            "condition": comparison,
            "comparison": {"id": answers[rhs_answer].answer_id, "source": "answers"},
        }
    ]

    assert (
        evaluate_when_rules(
            when_rules=when,
            schema=questionnaire_schema,
            metadata={},
            answer_store=answer_store,
            list_store=list_store,
            current_location=current_location,
            routing_path_block_ids=None,
        )
        is expected
    )


@pytest.mark.parametrize(
    "list_item_id,expected",
    (
        ("abc123", True),
        ("123abc", False),
    ),
)
def test_evaluate_when_rule_with_list_item_id(
    list_item_id,
    expected,
    answer_store,
    list_store,
    questionnaire_schema,
    mocker,
):
    when_rules = [{"id": "my_answer", "condition": "equals", "value": "an answer"}]

    answer_store.add_or_update(
        Answer(answer_id="my_answer", value="an answer", list_item_id="abc123")
    )

    current_location = Location(
        section_id="some-section", block_id="some-block", list_item_id=list_item_id
    )

    schema = mocker.Mock(questionnaire_schema)
    schema.is_repeating_answer = mocker.Mock(return_value=True)

    assert (
        evaluate_when_rules(
            when_rules=when_rules,
            schema=schema,
            metadata={},
            answer_store=answer_store,
            list_store=list_store,
            current_location=current_location,
        )
        is expected
    )


def test_evaluate_when_rule_raises_if_bad_when_condition(
    answer_store, list_store, questionnaire_schema, current_location
):
    when_rules = [{"condition": "not set"}]
    with pytest.raises(Exception):
        evaluate_when_rules(
            when_rules=when_rules,
            schema=questionnaire_schema,
            metadata={},
            answer_store=answer_store,
            list_store=list_store,
            current_location=current_location,
        )


@pytest.mark.parametrize(
    "when_rules,expected",
    (
        ([{"list": "people", "condition": "less than", "value": 2}], True),
        ([{"list": "people", "condition": "equals", "value": 1}], True),
    ),
)
def test_evaluate_when_rule_with_list_rules(
    when_rules,
    expected,
    answer_store,
    questionnaire_schema,
    current_location,
):
    list_store = ListStore(existing_items=[{"name": "people", "items": ["abcdef"]}])

    assert (
        evaluate_when_rules(
            when_rules=when_rules,
            schema=questionnaire_schema,
            metadata={},
            answer_store=answer_store,
            list_store=list_store,
            current_location=current_location,
        )
        is expected
    )


@pytest.mark.parametrize(
    "routing_path,is_on_answer_path,expected",
    (
        (
            RoutingPath(
                ["test_block_id", "some-block"],
                section_id="some-section",
                list_name="people",
                list_item_id="abc123",
            ),
            True,
            True,
        ),
        (
            [
                Location(
                    section_id="some-section",
                    block_id="test_block_id",
                    list_name="people",
                    list_item_id="abc123",
                )
            ],
            False,
            False,
        ),
    ),
)
def test_routing_answer_on_path_when_in_a_repeat(
    routing_path,
    is_on_answer_path,
    expected,
    answer_store,
    list_store,
    questionnaire_schema,
    mocker,
):
    when_rules = [{"id": "some-answer", "condition": "equals", "value": "some value"}]

    answer = Answer(answer_id="some-answer", value="some value")
    answer_store.add_or_update(answer)

    routing_path = RoutingPath(
        ["test_block_id", "some-block"],
        section_id="some-section",
        list_name="people",
        list_item_id="abc123",
    )

    current_location = Location(
        section_id="some-section",
        block_id="some-block",
        list_name="people",
        list_item_id="abc123",
    )

    with mocker.patch(
        "app.questionnaire.when_rules.get_answer_for_answer_id", return_value=answer
    ), mocker.patch(
        "app.questionnaire.when_rules._is_answer_on_path",
        return_value=is_on_answer_path,
    ):
        assert (
            evaluate_when_rules(
                when_rules=when_rules,
                schema=questionnaire_schema,
                metadata={},
                answer_store=answer_store,
                list_store=list_store,
                current_location=current_location,
                routing_path_block_ids=routing_path,
            )
            is expected
        )


def test_routing_ignores_answers_not_on_path(
    answer_store, list_store, current_location, questionnaire_schema, mocker
):
    when_rules = [{"id": "some-answer", "condition": "equals", "value": "some value"}]
    answer_store.add_or_update(Answer(answer_id="some-answer", value="some value"))

    routing_path = [Location(section_id="some-section", block_id="test_block_id")]

    assert evaluate_when_rules(
        when_rules=when_rules,
        schema=questionnaire_schema,
        metadata={},
        answer_store=answer_store,
        list_store=list_store,
        current_location=current_location,
    )

    with mocker.patch(
        "app.questionnaire.when_rules._is_answer_on_path", return_value=False
    ):
        assert not (
            evaluate_when_rules(
                when_rules=when_rules,
                schema=questionnaire_schema,
                metadata={},
                answer_store=answer_store,
                list_store=list_store,
                current_location=current_location,
                routing_path_block_ids=routing_path,
            )
        )


@pytest.mark.parametrize(
    "when_rule_comparison_id,expected",
    (
        (
            "list_item_id",
            True,
        ),
        (
            "invalid-location-id",
            False,
        ),
    ),
)
def test_primary_person_checks_location(
    when_rule_comparison_id, expected, answer_store, questionnaire_schema
):
    list_store = ListStore(
        existing_items=[
            {
                "name": "people",
                "primary_person": "abcdef",
                "items": ["abcdef", "12345"],
            }
        ]
    )

    current_location = RelationshipLocation(
        section_id="some-section",
        block_id="some-block",
        list_item_id="abcdef",
        to_list_item_id="12345",
        list_name="household",
    )

    when_rules = [
        {
            "list": "people",
            "id_selector": "primary_person",
            "condition": "equals",
            "comparison": {"source": "location", "id": when_rule_comparison_id},
        }
    ]

    assert (
        evaluate_when_rules(
            when_rules=when_rules,
            schema=questionnaire_schema,
            metadata={},
            answer_store=answer_store,
            list_store=list_store,
            current_location=current_location,
        )
        is expected
    )


def test_when_rule_returns_first_item_in_list(answer_store, questionnaire_schema):
    list_store = ListStore(
        existing_items=[{"name": "people", "items": ["abcdef", "12345"]}]
    )

    current_location = Location(
        section_id="some-section",
        block_id="some-block",
        list_name="people",
        list_item_id="abcdef",
    )

    when_rules = [
        {
            "list": "people",
            "id_selector": "first",
            "condition": "equals",
            "comparison": {"source": "location", "id": "list_item_id"},
        }
    ]

    assert evaluate_when_rules(
        when_rules=when_rules,
        schema=questionnaire_schema,
        metadata={},
        answer_store=answer_store,
        list_store=list_store,
        current_location=current_location,
    )
